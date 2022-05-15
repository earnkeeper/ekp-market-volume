from sqlalchemy import Column, DateTime, Integer, String, Table, Float
from sqlalchemy import select, desc
from sqlalchemy.dialects.postgresql import insert

class TofuBuysRepo:
    def __init__(self, pg_db):
        self.pg_db = pg_db
        self.table = Table('tofu_buys', pg_db.meta_data,
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

        self.pg_db.meta_data.create_all(pg_db.engine)

    def find_latest(self):
        result = list(
            self.pg_db.conn.execute(
                select(self.table).order_by(desc('timestamp_unix')).limit(1)
            )
        )

        if (len(result)):
            return result[0]

        return None
    
    def save(self, models):
        stmt = insert(self.table)
        self.pg_db.conn.execute(
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
