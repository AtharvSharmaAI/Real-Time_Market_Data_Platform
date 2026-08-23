# OWNER: P2
#
# PURPOSE:
# Kafka consumer wrapper.
#
# RESPONSIBILITIES:
# consume raw-trades
# deserialize
# pass events into processing pipeline
# commit offsets only according to chosen processing semantics
# document at-least-once/idempotency assumptions
#
# DEPENDENCIES:
# confluent-kafka
#
# INTERFACES:
# INPUT: Kafka Topic
# OUTPUT: Events
#
# IMPLEMENTATION TODO:
# 1. Implement consumer loop and offset management.
#
# DO NOT IMPLEMENT YET.
