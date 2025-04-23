from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, services
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/v1/tickets", tags=["tickets"])

def auth_dep():
    return Depends(get_current_user)

@router.post("", response_model=schemas.Response[schemas.TicketOut], status_code=status.HTTP_201_CREATED)
async def buy_ticket(
    ticket_in: schemas.TicketCreate,
    db: Session = Depends(get_db),
    username: str = auth_dep()
):
    try:
        ticket = services.buy_ticket(db, ticket_in)
        return schemas.Response(status="success", message="Ticket purchased", data=ticket)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/checkin", response_model=schemas.Response[schemas.PassengerSeat])
async def check_in(
    check_in_in: schemas.CheckIn,
    db: Session = Depends(get_db),
    
):
    try:
        passenger_seat = services.check_in(db, check_in_in)
        return schemas.Response(status="success", message="Check-in successful", data=passenger_seat)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/passengers", response_model=schemas.Response[list[schemas.PassengerSeat]])
async def passenger_list(
    flight_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    username: str = auth_dep()
):
    try:
        passengers = services.list_passengers(db, flight_id, skip, limit)
        return schemas.Response(status="success", message="Passenger list fetched", data=passengers)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))