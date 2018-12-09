import os
from sqlalchemy import *
from optparse import OptionParser

def drop_table(engine, metadata, tablename):
    table = Table(tablename, metadata, autoload=True, autoload_with=engine)
    table.drop(engine)

if __name__ == "__main__":
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASS'],
        os.environ['DB_SERVICE'],
        os.environ['DB_PORT'],
        os.environ['DB_NAME']))
    metadata = MetaData()
    drop_table(engine, metadata, 'column_test')
