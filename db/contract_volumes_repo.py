import time
from sdk.db.pg_client import PgClient
from sqlalchemy import (Column, DateTime, Float, Integer, String, Table, desc,
                        select)
from sqlalchemy.dialects.postgresql import insert


class ContractVolumesRepo:
    def __init__(
        self,
        pg_client: PgClient
    ):
        self.pg_client = pg_client
        self.table = Table(
            'contract_volumes',
            pg_client.meta_data,
            Column('date_str', String(16), primary_key=True),
            Column('address', String(42), primary_key=True),
            Column('timestamp', DateTime(), index=True, nullable=False),
            Column('updated', Integer(), index=True, nullable=False),
            Column('name', String(128), nullable=True),
            Column('volume', Integer(), nullable=False),
            Column('volume_usd', Float(), nullable=False),
        )

        pg_client.meta_data.create_all(pg_client.engine)

    def find_all(self):
        start = time.perf_counter()
        
        result = list(
            self.pg_client.conn.execute(
                select(self.table).order_by('date_str')
            )
        )
        
        print(f"⏱  [contract_volumes_repo.find_all] {time.perf_counter() - start:0.3f}s")
        
        return result

    def save(self, models):
        start = time.perf_counter()
        
        stmt = insert(self.table)
        self.pg_client.conn.execute(
            stmt
            .on_conflict_do_update(
                index_elements=["date_str", "address"],
                set_={
                    "volume": stmt.excluded.volume,
                    "volume_usd": stmt.excluded.volume_usd
                }
            ),
            models
        )
        
        print(f"⏱  [contract_volumes_repo.save] {time.perf_counter() - start:0.3f}s")
