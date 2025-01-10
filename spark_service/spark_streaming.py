import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from spark_processing import votes_per_candidate_to_kafka, turnout_by_location_to_kafka


if __name__ == "__main__":
    try:
        # Start the first Spark streaming job
        votes_per_candidate_to_kafka.awaitTermination()
    except Exception as e:
        print(f"Error in votes_per_candidate_to_kafka: {e}")
    
    try:
        # Start the second Spark streaming job
        turnout_by_location_to_kafka.awaitTermination()
    except Exception as e:
        print(f"Error in turnout_by_location_to_kafka: {e}")


# kafka-topics --list --bootstrap-server broker:29092
# kafka-console-consumer --topic vehicle_data --bootstrap-server broker:9092 --from-beginning
# kafka-topics --delete --topic aggregated_votes_per_candidate --bootstrap-server broker:29092        
# kafka-topics --delete --topic gps_data --bootstrap-server broker:29092        
# kafka-topics --delete --topic traffic_data --bootstrap-server broker:29092        
# kafka-topics --delete --topic weather_data --bootstrap-server broker:29092       