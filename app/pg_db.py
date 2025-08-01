import sqlalchemy
import uuid
from sqlalchemy import DateTime
import databases
from sqlalchemy import (
    Table, Column, Integer, BigInteger, String, Text, Float,
    Boolean, TIMESTAMP, ForeignKey, MetaData, create_engine
)
from datetime import datetime
import os


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mymarket")

database = databases.Database(DATABASE_URL)

metadata = MetaData()



categories = Table(
    "categories",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("parent_id", BigInteger, ForeignKey("categories.id"), nullable=True),
    Column("name", String(255), unique=True, nullable=False),
    Column("description", Text, nullable=True),
    Column("created_at", TIMESTAMP, default=datetime.utcnow, nullable=False),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
)

users = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("username", String(100), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("role_id", BigInteger, nullable=False, default=1),
    Column("created_at", TIMESTAMP, default=datetime.utcnow, nullable=False),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
    Column("created_by", String(100), nullable=True),
    Column("updated_by", String(100), nullable=True)
)


products = Table(
    "products",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False,unique=True),
    Column("description", Text, nullable=True),
    Column("price", Float, nullable=False),
    Column("image_url", Text, nullable=True),
    Column("quantity", BigInteger, default=0, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("category_id", BigInteger, ForeignKey("categories.id"), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow, nullable=False),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
    Column("created_by", String(100), nullable=True),
    Column("updated_by", String(100), nullable=True),
)



files = Table(
    'files',
    metadata,
    Column('uuid', String(36), primary_key=True, default=str(uuid.uuid4), nullable=False),
    Column('name', String(255), nullable=False, unique=True),
    Column('type', String(50), nullable=False),
    Column('weight', Float, nullable=False),
    Column('uploaded_at', DateTime, default=datetime.utcnow, nullable=False),
    Column('uploaded_by', String(100), nullable=False),
    Column('status', String(20), default='active', nullable=False)
)



engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300
)

