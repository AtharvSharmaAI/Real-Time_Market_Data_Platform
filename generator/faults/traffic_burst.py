# OWNER: P1
#
# PURPOSE:
# Inject traffic bursts.

class TrafficBurstController:
    def __init__(self, multiplier: int = 5):
        self.multiplier = multiplier
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def get_current_rate(self, baseline_rate: int) -> int:
        """
        Calculate target event rate.
        """
        if self.active:
            return baseline_rate * self.multiplier
        return baseline_rate
