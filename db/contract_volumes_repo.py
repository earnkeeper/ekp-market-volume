import time
from ekp_sdk.db import PgClient
from sqlalchemy import (Column, DateTime, Float, Integer, String, Table, desc,
                        select, func)
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
            Column('address', String(42), index=True, primary_key=True),
            Column('date_timestamp', Integer(), index=True, nullable=False),
            Column('updated', Integer(), index=True, nullable=False),
            Column('name', String(128), nullable=True),
            Column('volume', Integer(), nullable=False),
            Column('volume_usd', Float(), nullable=False),
        )

        pg_client.meta_data.create_all(pg_client.engine)

    def find_all_by_address(self, address, since = 0):
        start = time.perf_counter()

        result = list(
            self.pg_client.conn.execute(
                select(self.table)
                .where(self.table.c.address == address)
                .where(self.table.c.date_timestamp >= since)
                .order_by('date_timestamp')
            )
        )

        print(
            f"⏱  [contract_volumes_repo.find_all] {time.perf_counter() - start:0.3f}s")

        return result

    def group_by_address_and_name(self, since, limit):
        query = select([
            self.table.c.address,
            self.table.c.name,
            func.sum(self.table.c.volume),
            func.sum(self.table.c.volume_usd),
        ]).where(
            self.table.c.date_timestamp > since   
        ).group_by(
            self.table.c.address, 
            self.table.c.name
        ).order_by(func.sum(self.table.c.volume_usd).desc())
        
        results = self.pg_client.engine.execute(query).fetchmany(limit)
        
        rows = []
        
        i = 0
        for result in results:
            rows.append({
                "address": result[0],
                "name": result[1],
                "volume": result[2],
                "volume_usd": result[3],
            })
            i+=1
            if i >= limit:
                break
            
        return rows

    def find_all(self):
        start = time.perf_counter()

        result = list(
            self.pg_client.conn.execute(
                select(self.table)
                .order_by('date_timestamp')
            )
        )

        print(
            f"⏱  [contract_volumes_repo.find_all] {time.perf_counter() - start:0.3f}s")

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

        print(
            f"⏱  [contract_volumes_repo.save] {time.perf_counter() - start:0.3f}s")
