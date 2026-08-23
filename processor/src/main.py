# OWNER: P2
#
# PURPOSE:
# Orchestration entry point.
#
# RESPONSIBILITIES:
# It will eventually connect:
# Kafka consumer
# -> validation
# -> deduplication
# -> event-time processing
# -> watermark
# -> windows
# -> analytics
# -> anomaly detection
# -> output Kafka topic
# Keep orchestration separate from business logic.
#
# DEPENDENCIES:
# all processor submodules
#
# INTERFACES:
# INPUT: Kafka Consumer
# OUTPUT: Kafka Producer
#
# IMPLEMENTATION TODO:
# 1. Wire up pipeline components.
#
# DO NOT IMPLEMENT YET.
