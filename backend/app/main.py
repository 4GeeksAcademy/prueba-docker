from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MESSAGES = [
    {"id": 1, "text": "Hola desde el contenedor de la API"},
    {"id": 2, "text": "Este JSON lo sirve FastAPI"},
    {"id": 3, "text": "Otro mensaje de ejemplo"}
]


@app.get("/messages")
def get_messages():
    return MESSAGES