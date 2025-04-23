from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, services
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/v1/flights", tags=["flights"])

@router.post("", response_model=schemas.Response[schemas.FlightOut])
def create_flight(f_in: schemas.FlightCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    flight = services.add_flight(db, f_in)
    return schemas.Response(status="success", message="Flight created", data=schemas.FlightOut.from_orm(flight))

@router.get("", response_model=schemas.Response[list[schemas.FlightOut]])
def get_flights(date_from: str, date_to: str, airport_from: str, airport_to: str, skip: int=0, limit: int=10, db: Session=Depends(get_db)):
    flights = services.query_flights(db, skip, limit, date_from=date_from, date_to=date_to, airport_from=airport_from, airport_to=airport_to)
    out = [schemas.FlightOut.from_orm(f) for f in flights]
    return schemas.Response(status="success", message="Flights fetched", data=out)
