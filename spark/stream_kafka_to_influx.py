import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp, window, avg, sum as _sum, max as _max
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

from spark_common import env

KAFKA_BOOTSTRAP = env("KAFKA_BOOTSTRAP", "master:9092")
TOPIC = env("KAFKA_TOPIC", "crypto_ticks")

INFLUX_URL = env("INFLUX_URL", "http://localhost:8086")
INFLUX_ORG = env("INFLUX_ORG", "bigdata")
INFLUX_BUCKET = env("INFLUX_BUCKET", "crypto")
INFLUX_TOKEN = env("INFLUX_TOKEN", "")

schema = StructType([
    StructField("source", StringType(), True),
    StructField("symbol", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("volume_24h", DoubleType(), True),
    StructField("ts", StringType(), True),
])

def main():
    if not INFLUX_TOKEN:
        raise RuntimeError("Missing INFLUX_TOKEN in environment (.env).")

    spark = (
        SparkSession.builder
        .appName("KafkaToInfluxCrypto")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", TOPIC)
        .option("startingOffsets", "latest")
        .load()
    )

    parsed = (
        df.selectExpr("CAST(value AS STRING) as json_str")
        .select(from_json(col("json_str"), schema).alias("d"))
        .select(
            col("d.source").alias("source"),
            col("d.symbol").alias("symbol"),
            col("d.price").alias("price"),
            col("d.volume_24h").alias("volume_24h"),
            to_timestamp(col("d.ts")).alias("time")
        )
        .filter(col("symbol").isNotNull() & col("price").isNotNull() & col("time").isNotNull())
    )

    # 1) latest measurement
    latest = (
        parsed
        .withWatermark("time", "5 minutes")
        .groupBy("source", "symbol")
        .agg(_max("time").alias("time"), _max("price").alias("price"), _max("volume_24h").alias("volume_24h"))
    )

    # 2) 1-min aggregations
    agg_1min = (
        parsed
        .withWatermark("time", "10 minutes")
        .groupBy(window(col("time"), "1 minute"), col("source"), col("symbol"))
        .agg(
            avg("price").alias("avg_price"),
            _sum("volume_24h").alias("sum_volume_24h")
        )
        .select(
            col("window.start").alias("time"),
            col("source"),
            col("symbol"),
            col("avg_price"),
            col("sum_volume_24h")
        )
    )

    # Write latest to InfluxDB
    q1 = (
        latest.writeStream
        .outputMode("update")
        .format("influxdb")
        .option("influxdb.url", INFLUX_URL)
        .option("influxdb.token", INFLUX_TOKEN)
        .option("influxdb.org", INFLUX_ORG)
        .option("influxdb.bucket", INFLUX_BUCKET)
        .option("influxdb.measurement", "crypto_latest")
        .option("checkpointLocation", "checkpoint/crypto_latest")
        .start()
    )

    # Write 1min to InfluxDB
    q2 = (
        agg_1min.writeStream
        .outputMode("append")
        .format("influxdb")
        .option("influxdb.url", INFLUX_URL)
        .option("influxdb.token", INFLUX_TOKEN)
        .option("influxdb.org", INFLUX_ORG)
        .option("influxdb.bucket", INFLUX_BUCKET)
        .option("influxdb.measurement", "crypto_1min")
        .option("checkpointLocation", "checkpoint/crypto_1min")
        .start()
    )

    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    main()
