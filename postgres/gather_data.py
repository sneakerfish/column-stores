import csv
import os
from sqlalchemy import create_engine, Table, MetaData
import sqlalchemy

from load_table import load_table
from drop_table import drop_table
from time_select import time_select
from create_table import create_table

if __name__ == "__main__":
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASS'],
        os.environ['DB_SERVICE'],
        os.environ['DB_PORT'],
        os.environ['DB_NAME']))
    metadata = MetaData()
    with open("column-data.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['n columns', 'n rows', 'n rows sampled', 'sample', 'time'])
        for colno in [100, 500, 1000]:
            for rowno in [1000, 10000, 100000, 500000]:
                try:
                    drop_table(engine, metadata, 'column_test')
                except sqlalchemy.exc.NoSuchTableError:
                    pass
                metadata = MetaData()
                print("Creating table for {} columns, {} rows.".format(colno, rowno))
                create_table(engine, metadata, colno)
                table = Table('column_test', metadata, autoload=True, autoload_with=engine)
                load_table(engine, table, rowno, colno)
                for nsamp in [5, 10, 50]:
                    for sample in range(50):
                        writer.writerow([colno, rowno, nsamp, sample, time_select(engine, table, nsamp)])
