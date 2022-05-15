from sqlalchemy import Column, DateTime, Integer, String, Table, Float
from sqlalchemy import select, desc
from sqlalchemy.dialects.postgresql import insert

class ContractVolumesRepo:
    def __init__(self, pg_db):
        self.pg_db = pg_db
        self.table = Table('contract_volumes', pg_db.meta_data,
                           Column('date_str', String(16), primary_key=True),
                           Column('address', String(42), nullable=True),
                           Column('name', String(128), nullable=True),
                           Column('volume', Integer(), nullable=False),
                           Column('volume_usd', Float(), nullable=False),
                           )

        self.pg_db.meta_data.create_all(pg_db.engine)

    def find_all(self):
        return list(
            self.pg_db.conn.execute(
                select(self.table).order_by('date_str')
            )
        )
    
    def save(self, models):
        self.pg_db.conn.execute(
            insert(self.table)
            .on_conflict_do_nothing(index_elements=["hash"]),
            models
        )
