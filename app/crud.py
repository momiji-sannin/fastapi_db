from sqlalchemy.orm import Session

from . import models, schemas


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client._id == client_id).first()

def get_client_name(db: Session, client_name: str):
    return db.query(models.Client).filter(models.Client.nombre == client_name).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(nombre=client.nombre)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def create_client_name(db: Session, client_name: str):
    db_client = models.Client(nombre=client_name)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_provider(db: Session, provider_id: int):
    return db.query(models.Provider).filter(models.Provider._id == provider_id).first()

def get_provider_name(db: Session, provider_name: str):
    return db.query(models.Provider).filter(models.Provider.nombre == provider_name).first()

def get_providers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Provider).offset(skip).limit(limit).all()


def create_provider(db: Session, provider: schemas.ProviderCreate):
    db_provider = models.Provider(nombre=provider.nombre)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


def create_provider_name(db: Session, provider_name: str):
    db_provider = models.Provider(nombre=provider_name)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


def get_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Payment).offset(skip).limit(limit).all()


def get_payments_by_client(db: Session, client_id):
    return db.query(models.Payment).filter(models.Payment.cliente_id == client_id).first()


def get_payments_by_provider(db: Session, provider_id):
    return db.query(models.Payment).filter(models.Payment.proveedor_id == provider_id).first()


def create_payment(db: Session, fecha:str, monto: float, client_id: int, provider_id: int):
    db_pay= models.Payment(fecha=fecha, monto=monto, cliente_id=client_id, proveedor_id=provider_id)
    db.add(db_pay)
    db.commit()
    db.refresh(db_pay)
    return db_pay