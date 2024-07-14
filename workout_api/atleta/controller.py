from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate
from workout_api.database import get_db
from workout_api.atleta.schemas import AtletaOut
from workout_api.atleta.models import Atleta

router = APIRouter()

@router.get("/", response_model=Page[AtletaOut])
async def get_atletas(
    nome: Optional[str] = Query(None, description="Nome do atleta"),
    cpf: Optional[str] = Query(None, description="CPF do atleta"),
    db: Session = Depends(get_db)
):
    query = db.query(Atleta)
    if nome:
        query = query.filter(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(Atleta.cpf == cpf)
    return paginate(query.all())

add_pagination(router)
