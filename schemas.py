from pydantic import BaseModel
from datetime import date, datetime, timedelta
from typing import Optional, List

# Client Schemas
class ClientCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: str
    registration_date: date
    club_driver: bool = False


class ClientResponse(BaseModel):
    client_id: int
    name: str
    phone: Optional[str]
    email: str
    registration_date: date
    club_driver: bool

    class Config:
        orm_mode = True


# Booking Schemas
class BookingCreate(BaseModel):
    booking_datetime: datetime
    booking_type: str
    client_id: int


class BookingResponse(BaseModel):
    booking_id: int
    booking_datetime: datetime
    booking_type: str
    client_id: int

    class Config:
        orm_mode = True


# Race Schemas
class RaceCreate(BaseModel):
    race_datetime: datetime
    participant_count: int
    duration: timedelta


class RaceResponse(BaseModel):
    race_id: int
    race_datetime: datetime
    participant_count: int
    duration: timedelta

    class Config:
        orm_mode = True


# Kart Schemas
class KartCreate(BaseModel):
    brand: str
    technical_condition: str
    last_maintenance_date: Optional[date] = None


class KartResponse(BaseModel):
    kart_id: int
    brand: str
    technical_condition: str
    last_maintenance_date: Optional[date]

    class Config:
        orm_mode = True


# RaceResult Schemas
class RaceResultCreate(BaseModel):
    race_datetime: datetime
    race_position: Optional[int] = None
    client_id: int
    race_id: int
    kart_id: int


class RaceResultResponse(BaseModel):
    result_id: int
    race_datetime: datetime
    race_position: Optional[int]
    client_id: int
    race_id: int
    kart_id: int

    class Config:
        orm_mode = True


# LapTime Schemas
class LapTimeCreate(BaseModel):
    result_id: int
    lap_time: timedelta
    lap_number: int


class LapTimeResponse(BaseModel):
    lap_time_id: int
    result_id: int
    lap_time: timedelta
    lap_number: int

    class Config:
        orm_mode = True


# Maintenance Schemas
class MaintenanceCreate(BaseModel):
    maintenance_date: date
    work_description: Optional[str] = None
    kart_id: int


class MaintenanceResponse(BaseModel):
    maintenance_id: int
    maintenance_date: date
    work_description: Optional[str]
    kart_id: int

    class Config:
        orm_mode = True