
from pyspark.sql import SparkSession


# postgreSQL_driver = '/Users/macos/Downloads/WORKSPACE/data-engineer-project/Real-time-Presidential-Voting-System-with-Kafka-and-Spark/spark_service/postgresql-42.7.1.jar'
# app_name = 'RealTimeVotingEngineering'

spark_sesion = (SparkSession.builder
            .appName('RealTimeVotingEngineering')
            .config("spark.jars.packages",
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")  # Spark-Kafka integration
            .config("spark.jars",
                    "postgresql-42.7.1.jar")  # PostgreSQL driver
            .config("spark.sql.adaptive.enabled", "false")  # Disable adaptive query execution
            .getOrCreate())
