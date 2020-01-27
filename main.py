import pandas as pd

names = []
labels = []
with open('data/9k.names', 'rb') as input_file:
    for line in input_file:
        names.append(line.decode("utf-8") )
with open('data/9k.labels', 'rb') as input_file:
    for line in input_file:
        labels.append(line.decode("utf-8") )

data = pd.DataFrame(list(zip(names, labels)), columns=['name', 'label'])
pass