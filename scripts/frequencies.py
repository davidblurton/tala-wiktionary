import csv


class Frequencies:
    def __init__(self, csv):
        self.freqs = {}

        with open(csv) as file:
            reader = csv.reader(file)

            for (word, frequency) in reader:
                self.freqs[word] = frequency

    def get(self, word, default=0):
        try:
            return self.freqs[words]
        except KeyError:
            return default
