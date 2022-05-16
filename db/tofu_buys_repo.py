import time
from ekp_sdk.db import PgClient
from sqlalchemy import (Column, DateTime, Float, Integer, String, Table, desc,
                        select)
from sqlalchemy.dialects.postgresql import insert


class TofuBuysRepo:
    def __init__(
        self,
        pg_client: PgClient
    ):
        self.pg_client = pg_client
        self.table = Table(
            'tofu_buys',
            pg_client.meta_data,
            Column('hash', String(128), primary_key=True),
            Column('block_number', Integer(), index=True, nullable=False),
            Column('gas_price', String(64), nullable=False),
            Column('gas_used', Integer(), nullable=False),
            Column('nft_contract_address', String(42), index=True, nullable=False),
            Column('value', String(64), nullable=False),
            Column('currency', String(42), nullable=False),
            Column('value_usd', Float(), nullable=False),
            Column('timestamp', DateTime(), index=True, nullable=False),
            Column('timestamp_unix', Integer(), index=True, nullable=False),
        )

        pg_client.meta_data.create_all(pg_client.engine)

    def find_latest(self):
        
        start = time.perf_counter()
        
        result = list(
            self.pg_client.conn.execute(
                select(self.table)
                .order_by(desc('timestamp_unix'))
                .limit(1)
            )
        )

        print(f"⏱  [tofu_buys_repo.find_latest] {time.perf_counter() - start:0.3f}s")

        if (len(result)):
            return result[0]

        return None

    def save(self, models):
        start = time.perf_counter()
        
        self.pg_client.conn.execute(
            insert(self.table)
            .on_conflict_do_nothing(index_elements=["hash"]),
            models
        )
        
        print(f"⏱  [tofu_buys_repo.save] {time.perf_counter() - start:0.3f}s")
