from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List, Dict, Any
from Models.models import Curso
from Database.database import db 

router = APIRouter()

@router.post("/cursos", response_model=Curso)
async def criar_curso(curso: Curso):
    curso_dict = curso.dict(by_alias=True, exclude={"id"})
    
    novo_curso = await db.cursos.insert_one(curso_dict)
    
    curso_criado = await db.cursos.find_one({"_id": novo_curso.inserted_id})
    
    if not curso_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar curso")

    # Converte o `_id` do MongoDB para string antes de retornar
    curso_criado["_id"] = str(curso_criado["_id"])

    return curso_criado



@router.get("/cursos/{curso_id}", response_model=Curso)
async def buscar_cursos_por_id(curso_id: str) -> Dict[str, Any]:
    filtro = {"_id": ObjectId(curso_id)} if ObjectId.is_valid(curso_id) else {"_id": curso_id}

    curso = await db.cursos.find_one(filtro)

    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    curso["_id"] = str(curso["_id"])

    if "modulos" in curso and isinstance(curso["modulos"], list):
        curso["modulos"] = [str(modulo_id) if isinstance(modulo_id, ObjectId) else modulo_id for modulo_id in curso["modulos"]]

    return curso

@router.get("/cursos", response_model=List[Curso])
async def listar_curso():
    cursos = await db.cursos.find().to_list(None)
    
    for curso in cursos:
        curso["_id"] = str(curso["_id"])
        
        # Converte os IDs dos cursos para string, se existirem
        if "categoria" in curso and isinstance(curso["categoria"], list):
            curso["categoria"] = [str(id) if isinstance(id, ObjectId) else id for id in curso["categoria"]]

    return cursos



@router.put("/cursos/{curso_id}", response_model=Curso)
async def atualizar_curso(curso_id: str, curso: Curso):
    if not ObjectId.is_valid(curso_id):
        raise HTTPException(status_code=400, detail="Id inválido")
    
    curso_dict = curso.model_dump(by_alias=True, exclude={"id"})
     
    resultado = await db.cursos.update_one({"_id": ObjectId(curso_id)}, {"$set" : curso_dict})
    
    if resultado.matched_count == 0:
        raise HTTPException (status_code=404, detail="Curso não encontrado")
    
    curso_atualizado = await db.cursos.find_one({"_id": ObjectId(curso_id)})
    curso_atualizado["_id"] = str(curso_atualizado["_id"])
    
    return curso_atualizado

@router.delete("/cursos/{curso_id}", status_code=200)
async def excluir_curso(curso_id: str):
    if not ObjectId.is_valid(curso_id):
        raise HTTPException(status_code=400, detail="ID de curso inválido")
    
    curso_obj_id = ObjectId(curso_id)
    
    curso = await db.cursos.find_one({"_id": curso_obj_id})
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    
    delete_resultado = await db.cursos.delete_one({"_id": curso_obj_id})
    if delete_resultado.deleted_count ==0:
        raise HTTPException(status_code=500, detail="Erro ao excluir curso")
    
    
    return {"messagem": "Curso excluido"}

