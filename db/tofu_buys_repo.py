from sdk.db.pg_client import PgClient
from sqlalchemy import (Column, DateTime, Float, Integer, String, Table, desc,
                        select)
from sqlalchemy.dialects.postgresql import insert


class TofuBuysRepo:
    def __init__(
        self,
        pg_client: PgClient
    ):
        self.pg_client = pg_client
        self.table = Table('tofu_buys', pg_client.meta_data,
                           Column('hash', String(128), primary_key=True),
                           Column('block_number', Integer(), nullable=False),
                           Column('gas_price', String(64), nullable=False),
                           Column('gas_used', Integer(), nullable=False),
                           Column('nft_contract_address',
                                  String(42), nullable=False),
                           Column('value', String(64), nullable=False),
                           Column('currency', String(42), nullable=False),
                           Column('value_usd', Float(), nullable=False),
                           Column('timestamp', DateTime(), nullable=False),
                           Column('timestamp_unix', Integer(), nullable=False),
                           )

        pg_client.meta_data.create_all(pg_client.engine)

    def find_latest(self):
        result = list(
            self.pg_client.conn.execute(
                select(self.table).order_by(desc('timestamp_unix')).limit(1)
            )
        )

        if (len(result)):
            return result[0]

        return None

    def save(self, models):
        stmt = insert(self.table)
        self.pg_client.conn.execute(
            stmt
            .on_conflict_do_update(
                index_elements=["date_str"],
                set_={
                    "volume": stmt.excluded.cost,
                    "volume_usd": stmt.excluded.volume_usd
                }
            ),
            models
        )
