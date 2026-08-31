# OWNER: P1
#
# PURPOSE:
# Handle configuration for the generator.

import os

class GeneratorConfig:
    def __init__(self):
        self.event_rate = int(os.getenv("GENERATOR_EVENT_RATE", "100"))
        self.symbols = os.getenv("GENERATOR_SYMBOLS", "AAPL,MSFT,GOOGL,AMZN").split(",")
        self.seed = os.getenv("GENERATOR_SEED")
        if self.seed is not None:
            self.seed = int(self.seed)
        self.replay_speed = float(os.getenv("GENERATOR_REPLAY_SPEED", "1.0"))
        
        # Fault probabilities
        self.prob_malformed = float(os.getenv("FAULT_PROB_MALFORMED", "0.0"))
        self.prob_duplicate = float(os.getenv("FAULT_PROB_DUPLICATE", "0.0"))
        self.prob_late = float(os.getenv("FAULT_PROB_LATE", "0.0"))
        self.prob_out_of_order = float(os.getenv("FAULT_PROB_OUT_OF_ORDER", "0.0"))
        self.prob_anomaly = float(os.getenv("FAULT_PROB_ANOMALY", "0.0"))
        self.burst_multiplier = int(os.getenv("FAULT_BURST_MULTIPLIER", "1"))

settings = GeneratorConfig()
