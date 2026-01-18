from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

from spark_common import env

KAFKA_BOOTSTRAP = env("KAFKA_BOOTSTRAP", "master:9092")
TOPIC = env("KAFKA_TOPIC", "crypto_ticks")
HDFS_OUT = env("HDFS_OUT", "hdfs:///data/crypto/raw")

def main():
    spark = SparkSession.builder.appName("KafkaToHDFSRaw").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", TOPIC)
        .option("startingOffsets", "latest")
        .load()
    )

    out = (
        df.selectExpr("CAST(value AS STRING) as json", "timestamp")
        .withColumn("day", to_date(col("timestamp")))
    )

    (
        out.writeStream
        .format("parquet")
        .option("path", HDFS_OUT)
        .option("checkpointLocation", "checkpoint/hdfs_raw")
        .partitionBy("day")
        .outputMode("append")
        .start()
        .awaitTermination()
    )

if __name__ == "__main__":
    main()
