```python
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Open Data Pipeline") \
    .getOrCreate()

def bronze_layer_ingestion(source_path: str) -> DataFrame:
    """
    Ingest data from the source path into the Bronze layer.
    
    :param source_path: Path to the source data (e.g., CSV, JSON)
    :return: DataFrame containing the raw data
    """
    # Read raw data from the source
    raw_data = spark.read.option("header", "true").csv(source_path)
    return raw_data

def silver_layer_transformation(raw_data: DataFrame) -> DataFrame:
    """
    Transform the raw data into the Silver layer.
    
    :param raw_data: DataFrame containing the raw data
    :return: DataFrame containing the cleaned and transformed data
    """
    # Example transformation: Select specific columns and filter rows
    transformed_data = raw_data.select("column1", "column2", "column3") \
        .filter(col("column1").isNotNull()) \
        .dropDuplicates()
    
    return transformed_data

def write_to_parquet(data: DataFrame, output_path: str):
    """
    Write the transformed data to Parquet format.
    
    :param data: DataFrame containing the transformed data
    :param output_path: Path to save the Parquet files
    """
    data.write.mode("overwrite").parquet(output_path)

def main():
    # Define paths
    source_path = "path/to/open/data.csv"
    bronze_output_path = "path/to/bronze_layer"
    silver_output_path = "path/to/silver_layer"

    # Bronze Layer: Ingest data
    raw_data = bronze_layer_ingestion(source_path)
    raw_data.write.mode("overwrite").parquet(bronze_output_path)

    # Silver Layer: Transform data
    transformed_data = silver_layer_transformation(raw_data)
    write_to_parquet(transformed_data, silver_output_path)

if __name__ == "__main__":
    main()
    # Stop the Spark session
    spark.stop()
```