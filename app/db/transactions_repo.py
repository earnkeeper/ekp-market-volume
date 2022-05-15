from sqlalchemy import Column, DateTime, Integer, String, Table, Boolean, Text
from sqlalchemy import select, desc
from sqlalchemy.dialects.postgresql import insert


class TransactionsRepo:
    def __init__(self, pg_db):
        self.pg_db = pg_db
        self.table = Table('transactions', pg_db.meta_data,
                           Column('hash', String(128), primary_key=True),
                           Column('block_hash', String(128), nullable=False),
                           Column('block_number', Integer(), nullable=False),
                           Column('cumulative_gas_used',
                                  Integer(), nullable=False),
                           Column('from', String(42), nullable=False),
                           Column('gas_price', String(64), nullable=False),
                           Column('gas_used', Integer(), nullable=False),
                           Column('input', Text(), nullable=False),
                           Column('is_error', Boolean(), nullable=False),
                           Column('query_address', String(42), nullable=False),
                           Column('timestamp', DateTime(), nullable=False),
                           Column('timestamp_unix', Integer(), nullable=False),
                           Column('to', String(42), nullable=False),
                           Column('transaction_index',
                                  Integer(), nullable=False),
                           )

        self.pg_db.meta_data.create_all(pg_db.engine)

    def find_latest(self):
        result = list(
            self.pg_db.conn.execute(
                select(self.table).order_by(desc('timestamp')).limit(1)
            )
        )

        if (len(result)):
            return result[0]

        return None

    def save(self, models):
        self.pg_db.conn.execute(
            insert(self.table)
            .on_conflict_do_nothing(index_elements=["hash"]),
            models
        )

    def find_next_by_source(self, query_address, method_id, start_timestamp, page_size):
        return list(
            self.pg_db.conn.execute(
                select(self.table)
                    .where(self.table.c.query_address == query_address)
                    .where(self.table.c.input.like(f"{method_id}%"))
                    .where(self.table.c.timestamp_unix > start_timestamp)
                    .order_by('timestamp')
                    .limit(page_size)
            )
        )
