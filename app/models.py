from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
import datetime

from .database import Base


class Client(Base):
    __tablename__ = "clientes"

    _id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    #pagos = relationship("Payment", back_populates="client_id")


class Payment(Base):
    __tablename__ = "pagos"

    _id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.datetime.date)
    cliente_id = Column(Integer, ForeignKey("clientes._id"))
    monto = Column(Float)
    proveedor_id = Column(Integer, ForeignKey("proveedores._id"))

class Provider(Base):
    __tablename__ = "proveedores"

    _id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)