from datetime import date
from typing import Optional, List
from uuid import UUID, uuid4

from fastapi import FastAPI
from pydantic import BaseModel, constr, Field


class PersonBase(BaseModel):
    apelido: constr(max_length=32)
    nome: constr(max_length=100)
    nascimento: date
    stack: Optional[List[str]] = None

    @property
    def stack(self) -> str:
        return " ".join(self.stack) if self.stack else None


class PerssonCreate(PersonBase):
    id: UUID = Field(default_factory=uuid4)


app = FastAPI()


@app.post("/pessoas")
async def create_person(person: PersonBase):
    return {"message": "Hello World"}


@app.get("/pessoas/{id}")
async def get_person(id):
    return {"message": "Hello World"}


@app.get("/pessoas")
async def get_persons_by_term(t: str | None = None):
    return {"message": "Hello World"}


@app.get("/contagem-pessoas")
async def count_persons():
    return {"message": "Hello World"}
