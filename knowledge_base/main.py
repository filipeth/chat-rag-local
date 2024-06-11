from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import endpoints as v1

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.router, prefix="/v1")

@app.get("/")
async def health_check() -> str:
    return "OK"
