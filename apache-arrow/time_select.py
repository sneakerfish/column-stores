import time, os
import numpy as np
import pyarrow.parquet as pq

def select_random(table, ncols, nsel):
    column_names = [ 'col{:03d}'.format(i) for i in range(ncols) ]
    selected_cols = np.random.choice(column_names, nsel, False)
    data = pq.read_table(table, columns=selected_cols)
    return data

def time_select(table, ncols, nsel=5):
    st_time = time.time()
    select_random(table, ncols, nsel)
    end_time = time.time()
    return end_time - st_time
