from pyspark.sql.types import IntegerType, TimestampType
from pyspark.sql.functions import from_json, col
from pyspark.sql.functions import sum as _sum
from spark_table import vote_schema
from spark_config import spark_sesion

broker_address = 'broker:29092'
TOPIC = 'topic_votes'

# Read data from Kafka 'votes_topic' and process it
votes_df = spark_sesion.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers",broker_address) \
        .option("subscribe", TOPIC) \
        .option("startingOffsets", "earliest") \
        .load() \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), vote_schema).alias("data")) \
        .select("data.*")

# Data preprocessing: type casting and watermarking
votes_df = votes_df.withColumn("voting_time", col("voting_time").cast(TimestampType())) \
    .withColumn('vote', col('vote').cast(IntegerType()))
enriched_votes_df = votes_df.withWatermark("voting_time", "1 minute")

# Aggregate votes per candidate and turnout by location
votes_per_candidate = enriched_votes_df.groupBy("candidate_id", "candidate_name", "party_affiliation",
                                                "photo_url").agg(_sum("vote").alias("total_votes"))
turnout_by_location = enriched_votes_df.groupBy("address.state").count().alias("total_votes")

# Write aggregated data to Kafka topics ('aggregated_votes_per_candidate', 'aggregated_turnout_by_location')
votes_per_candidate_to_kafka = votes_per_candidate.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", broker_address) \
    .option("topic", "aggregated_votes_per_candidate") \
    .option("checkpointLocation", "./checkpoints/checkpoints1") \
    .outputMode("update") \
    .start()

turnout_by_location_to_kafka = turnout_by_location.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", broker_address) \
    .option("topic", "aggregated_turnout_by_location") \
    .option("checkpointLocation", "./checkpoints/checkpoints2") \
    .outputMode("update") \
    .start()