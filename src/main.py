from fastapi import FastAPI
import uvicorn

from api import auth, websocket


app = FastAPI()

app.include_router(auth.router)
app.include_router(websocket.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
