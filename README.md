# Column Stores: Parquet vs Postgres

A small experiment comparing how long it takes to select a random subset of
columns from a wide table stored in:

- **Postgres** (a row store), in [`postgres/`](postgres/)
- **Parquet** via Apache Arrow (a column store), in [`apache-arrow/`](apache-arrow/)

Each side has a `gather_data.py` script that builds tables of 100 / 500 / 1000
columns and 1,000 – 750,000 rows of random floats, then times repeated reads of
5, 10 and 50 randomly chosen columns. The timings are written to CSV and plotted
in [`notebook/column-vs-parquet.ipynb`](notebook/column-vs-parquet.ipynb).
The write-up is in `Parquet vs Postgers.pdf`.

Everything targets Python 3.12.

## 1. Postgres timings

`postgres/docker-compose.yml` runs Postgres 17, Redis and a small Flask app.
The scripts read their connection settings from `postgres/env`.

```sh
cd postgres
docker compose up -d db
docker compose run --rm web python gather_data.py   # writes column-data.csv
```

Or run the scripts on your host against the container:

```sh
cd postgres
uv venv && uv pip install -r requirements.txt
export DB_USER=postgres DB_PASS=inq6mth DB_SERVICE=localhost DB_PORT=5432 DB_NAME=columntest
uv run python create_table.py && uv run python load_table.py && uv run python time_select.py
```

The `columntest` database is created on first start (`POSTGRES_DB`). If you
have an old `postgres/tmp/db` directory from the Postgres 9.6 version of this
repo, delete it first: data directories are not compatible across major
versions.

## 2. Parquet timings

```sh
cd apache-arrow
uv venv && uv pip install -r requirements.txt
uv run python gather_data.py      # writes parquet-data.csv
```

(`docker compose run --rm app python gather_data.py` also works.)

The full run is large (up to 1000 columns x 750,000 rows); shrink the lists in
`gather_data.py` for a quick try.

## 3. Plot the results

The notebook expects `postgres-data.csv` and `parquet-data.csv` next to it:

```sh
cp postgres/column-data.csv notebook/postgres-data.csv
cp apache-arrow/parquet-data.csv notebook/parquet-data.csv

cd notebook
pipenv sync            # or: uvx pipenv sync
pipenv run jupyter notebook column-vs-parquet.ipynb
```

`notebook/Pipfile.lock` pins exact versions. To refresh it, run `pipenv lock`
(or `uvx pipenv lock`).
