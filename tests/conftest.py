import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import Base,get_db
from app.main import app
@pytest.fixture
def client():
    e=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    S=sessionmaker(bind=e,autoflush=False,autocommit=False); Base.metadata.create_all(bind=e)
    def override():
        d=S()
        try: yield d
        finally: d.close()
    app.dependency_overrides[get_db]=override
    with TestClient(app) as c: yield c
    app.dependency_overrides.clear()
