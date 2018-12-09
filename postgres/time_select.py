import time, os
import numpy as np
from sqlalchemy import create_engine, Table, MetaData, text
from sqlalchemy.sql import select, column

def select_random(engine, table, nsel=5):
    columns = [col.name for col in table.columns][1:]  # Skip id column
    selected_cols = np.random.choice(columns, nsel, False)
    sql = text("select {} from column_test".format(", ".join(selected_cols)))
    results = engine.execute(sql)
    data = []
    for row in results:
        data.append(row)
    return data

def time_select(engine, table, ncols):
    st_time = time.time()
    select_random(engine, table, ncols)
    end_time = time.time()
    return end_time - st_time

if __name__ == "__main__":
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASS'],
        os.environ['DB_SERVICE'],
        os.environ['DB_PORT'],
        os.environ['DB_NAME']))
    metadata = MetaData()
    column_test_table = Table('column_test', metadata, autoload=True, autoload_with=engine)
    print(time_select(engine, column_test_table, 30))
