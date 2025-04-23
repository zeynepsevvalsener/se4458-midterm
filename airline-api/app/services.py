from sqlalchemy.orm import Session
from .models import Flight, Ticket, User
from .security import get_password_hash, verify_password, create_access_token
from .schemas import FlightCreate, TicketCreate, CheckIn, UserCreate, LoginForm, PassengerSeat
import uuid

# Flight services

def add_flight(db: Session, flight_in: FlightCreate) -> Flight:
    flight = Flight(**flight_in.dict())
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight

def query_flights(db: Session, skip: int, limit: int, **filters) -> list[Flight]:
    q = db.query(Flight)
    for attr, val in filters.items(): q = q.filter(getattr(Flight, attr) == val)
    return q.offset(skip).limit(limit).all()

# Ticket services

def buy_ticket(db: Session, ticket_in: TicketCreate) -> Ticket:
    flight = db.get(Flight, ticket_in.flight_id)
    sold = db.query(Ticket).filter_by(flight_id=flight.id).count()
    if sold >= flight.capacity: raise ValueError("Sold out")
    ticket = Ticket(flight_id=flight.id, passenger_name=ticket_in.passenger_name, ticket_number=str(uuid.uuid4()))
    db.add(ticket); db.commit(); db.refresh(ticket)
    return ticket

def check_in(db: Session, data: CheckIn) -> Ticket:
    ticket = db.query(Ticket).filter_by(flight_id=data.flight_id, passenger_name=data.passenger_name).first()
    if not ticket or ticket.checked_in: raise ValueError("Check-in failed")
    seat_no = f"S{db.query(Ticket).filter_by(flight_id=data.flight_id).count()}"
    ticket.checked_in = seat_no; db.commit()
    return ticket


def list_passengers(db: Session, flight_id: int, skip: int, limit: int) -> list[PassengerSeat]:
    rows = db.query(Ticket).filter_by(flight_id=flight_id).offset(skip).limit(limit).all()
    return [PassengerSeat(passenger_name=t.passenger_name, seat=t.checked_in or "") for t in rows]

# User services

def register_user(db: Session, user_in: UserCreate) -> User:
    exists = db.query(User).filter((User.username == user_in.username) | (User.email == user_in.email)).first()
    if exists: raise ValueError("Username or email already registered")
    hashed = get_password_hash(user_in.password)
    user = User(username=user_in.username, email=user_in.email, hashed_password=hashed)
    db.add(user); db.commit(); db.refresh(user)
    return user

def login_user(db: Session, form_data: LoginForm) -> str:
    user = db.query(User).filter((User.username == form_data.username) | (User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password): raise ValueError("Invalid credentials")
    return create_access_token({"sub": user.username})
