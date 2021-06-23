import uuid

import pandas

df = pandas.read_csv('input/supporters.csv')

df['id'] = [f"t{str(uuid.uuid4().hex)[:5]}" for _ in range(len(df.index))]

df.to_csv('output/supporters.csv')
