# app/main.py
import os
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from app.api.v1.endpoints import stats
from app.api.v1.endpoints import statics
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import probability
from app.socket_manager import SocketManager
from app.core.security import JWTBearer
from app.database import engine,Base,SessionLocal
import threading
import socketio

from fastapi.security import OAuth2PasswordBearer 
from app.rabbitmq_consumer import start_rabbit_consumer
from contextlib import asynccontextmanager

load_dotenv()
app = FastAPI()


Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],


    
)

socket_manager = SocketManager(app)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize AuthJWT instance


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(stats.router, prefix="/api/v1/stats",dependencies=[Depends(JWTBearer())])
app.include_router(statics.router, prefix="/api/v1/statics",dependencies=[Depends(JWTBearer())])
app.include_router(probability.router, prefix="/api/v1/probability",dependencies=[Depends(JWTBearer())])

@asynccontextmanager
async def lifespan(app:FastAPI):
    thread=threading.Thread(target=start_rabbit_consumer)
    thread.start()
    yield
    thread.join()

    
# Incluye el middleware en la aplicación
app.router.lifespan_context = lifespan

# Incluye los endpoints





if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)




