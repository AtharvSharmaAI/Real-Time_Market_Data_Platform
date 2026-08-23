# OWNER: P2
#
# PURPOSE:
# Handle watermarks.
#
# RESPONSIBILITIES:
# Explain exact intended rule:
# watermark = max(event_time_seen) - 3 seconds
# Document:
# - watermark progression
# - why 3 seconds is used
# - window closure
# - late-event behavior
#
# DEPENDENCIES:
# None
#
# INTERFACES:
# INPUT: Event Time
# OUTPUT: Watermark
#
# IMPLEMENTATION TODO:
# 1. Implement watermark generation.
#
# DO NOT IMPLEMENT YET.
