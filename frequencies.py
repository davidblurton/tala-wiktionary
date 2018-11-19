import csv

# Exclude words which are nouns but more common as some other word class
exclude = ['ekki', 'ef', 'var', 'hver', 'sig', 'bara', 'vera', 'koma', 'tala', 'sjá', 'átt', 'skil']

class Frequencies:
    def __init__(self, csvFile):
        self.freqs = {}

        with open(csvFile) as file:
            reader = csv.reader(file)

            for (word, frequency) in reader:
                self.freqs[word] = frequency

        for exclusion in exclude:
            self.freqs[exclusion] = None

    def get(self, word, default=None):
        return self.freqs.get(word, default)
