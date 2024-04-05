cat shared/data.json | kafka-console-producer.sh --broker-list kafka:9093 --topic data-seismes
