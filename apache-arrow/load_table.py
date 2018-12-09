import numpy as np
from numpy.random import random_sample
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def load_table(filename, nrows, ncols=100):
    data = { 'col{:03d}'.format(i): random_sample(nrows) for i in range(ncols) }
    dataframe = pd.DataFrame(data)
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, filename)

if __name__ == "__main__":
    load_table('column_test.parquet', 100000, 100)
