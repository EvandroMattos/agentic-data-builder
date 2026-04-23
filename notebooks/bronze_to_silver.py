# Databricks notebook source

import requests
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# --- INGESTÃO (BRONZE) ---
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json"
response = requests.get(url)
data = response.json()

df = spark.createDataFrame(data)

# salvar bronze
df.write.mode("overwrite").format("delta").save("/tmp/bronze/bacen")

# --- TRANSFORMAÇÃO (SILVER) ---
silver_df = (
    df.withColumnRenamed("data", "date")
      .withColumnRenamed("valor", "value")
)

silver_df.write.mode("overwrite").format("delta").save("/tmp/silver/bacen")

print("✅ Pipeline executado com sucesso")