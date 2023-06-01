import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
file_name = "payments.xlsx"
mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def validate_data(file_name):
    data = pd.read_excel(file_name)
    data.reset_index(drop=True, inplace=True)

    #? Validate if empty
    for col in data.columns.values:
        err = emptycol(data, col)
        if err is not None:
            return err 
        
    #? Validate date
    try:
        data["Fecha"] = pd.to_datetime(data["Fecha"].dt.strftime("%Y-%m-%d"))
    except:
        return {"Error" : "Fecha invalida"}
    
    #? Validate monto
    try:
        data["Monto"] = pd.to_numeric(data["Monto"], downcast="float")
    except:
        return {"Error" : "Monto invalido"}

    print("Validation Completed")
    return data
    

def emptycol(data: pd.DataFrame, col_name: str):
    result = pd.isna(data[col_name])
    if not result[result == True].empty:
        return {"Error" : f"{col_name} vacio en: {data.iloc[result[result == True].index.values].values}"}
    return None


def upload_to_db(db, data: pd.DataFrame):
    for _, x in data.iterrows():
        client = crud.get_client_name(db, client_name=x["Cliente"])
        if client is None:
            client = crud.create_client_name(db, x["Cliente"])
        provider = crud.get_provider_name(db, provider_name=x["Proveedor"])
        if provider is None:
            provider = crud.create_provider_name(db, x["Proveedor"])
        crud.create_payment(db, x["Fecha"], x["Monto"], client._id, provider._id)


def generate_excel_payments(db, payments: list[schemas.Payment]):
    df = get_dataframe(db, payments)
    df.to_excel("Pagos.xlsx")

def get_dataframe(db, payments: list[schemas.Payment]):
    df = pd.DataFrame(columns=["Fecha", "Cliente", "Monto", "Proveedor"])
    for p in payments:
        client = crud.get_client(db, p.cliente_id)
        provider = crud.get_provider(db, p.proveedor_id)
        df.loc[p._id] = [p.fecha, client.nombre, p.monto, provider.nombre]
    return df


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"Data": "Testing"}


@app.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db=db, client=client)


@app.get("/clients/", response_model=list[schemas.Client])
def get_clients(db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=0, limit=1000)
    return clients


@app.get("/clients/{client_id}", response_model=schemas.Client)
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@app.post("/providers/", response_model=schemas.Provider)
def create_provider(provider: schemas.ProviderCreate, db: Session = Depends(get_db)):
    return crud.create_provider(db=db, provider=provider)


@app.get("/providers/", response_model=list[schemas.Provider])
def get_providers(db: Session = Depends(get_db)):
    providers = crud.get_providers(db, skip=0, limit=1000)
    return providers


@app.get("/providers/{provider_id}", response_model=schemas.Provider)
def get_provider_by_id(provider_id: int, db: Session = Depends(get_db)):
    db_provider = crud.get_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider

@app.get("/payments/")
def download_excel(db: Session = Depends(get_db)):
    try:
        payments = crud.get_payments(db, skip=0, limit=1000)
        generate_excel_payments(db, payments)
        return FileResponse(path="Pagos.xlsx", filename="Pagos.xlsx", media_type="multipart/form-data")
    except:
        raise HTTPException(400, detail="Error in generating excel")

@app.get("/payments-total/")
def get_total(db: Session = Depends(get_db)):
    try:
        payments = crud.get_payments(db, skip=0, limit=1000)
        df = get_dataframe(db, payments)
        total = round(df["Monto"].sum(), 2)
        return {"Data": f"La suma total de los pagos es: {total}"}
    except:
        raise HTTPException(400, detail="Error in calculating total")

@app.post("/payments/")
async def upload_payments(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != mime_type:
        raise HTTPException(400, detail="Invalid document type. File must be .xlsx")
    with open(file_name, "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)
    data = validate_data(file_name)
    if type(data) == dict:
        return data
    upload_to_db(db, data)
    return {"Data" : f"'{file.filename}' Uploaded Successfully!"}

