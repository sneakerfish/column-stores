import os
from sqlalchemy import create_engine, Table, MetaData
from numpy.random import random_sample


def load_table(engine, table, nrows, ncols):
    for i in range(nrows // 1000):
        data_rows = []
        for i in range(1000):
            # tolist() gives plain Python floats, which the database driver understands
            randomdata = random_sample(ncols).tolist()
            data = { 'col{:03d}'.format(i): randomdata[i] for i in range(ncols) }
            data_rows.append(data)
        with engine.begin() as conn:
            conn.execute(table.insert(), data_rows)

if __name__ == "__main__":
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASS'],
        os.environ['DB_SERVICE'],
        os.environ['DB_PORT'],
        os.environ['DB_NAME']))
    metadata = MetaData()
    table = Table('column_test', metadata, autoload_with=engine)
    load_table(engine, table, 100000, 100)
