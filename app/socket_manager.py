import os
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
import socketio

SECRET_KEY = os.getenv("JWT_SECRET")
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


class SocketManager:
    def __init__(self, app: FastAPI):
        self.sio = socketio.ASGIApp(sio)
        app.mount("/socket.io", self.sio)
        self.setup_routes()

    def setup_routes(self):
        @sio.event
        async def connect(sid, environ):
            print(f"User {sid} connected")
            token = environ.get("HTTP_AUTHORIZATION")
           

            
            if not token:
                await sio.enter_room(sid,"123derg4ff4r4r")
                return
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                print(payload)
                idSpecificProduct = payload["idSpeceficProduct"]
                await sio.enter_room(sid, idSpecificProduct)
                print(f"User {idSpecificProduct} connected")
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

        @sio.event
        async def disconnect(sid):
            print(f"User {sid} disconnected")

        @sio.event
        async def message(sid, data):
            print(f"Message received from {sid}: {data}")
            await sio.emit('response', {'data': 'Server response'}, room=sid)