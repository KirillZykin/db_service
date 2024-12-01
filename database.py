from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey,
    Interval,
    Text,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship

DATABASE_URL = "postgresql://postgres:53227172@localhost/db_karting"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Client(Base):
    __tablename__ = "client"

    client_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=False)
    registration_date = Column(Date, nullable=False)
    club_driver = Column(Boolean, default=False)

    bookings = relationship("Booking", back_populates="client", cascade="all, delete-orphan")
    race_results = relationship("RaceResult", back_populates="client", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True, index=True)
    booking_datetime = Column(TIMESTAMP, nullable=False)
    booking_type = Column(String(50), nullable=False)
    client_id = Column(Integer, ForeignKey("client.client_id", ondelete="CASCADE"), nullable=False)

    client = relationship("Client", back_populates="bookings")


class Race(Base):
    __tablename__ = "race"

    race_id = Column(Integer, primary_key=True, index=True)
    race_datetime = Column(TIMESTAMP, nullable=False)
    participant_count = Column(Integer, nullable=False)
    duration = Column(Interval, nullable=False)

    race_results = relationship("RaceResult", back_populates="race", cascade="all, delete-orphan")


class Kart(Base):
    __tablename__ = "kart"

    kart_id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False)
    technical_condition = Column(String(100), nullable=False)
    last_maintenance_date = Column(Date, nullable=True)

    race_results = relationship("RaceResult", back_populates="kart", cascade="all, delete-orphan")
    maintenances = relationship("Maintenance", back_populates="kart", cascade="all, delete-orphan")


class RaceResult(Base):
    __tablename__ = "race_result"

    result_id = Column(Integer, primary_key=True, index=True)
    race_datetime = Column(TIMESTAMP, nullable=False)
    race_position = Column(Integer, nullable=True)
    client_id = Column(Integer, ForeignKey("client.client_id", ondelete="CASCADE"), nullable=False)
    race_id = Column(Integer, ForeignKey("race.race_id", ondelete="CASCADE"), nullable=False)
    kart_id = Column(Integer, ForeignKey("kart.kart_id", ondelete="CASCADE"), nullable=False)

    client = relationship("Client", back_populates="race_results")
    race = relationship("Race", back_populates="race_results")
    kart = relationship("Kart", back_populates="race_results")
    lap_times = relationship("LapTime", back_populates="race_result", cascade="all, delete-orphan")


class LapTime(Base):
    __tablename__ = "lap_time"

    lap_time_id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("race_result.result_id", ondelete="CASCADE"), nullable=False)
    lap_time = Column(Interval, nullable=False)
    lap_number = Column(Integer, nullable=False)

    race_result = relationship("RaceResult", back_populates="lap_times")


class Maintenance(Base):
    __tablename__ = "maintenance"

    maintenance_id = Column(Integer, primary_key=True, index=True)
    maintenance_date = Column(Date, nullable=False)
    work_description = Column(Text, nullable=True)
    kart_id = Column(Integer, ForeignKey("kart.kart_id", ondelete="CASCADE"), nullable=False)

    kart = relationship("Kart", back_populates="maintenances")