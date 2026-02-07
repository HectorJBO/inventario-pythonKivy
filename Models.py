from sqlalchemy import Column, Integer, String, Float, MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine('sqlite:///ivan.db')
metadata = MetaData()
bs = declarative_base()

class Productos(bs):
    __tablename__ ='repuestos'
    id = Column(Integer, primary_key=True)
    Nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    
bs.metadata.create_all(db)
session = sessionmaker(bind=db)
sess = session()