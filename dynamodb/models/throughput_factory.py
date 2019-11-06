from .throughput import Throughput


class ThroughputFactory:

    def create(self, throughput):
        last_increased = None
        last_decreased = None

        if 'LastIncreaseDateTime' in throughput:
            last_increased = throughput['LastIncreaseDateTime']

        if 'LastDecreaseDateTime' in throughput:
            last_decreased = throughput['LastDecreaseDateTime']

        return Throughput(
            last_increased,
            last_decreased,
            throughput['NumberOfDecreasesToday'],
            throughput['ReadCapacityUnits'],
            throughput['WriteCapacityUnits'])
