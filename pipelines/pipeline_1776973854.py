```python
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_timestamp

# Initialize Spark Session
def create_spark_session(app_name: str) -> SparkSession:
    """
    Create and return a Spark session.
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()
    return spark

# Bronze Layer Ingestion
def ingest_bronze_data(spark: SparkSession, bronze_path: str) -> DataFrame:
    """
    Ingest raw data from the Bronze layer.
    :param spark: Spark session
    :param bronze_path: Path to the Bronze layer data
    :return: DataFrame containing raw data
    """
    # Read raw data from the Bronze layer
    bronze_df = spark.read \
        .format("csv") \
        .option("header", "true") \
        .load(bronze_path)
    
    return bronze_df

# Silver Layer Transformation
def transform_to_silver(bronze_df: DataFrame) -> DataFrame:
    """
    Transform the Bronze DataFrame into the Silver layer.
    :param bronze_df: DataFrame containing raw data
    :return: Transformed DataFrame for Silver layer
    """
    # Example transformation: Clean and convert data types
    silver_df = bronze_df \
        .withColumn("timestamp", to_timestamp(col("timestamp_column"))) \
        .drop("unnecessary_column") \
        .filter(col("important_column").isNotNull())
    
    return silver_df

# Write Silver Layer Data
def write_silver_data(silver_df: DataFrame, silver_path: str) -> None:
    """
    Write the transformed Silver DataFrame to storage.
    :param silver_df: DataFrame containing transformed data
    :param silver_path: Path to save the Silver layer data
    """
    silver_df.write \
        .format("parquet") \
        .mode("overwrite") \
        .save(silver_path)

# Main Pipeline Execution
def main():
    # Define paths
    bronze_path = "s3://your-bucket/bronze/"
    silver_path = "s3://your-bucket/silver/"
    
    # Create Spark session
    spark = create_spark_session("DataPipeline")

    # Ingest data from Bronze layer
    bronze_df = ingest_bronze_data(spark, bronze_path)

    # Transform data to Silver layer
    silver_df = transform_to_silver(bronze_df)

    # Write transformed data to Silver layer
    write_silver_data(silver_df, silver_path)

    # Stop Spark session
    spark.stop()

if __name__ == "__main__":
    main()
```