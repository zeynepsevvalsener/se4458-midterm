from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, constr, EmailStr
from pydantic.generics import GenericModel
from datetime import date
from pydantic import BaseModel, ConfigDict

DataT = TypeVar("DataT")
class Response(GenericModel, Generic[DataT]):
    status: str
    message: str
    data: Optional[DataT]

class FlightBase(BaseModel):
    date_from: date
    date_to: date
    airport_from: str
    airport_to: str
    duration: int
    capacity: int

class FlightCreate(FlightBase): pass

class FlightOut(FlightBase):
    id: int
    remaining_seats: int
    model_config = ConfigDict(from_attributes=True)

class TicketCreate(BaseModel):
    flight_id: int
    passenger_name: str

class TicketOut(BaseModel):
    ticket_number: str
    model_config = ConfigDict(from_attributes=True)

class CheckIn(BaseModel):
    flight_id: int
    passenger_name: str

class PassengerSeat(BaseModel):
    passenger_name: str
    seat: str
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class LoginForm(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

