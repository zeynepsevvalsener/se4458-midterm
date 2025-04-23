from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from .database import init_db
from .routers import auth, flights, tickets

app = FastAPI(title="Airline Ticketing API", version="v1")
init_db()
app.include_router(auth.router)
app.include_router(flights.router)
app.include_router(tickets.router)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"status":"error","message":exc.detail,"data":None})

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"status":"error","message":str(exc),"data":None})