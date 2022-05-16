import time

from ekp_sdk.db import PgClient
from sqlalchemy import (Boolean, Column, DateTime, Index, Integer, String, Table,
                        Text, desc, select)
from sqlalchemy.dialects.postgresql import insert


class TransactionsRepo:
    def __init__(
        self,
        pg_client: PgClient
    ):
        self.pg_client = pg_client
        self.table = Table(
            'transactions',
            pg_client.meta_data,
            Column('hash', String(128), primary_key=True),
            Column('block_hash', String(128), nullable=False),
            Column('block_number', Integer(), index=True, nullable=False),
            Column('cumulative_gas_used', Integer(), nullable=False),
            Column('from', String(42), index=True, nullable=False),
            Column('gas_price', String(64), nullable=False),
            Column('gas_used', Integer(), nullable=False),
            Column('input_method', String(10), index=True, nullable=True),
            Column('input', Text(), nullable=False),
            Column('is_error', Boolean(), nullable=False),
            Column('query_address', String(42), index=True, nullable=False),
            Column('timestamp', DateTime(), index=True, nullable=False),
            Column('timestamp_unix', Integer(), index=True, nullable=False),
            Column('to', String(42), index=True, nullable=False),
            Column('transaction_index', Integer(), nullable=False),
            Index('idx_find_latest', 'query_address', 'timestamp'),
            Index('idx_find_next_by_source','query_address', 'input_method', 'timestamp_unix'),
        )

        self.pg_client.meta_data.create_all(pg_client.engine)

    def find_latest(self, query_address):
        start = time.perf_counter()
        
        result = list(
            self.pg_client.conn.execute(
                select(self.table)
                .where(self.table.c.query_address == query_address)
                .order_by(desc('timestamp'))
                .limit(1)
            )
        )

        print(f"⏱  [transactions_repo.find_latest] {time.perf_counter() - start:0.3f}s")
        
        if (len(result)):
            return result[0]

        return None

    def find_next_by_source(self, query_address, input_method, start_timestamp, limit):
        start = time.perf_counter()
        
        result =  list(
            self.pg_client.conn.execute(
                select(self.table)
                .where(self.table.c.query_address == query_address)
                .where(self.table.c.input_method == input_method)
                .where(self.table.c.timestamp_unix > start_timestamp)
                .order_by('timestamp_unix')
                .limit(limit)
            )
        )
        
        print(f"⏱  [transactions_repo.find_next_by_source] {time.perf_counter() - start:0.3f}s")
        
        return result

    def save(self, models):
        
        start = time.perf_counter()
        
        self.pg_client.conn.execute(
            insert(self.table)
            .on_conflict_do_nothing(index_elements=["hash"]),
            models
        )
        
        print(f"⏱  [transactions_repo.save] {time.perf_counter() - start:0.3f}s")
