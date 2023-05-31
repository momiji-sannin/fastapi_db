from pydantic import BaseModel
import datetime

class PaymentBase(BaseModel):
    fecha: datetime.datetime
    monto: float

class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    _id: int
    cliente_id: int
    proveedor_id: int

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    nombre: str


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    _id: int

    class Config:
        orm_mode = True


class ProviderBase(BaseModel):
    nombre: str


class ProviderCreate(ProviderBase):
    pass


class Provider(ProviderBase):
    _id: int

    class Config:
        orm_mode = True