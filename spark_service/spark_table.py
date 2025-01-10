from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType


vote_schema = StructType([
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
    StructField("address", StructType([
        StructField("street", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("country", StringType(), True),
        StructField("postcode", StringType(), True)
    ]), True),
    StructField("email", StringType(), True),
    StructField("phone_number", StringType(), True),
    StructField("cell_number", StringType(), True),
    StructField("picture", StringType(), True),
    StructField("registered_age", IntegerType(), True),
    StructField("vote", IntegerType(), True)
])