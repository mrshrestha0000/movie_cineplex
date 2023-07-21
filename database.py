import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative 
import sqlalchemy.orm as _orm

DATABASE_URL = "sqlite:///./movie_database.db"
# DATABASE_URL = "postgresql://postgres:password@postgres/fastapi_postgres"


engine = sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()