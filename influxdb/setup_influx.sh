#!/usr/bin/env bash
set -e

# This script is optional. It assumes influx CLI is installed and you have admin access.
# If you already created org/bucket/token in UI, you can skip.

ORG="${INFLUX_ORG:-bigdata}"
BUCKET="${INFLUX_BUCKET:-crypto}"

echo "Create org/bucket using influx CLI (optional)."
echo "Example:"
echo "  influx setup --username admin --password '***' --org $ORG --bucket $BUCKET --force"
echo ""
echo "Then create a token in InfluxDB UI: Data -> Tokens"
