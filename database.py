import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative 
import sqlalchemy.orm as _orm

# DATABASE_URL = "postgresql://postgres:password@127.0.0.1:8081/fastapi_postgres"
DATABASE_URL = "postgresql://postgres:password@postgres/fastapi_postgres"



engine = sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()

# Base.metadata.create_all(bind=engine)



# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


# POSTGRES_DATABASE_URL = "postgresql://postgres:password@127.0.0.1:8081/fastapi_postgres"

# engine = create_engine(POSTGRES_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()