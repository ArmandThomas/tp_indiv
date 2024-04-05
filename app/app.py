from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag
from pyspark.sql.window import Window

# Créer une session Spark
spark = SparkSession.builder \
    .appName("Analyse Temporelle Sismique") \
    .getOrCreate()
# Charger les données dans un DataFrame Spark
data = spark.read.csv("hdfs://namenode:9000/data/dataset_sismique_villes.csv", header=True)

# Prétraitement des données (conversion de types, nettoyage, etc.)
# Supprimer les colonnes non nécessaires
data = data.select("ville", "secousse", "magnitude", "tension entre plaque", "date")
# Convertir le type de la colonne "time" en type de deate
data = data.withColumn("date", col("date").cast("timestamp"))

# Détection des motifs récurrents
# Créer une fenêtre de temps pour analyser les données temporelles
windowSpec = Window.orderBy("date")

# Utiliser la fonction lag pour comparer les valeurs précédentes et actuelles
data = data.withColumn("previous_magnitude", lag("magnitude", 1).over(windowSpec))
data = data.withColumn("magnitude_difference", col("magnitude") - col("previous_magnitude"))

# Identifier les séquences prédictives d'événements sismiques
# Filtrer les séismes avec une magnitude croissante pendant une certaine période
sequences = data.filter((col("magnitude_difference") > 0) & (col("magnitude_difference") < 1))

# Afficher les résultats
sequences.show()

# Arrêter la session Spark
spark.stop()
