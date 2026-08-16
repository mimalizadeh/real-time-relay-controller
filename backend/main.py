from fastapi import FastAPI

from src.routes import relay

app = FastAPI(
    title="Real time relay controller",
    description="Real time relay controller"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(relay.router)
