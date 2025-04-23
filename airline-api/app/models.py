from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from typing import Optional

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, index=True)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    airport_from = Column(String, nullable=False)
    airport_to = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    tickets = relationship("Ticket", back_populates="flight")

    @property
    def remaining_seats(self) -> int:
        # capacity eksi satılmış bilet sayısı
        return self.capacity - len(self.tickets)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    passenger_name = Column(String, nullable=False)
    ticket_number = Column(String, unique=True, index=True)
    checked_in = Column(String, nullable=True)
    flight = relationship("Flight", back_populates="tickets")

    @property
    def seat(self) -> Optional[str]:
        return self.checked_in

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)