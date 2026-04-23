```python
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_timestamp

# Initialize Spark Session
def create_spark_session(app_name: str) -> SparkSession:
    """
    Create and return a Spark session.
    """
    return SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()

# Bronze Layer Ingestion
def ingest_bronze_data(spark: SparkSession, bronze_path: str) -> DataFrame:
    """
    Ingest data from the Bronze layer.
    
    :param spark: Spark session
    :param bronze_path: Path to the Bronze layer data
    :return: DataFrame containing the raw data
    """
    return spark.read.format("csv").option("header", "true").load(bronze_path)

# Silver Layer Transformation
def transform_to_silver(bronze_df: DataFrame) -> DataFrame:
    """
    Transform the Bronze DataFrame to Silver layer.
    
    :param bronze_df: DataFrame from the Bronze layer
    :return: Transformed DataFrame for the Silver layer
    """
    # Example transformation: Convert date column to timestamp and filter out nulls
    silver_df = bronze_df \
        .withColumn("event_timestamp", to_timestamp(col("event_date"), "yyyy-MM-dd")) \
        .drop("event_date") \
        .na.drop()
    
    return silver_df

# Write Silver Layer Data
def write_silver_data(silver_df: DataFrame, silver_path: str) -> None:
    """
    Write the transformed Silver DataFrame to storage.
    
    :param silver_df: DataFrame for the Silver layer
    :param silver_path: Path to save the Silver layer data
    """
    silver_df.write.mode("overwrite").parquet(silver_path)

# Main Pipeline Execution
def main():
    # Define paths
    bronze_path = "s3://your-bucket/bronze-layer/"
    silver_path = "s3://your-bucket/silver-layer/"
    
    # Create Spark session
    spark = create_spark_session("DataPipeline")

    # Ingest Bronze data
    bronze_df = ingest_bronze_data(spark, bronze_path)

    # Transform to Silver layer
    silver_df = transform_to_silver(bronze_df)

    # Write Silver data
    write_silver_data(silver_df, silver_path)

    # Stop Spark session
    spark.stop()

if __name__ == "__main__":
    main()
```