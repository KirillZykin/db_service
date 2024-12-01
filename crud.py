from sqlalchemy.orm import Session
import database, schemas

def get_user_by_username(db: Session, username: str):
    return db.query(database.User).filter(database.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = database.User(username=user.username, hashed_password=user.hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Client CRUD
def create_client(db: Session, client: schemas.ClientCreate):
    db_client = database.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_clients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(database.Client).offset(skip).limit(limit).all()


def get_client(db: Session, client_id: int):
    return db.query(database.Client).filter(database.Client.client_id == client_id).first()


def update_client(db: Session, client_id: int, client: schemas.ClientCreate):
    db_client = get_client(db, client_id)
    if db_client:
        for key, value in client.dict().items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
    return db_client


def delete_client(db: Session, client_id: int):
    db_client = get_client(db, client_id)
    if db_client:
        db.delete(db_client)
        db.commit()
    return db_client


# Booking CRUD
def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = database.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_bookings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(database.Booking).offset(skip).limit(limit).all()


def get_booking(db: Session, booking_id: int):
    return db.query(database.Booking).filter(database.Booking.booking_id == booking_id).first()


def delete_booking(db: Session, booking_id: int):
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db.delete(db_booking)
        db.commit()
    return db_booking


# Race CRUD
def create_race(db: Session, race: schemas.RaceCreate):
    db_race = database.Race(**race.dict())
    db.add(db_race)
    db.commit()
    db.refresh(db_race)
    return db_race


def get_races(db: Session, skip: int = 0, limit: int = 10):
    return db.query(database.Race).offset(skip).limit(limit).all()


def get_race(db: Session, race_id: int):
    return db.query(database.Race).filter(database.Race.race_id == race_id).first()


def delete_race(db: Session, race_id: int):
    db_race = get_race(db, race_id)
    if db_race:
        db.delete(db_race)
        db.commit()
    return db_race


# Kart CRUD
def create_kart(db: Session, kart: schemas.KartCreate):
    db_kart = database.Kart(**kart.dict())
    db.add(db_kart)
    db.commit()
    db.refresh(db_kart)
    return db_kart


def get_karts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(database.Kart).offset(skip).limit(limit).all()


def get_kart(db: Session, kart_id: int):
    return db.query(database.Kart).filter(database.Kart.kart_id == kart_id).first()


def delete_kart(db: Session, kart_id: int):
    db_kart = get_kart(db, kart_id)
    if db_kart:
        db.delete(db_kart)
        db.commit()
    return db_kart


# RaceResult CRUD
def create_race_result(db: Session, result: schemas.RaceResultCreate):
    db_result = database.RaceResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_race_results(db: Session, skip: int = 0, limit: int = 10):
    return db.query(database.RaceResult).offset(skip).limit(limit).all()


def get_race_result(db: Session, result_id: int):
    return db.query(database.RaceResult).filter(database.RaceResult.result_id == result_id).first()


def delete_race_result(db: Session, result_id: int):
    db_result = get_race_result(db, result_id)
    if db_result:
        db.delete(db_result)
        db.commit()
    return db_result


# LapTime CRUD
def create_lap_time(db: Session, lap_time: schemas.LapTimeCreate):
    db_lap_time = database.LapTime(**lap_time.dict())
    db.add(db_lap_time)
    db.commit()
    db.refresh(db_lap_time)
    return db_lap_time


def get_lap_times(db: Session, skip: int = 0, limit: int = 10):
    return db.query(database.LapTime).offset(skip).limit(limit).all()


def get_lap_time(db: Session, lap_time_id: int):
    return db.query(database.LapTime).filter(database.LapTime.lap_time_id == lap_time_id).first()


def delete_lap_time(db: Session, lap_time_id: int):
    db_lap_time = get_lap_time(db, lap_time_id)
    if db_lap_time:
        db.delete(db_lap_time)
        db.commit()
    return db_lap_time


# Maintenance CRUD
def create_maintenance(db: Session, maintenance: schemas.MaintenanceCreate):
    db_maintenance = database.Maintenance(**maintenance.dict())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


def get_maintenances(db: Session, skip: int = 0, limit: int = 10):
    return db.query(database.Maintenance).offset(skip).limit(limit).all()


def get_maintenance(db: Session, maintenance_id: int):
    return db.query(database.Maintenance).filter(database.Maintenance.maintenance_id == maintenance_id).first()


def delete_maintenance(db: Session, maintenance_id: int):
    db_maintenance = get_maintenance(db, maintenance_id)
    if db_maintenance:
        db.delete(db_maintenance)
        db.commit()
    return db_maintenance