from decouple import config
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_URI = config("POSTGRES_URI")

class PgDb:
    def __init__(self):
        self.meta_data = MetaData()
        print('connecting to postgres')
        
        self.engine = create_engine(POSTGRES_URI)
        self.conn = self.engine.connect()
        print('postgres db connected')

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
