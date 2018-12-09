import time, os
import numpy as np
import pyarrow.parquet as pq

def time_select(table, ncols, nsel=5):
    column_names = [ 'col{:03d}'.format(i) for i in range(ncols) ]
    selected_cols = np.random.choice(column_names, nsel, False)
    st_time = time.time()
    data = pq.read_table(table, columns=selected_cols)
    end_time = time.time()
    return end_time - st_time
