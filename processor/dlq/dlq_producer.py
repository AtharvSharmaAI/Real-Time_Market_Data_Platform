# OWNER: P2
#
# PURPOSE:
# Produce events to DLQ.
#
# RESPONSIBILITIES:
# Comments explain DLQ event format:
# - original event
# - error category
# - error message
# - ingestion/processing timestamp
# - schema version
# Malformed events go to DLQ.
# Valid but unusual events do NOT go to DLQ.
#
# DEPENDENCIES:
# Kafka producer
#
# INTERFACES:
# INPUT: Malformed Event
# OUTPUT: Kafka Topic (DLQ)
#
# IMPLEMENTATION TODO:
# 1. Implement DLQ producer logic.
#
# DO NOT IMPLEMENT YET.
