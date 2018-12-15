import os
import time
import csv

from load_table import load_table
from time_select import time_select

if __name__ == "__main__":
    parquet_file = "column_test.parquet"
    output_file = "parquet-data.csv"
    with open(output_file, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['n columns', 'n rows', 'n rows sampled', 'sample', 'time'])
        for colno in [100, 500, 1000]:
            for rowno in [1000, 10000, 100000, 250000, 500000, 750000]:
                if os.path.isfile(parquet_file):
                    os.remove(parquet_file)
                print("Creating table for {} columns, {} rows.".format(colno, rowno))
                load_table(parquet_file, rowno, colno)
                for nsamp in [5, 10, 50]:
                    for sample in range(100):
                        writer.writerow([colno, rowno, nsamp, sample, time_select(parquet_file, colno, nsamp)])
