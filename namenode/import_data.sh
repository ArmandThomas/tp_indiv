hdfs dfs -mkdir -p /data/
hdfs dfs -put ./shared/dataset_sismique.csv /data/dataset_sismique.csv
hdfs dfs -ls /data