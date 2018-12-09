import os
from sqlalchemy import *
from optparse import OptionParser

def create_table(engine, metadata, ncols=100):
    cols = [Column('id', Integer, primary_key=True)]
    for i in range(ncols):
        cols.append(Column('col{:03d}'.format(i), Float))
    coltest = Table('column_test', metadata, *cols)
    metadata.create_all(engine)

if __name__ == "__main__":
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASS'],
        os.environ['DB_SERVICE'],
        os.environ['DB_PORT'],
        os.environ['DB_NAME']))
    metadata = MetaData()
    create_table(engine, metadata)
