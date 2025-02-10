import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Any
from Models.models import Aluno
from Database.database import get_db

router = APIRouter()

@router.post("/alunos", response_model=Aluno)
def criar_aluno(aluno: Aluno, db: Any = Depends(get_db)):
    aluno_data = aluno.model_dump(by_alias=True)

    result = db.alunos.insert_one(aluno_data)
    inserted_id = result.inserted_id

    aluno_data["_id"] = inserted_id
    aluno_data["id"] = str(inserted_id)

    return {"ok": "ok"}
