from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import database, schemas, crud
from database import engine, SessionLocal

# Создание таблиц
database.Base.metadata.create_all(bind=engine)

# Инициализация FastAPI
app = FastAPI()


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Routes for Client ---
@app.post("/clients/", response_model=schemas.ClientResponse)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db=db, client=client)


@app.get("/clients/", response_model=List[schemas.ClientResponse])
def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_clients(db=db, skip=skip, limit=limit)


@app.get("/clients/{client_id}", response_model=schemas.ClientResponse)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = crud.get_client(db=db, client_id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.delete("/clients/{client_id}", response_model=schemas.ClientResponse)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = crud.delete_client(db=db, client_id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# --- Routes for Booking ---
@app.post("/bookings/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)


@app.get("/bookings/", response_model=List[schemas.BookingResponse])
def read_bookings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_bookings(db=db, skip=skip, limit=limit)


@app.get("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = crud.get_booking(db=db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@app.delete("/bookings/{booking_id}", response_model=schemas.BookingResponse)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = crud.delete_booking(db=db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# --- Routes for Race ---
@app.post("/races/", response_model=schemas.RaceResponse)
def create_race(race: schemas.RaceCreate, db: Session = Depends(get_db)):
    return crud.create_race(db=db, race=race)


@app.get("/races/", response_model=List[schemas.RaceResponse])
def read_races(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_races(db=db, skip=skip, limit=limit)


@app.get("/races/{race_id}", response_model=schemas.RaceResponse)
def read_race(race_id: int, db: Session = Depends(get_db)):
    race = crud.get_race(db=db, race_id=race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race


@app.delete("/races/{race_id}", response_model=schemas.RaceResponse)
def delete_race(race_id: int, db: Session = Depends(get_db)):
    race = crud.delete_race(db=db, race_id=race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race


# --- Routes for Kart ---
@app.post("/karts/", response_model=schemas.KartResponse)
def create_kart(kart: schemas.KartCreate, db: Session = Depends(get_db)):
    return crud.create_kart(db=db, kart=kart)


@app.get("/karts/", response_model=List[schemas.KartResponse])
def read_karts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_karts(db=db, skip=skip, limit=limit)


@app.get("/karts/{kart_id}", response_model=schemas.KartResponse)
def read_kart(kart_id: int, db: Session = Depends(get_db)):
    kart = crud.get_kart(db=db, kart_id=kart_id)
    if not kart:
        raise HTTPException(status_code=404, detail="Kart not found")
    return kart


@app.delete("/karts/{kart_id}", response_model=schemas.KartResponse)
def delete_kart(kart_id: int, db: Session = Depends(get_db)):
    kart = crud.delete_kart(db=db, kart_id=kart_id)
    if not kart:
        raise HTTPException(status_code=404, detail="Kart not found")
    return kart


# --- Routes for RaceResult ---
@app.post("/race-results/", response_model=schemas.RaceResultResponse)
def create_race_result(result: schemas.RaceResultCreate, db: Session = Depends(get_db)):
    return crud.create_race_result(db=db, result=result)


@app.get("/race-results/", response_model=List[schemas.RaceResultResponse])
def read_race_results(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_race_results(db=db, skip=skip, limit=limit)


@app.get("/race-results/{result_id}", response_model=schemas.RaceResultResponse)
def read_race_result(result_id: int, db: Session = Depends(get_db)):
    result = crud.get_race_result(db=db, result_id=result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Race result not found")
    return result


@app.delete("/race-results/{result_id}", response_model=schemas.RaceResultResponse)
def delete_race_result(result_id: int, db: Session = Depends(get_db)):
    result = crud.delete_race_result(db=db, result_id=result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Race result not found")
    return result


# --- Routes for LapTime ---
@app.post("/lap-times/", response_model=schemas.LapTimeResponse)
def create_lap_time(lap_time: schemas.LapTimeCreate, db: Session = Depends(get_db)):
    return crud.create_lap_time(db=db, lap_time=lap_time)


@app.get("/lap-times/", response_model=List[schemas.LapTimeResponse])
def read_lap_times(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_lap_times(db=db, skip=skip, limit=limit)


@app.get("/lap-times/{lap_time_id}", response_model=schemas.LapTimeResponse)
def read_lap_time(lap_time_id: int, db: Session = Depends(get_db)):
    lap_time = crud.get_lap_time(db=db, lap_time_id=lap_time_id)
    if not lap_time:
        raise HTTPException(status_code=404, detail="Lap time not found")
    return lap_time


@app.delete("/lap-times/{lap_time_id}", response_model=schemas.LapTimeResponse)
def delete_lap_time(lap_time_id: int, db: Session = Depends(get_db)):
    lap_time = crud.delete_lap_time(db=db, lap_time_id=lap_time_id)
    if not lap_time:
        raise HTTPException(status_code=404, detail="Lap time not found")
    return lap_time


# --- Routes for Maintenance ---
@app.post("/maintenances/", response_model=schemas.MaintenanceResponse)
def create_maintenance(maintenance: schemas.MaintenanceCreate, db: Session = Depends(get_db)):
    return crud.create_maintenance(db=db, maintenance=maintenance)


@app.get("/maintenances/", response_model=List[schemas.MaintenanceResponse])
def read_maintenances(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_maintenances(db=db, skip=skip, limit=limit)


@app.get("/maintenances/{maintenance_id}", response_model=schemas.MaintenanceResponse)
def read_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = crud.get_maintenance(db=db, maintenance_id=maintenance_id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return maintenance


@app.delete("/maintenances/{maintenance_id}", response_model=schemas.MaintenanceResponse)
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = crud.delete_maintenance(db=db, maintenance_id=maintenance_id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return maintenance