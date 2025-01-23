from pyspark.sql import SparkSession
from config import DATALAKE_CONFIG
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
)
from dotenv import load_dotenv
import os

load_dotenv()

AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
AZURE_STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET_KEY = os.getenv("AZURE_CLIENT_SECRET_KEY")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")


votesSchema = StructType(
    [
        StructField("voter_id", StringType(), True),
        StructField("candidate_id", StringType(), True),
        StructField("voting_time", TimestampType(), True),
        StructField("voter_name", StringType(), True),
        StructField("party_affiliation", StringType(), True),
        StructField("biography", StringType(), True),
        StructField("campaign_platform", StringType(), True),
        StructField("photo_url", StringType(), True),
        StructField("candidate_name", StringType(), True),
        StructField("date_of_birth", StringType(), True),
        StructField("age", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("nationality", StringType(), True),
        StructField("registration_number", StringType(), True),
        StructField(
            "address",
            StructType(
                [
                    StructField("street", StringType(), True),
                    StructField("city", StringType(), True),
                    StructField("state", StringType(), True),
                    StructField("country", StringType(), True),
                    StructField("postcode", StringType(), True),
                ]
            ),
            True,
        ),
        StructField("email", StringType(), True),
        StructField("phone_number", StringType(), True),
        StructField("cell_number", StringType(), True),
        StructField("picture", StringType(), True),
        StructField("registered_age", IntegerType(), True),
        StructField("vote", IntegerType(), True),
    ]
)


def main():
    spark = (
        SparkSession.builder.appName("VotingDataPlatform")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,"
            "org.apache.hadoop:hadoop-azure-datalake:3.3.1,"
            "com.microsoft.azure:azure-storage:8.6.5",
        )
        .config(
            "spark.hadoop.fs.azure", "org.apache.hadoop.fs.azure.NativeAzureFileSystem"
        )
        .config(
            f"spark.hadoop.fs.azure.account.key.{AZURE_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
            AZURE_STORAGE_ACCOUNT_KEY,
        )
        .config(
            f"spark.hadoop.fs.azure.account.oauth.provider.type.{AZURE_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
            "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        )
        .config(
            f"spark.hadoop.fs.azure.account.oauth2.client.id.{AZURE_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
            AZURE_CLIENT_ID,
        )
        .config(
            f"spark.hadoop.fs.azure.account.oauth2.client.secret.{AZURE_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
            AZURE_CLIENT_SECRET_KEY,
        )
        .config(
            f"spark.hadoop.fs.azure.account.oauth2.client.endpoint.{AZURE_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
            f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token",
        )
        .config(
            "spark.hadoop.fs.azure.createRemoteFileSystemDuringInitialization", "true"
        )
        .config("spark.sql.adaptive.enabled", "false")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    def read_kafka_topic(topic, schema):
        return (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", "broker:29092")
            .option("subscribe", topic)
            .option("startingOffsets", "earliest")
            .load()
            .selectExpr("CAST(value AS STRING)")
            .select(from_json(col("value"), schema).alias("data"))
            .select("data.*")
        )

    def streamWriter(input, checkpointFolder, output):
        return (
            input.writeStream.format("parquet")
            .option("checkpointLocation", checkpointFolder)
            .option("path", output)
            .outputMode("append")
            .start()
        )

    votesDF = read_kafka_topic("topic_votes", votesSchema).alias("votes")

    query5 = streamWriter(
        votesDF,
        "abfss://bronze-layer@datalakevotingplatform.dfs.core.windows.net/checkpoints/",
        "abfss://bronze-layer@datalakevotingplatform.dfs.core.windows.net/data/",
    )
    query5.awaitTermination()


if __name__ == "__main__":
    main()


"""
docker exec -it spark_service-spark-master-1 spark-submit \
    --master spark://spark-master:7077 \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-azure:3.3.1,com.microsoft.azure:azure-storage:8.6.5 \
    ingestion_service/kafka_to_datalake.py
"""
