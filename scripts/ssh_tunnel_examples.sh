#!/usr/bin/env bash
echo "Examples :"
echo ""
echo "Grafana tunnel:"
echo "  ssh -L 3001:localhost:3001 adm-mcsc@<VM_PUBLIC_IP>"
echo ""
echo "Influx tunnel:"
echo "  ssh -L 8086:localhost:8086 adm-mcsc@<VM_PUBLIC_IP>"
