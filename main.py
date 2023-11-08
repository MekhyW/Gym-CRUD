from fastapi import Depends,FastAPI, Request, status, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from database import SessionLocal, engine
import crud
import schemas
import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Página Inicial"])
async def projeto_descricao():
    return {"message": "Bem-vindo ao projeto da academia. Este é um sistema de gerenciamento de membros, planos e assinaturas."}


###############
#MEMBROS
###############

@app.get("/membros/", response_model=list[schemas.MembrosBase], status_code=200, tags=["Membros"], 
         description="Retorna a lista de todos os membros, com seus respectivos atributos")
async def get_membros(db : Session = Depends(get_db)):
    membros = crud.get_membros(db)
    return membros

@app.get("/membros/{id_membro}", response_model=schemas.MembrosBase, status_code=200, tags=["Membros"], 
         description="Retorna um membro pelo seu ID")
async def get_membro_id(id_membro: int = Path(..., title="ID do membro"), db : Session = Depends(get_db)):
    db_membro = crud.get_membro_id(db, id_membro=id_membro)
    if db_membro is None:
        raise HTTPException(status_code=422, detail="Membro não encontrado")
    return db_membro

@app.post("/membros/create", response_model=schemas.MembrosBase, status_code=201, tags=["Membros"],
          description="Adiciona mais um membro novo na base")
async def create_membros(membro: schemas.MembrosCreate, db : Session = Depends(get_db)):
    db_membro = crud.get_membro_celular(db, celular=membro.celular)
    if db_membro:
        raise HTTPException(status_code=400, detail="Membro ja registrado")
    return crud.crate_membro(db=db, membro=membro)

@app.put("/membros/update/{id_membro}", status_code=200, tags=["Membros"],
         description="Atualiza um membro existente na base")
async def update_membros(membro: schemas.MembrosBase, db : Session = Depends(get_db)):
    db_membro = crud.update_membro(db, membro = membro)
    return db_membro

@app.delete("/membros/delete/{id_membro}", status_code=202, tags=["Membros"],
            description="Deleta um membro existente na base")
async def delete_membros(id_membro : int , db: Session = Depends(get_db) ):
    db_membro = crud.get_membro_id(db, id_membro= id_membro)
    if db_membro is None:
        raise HTTPException(status_code=422, detail="Membro não encontrado")
    return crud.delete_membro(db, id_membro=id_membro)


###############
#PLANOS
###############

@app.get("/planos/", response_model=list[schemas.PlanosBase], status_code=200, tags=["Planos"],
         description="Retorna a lista de todos os planos, com seus respectivos atributos")
async def get_planos(db : Session = Depends(get_db)):
    planos = crud.get_planos(db)
    return planos

@app.get("/planos/{id_plano}", response_model=schemas.PlanosBase, status_code=200, tags=["Planos"],
         description="Retorna um plano pelo seu ID")
async def get_plano_id(id_plano: int = Path(..., title="ID do plano"), db : Session = Depends(get_db)):
    db_plano = crud.get_planos_id(db, id_plano=id_plano)
    if db_plano is None:
        raise HTTPException(status_code=422, detail="Plano não encontrado")
    return db_plano

@app.post("/planos/create", response_model=schemas.PlanosCreate, status_code=201, tags=["Planos"],
          description="Adiciona mais um plano novo na base")
async def create_planos(plano: schemas.PlanosCreate, db: Session = Depends(get_db)):
    db_plano = crud.get_planos_nome (db, nome = plano.nome)
    if db_plano:
        raise HTTPException(status_code=400, detail="Plano ja registrado")    
    return crud.create_plano(db, plano=plano)

@app.put("/planos/update/{id_plano}", status_code=200, tags=["Planos"],
         description="Atualiza um plano existente na base")
async def update_planos(plano : schemas.PlanosBase, db : Session = Depends(get_db)):
    db_plano = crud.update_plano(db, plano=plano)
    return db_plano

@app.delete("/planos/delete/{id_plano}", status_code=202, tags=["Planos"],
            description="Deleta um plano existente na base")
async def delete_planos(id_plano: int, db: Session = Depends(get_db)):
    db_plano = crud.get_planos_id(db, id_plano = id_plano)
    if db_plano is None:
        raise HTTPException(status_code=422, detail="Plano não encontrado")
    return crud.delete_plano(db , id_plano=id_plano)


###############
#ASSINATURAS (MEMBRO-PLANO)
###############

@app.get("/assinaturas/", response_model=list[schemas.AssinaturasBase], status_code=200, tags=["Assinaturas"],
         description="Retorna a lista de todas as assinaturas, com seus respectivos atributos")
async def get_assinaturas(db : Session = Depends(get_db)):
    assinaturas = crud.get_assinaturas(db)
    return assinaturas


@app.get("/assinaturas/{id_assinatura}", response_model=schemas.Assinaturas, status_code=200, tags=["Assinaturas"],
         description="Retorna uma assinatura pelo seu ID")
async def get_assinatura_id(id_assinatura: int = Path(..., title="ID da assinatura"), db : Session = Depends(get_db)):
    db_assinatura = crud.get_assinatura_id(db , id_assinatura=id_assinatura)
    if db_assinatura is None:
        raise HTTPException(status_code=422, detail="Assinatura não encontrada")
    return db_assinatura

@app.post("/assinaturas/create", response_model=schemas.Assinaturas, status_code=201, tags=["Assinaturas"],
          description="Adiciona mais uma assinatura nova na base")
async def create_assinaturas(assinatura: schemas.Assinaturas, db : Session = Depends(get_db)):
    db_assinaturas = crud.get_assinatura_id (db, id_assinatura=assinatura.id_assinatura)
    if db_assinaturas:
        raise HTTPException(status_code=400, detail="Assinatura ja registrado")
    return crud.create_assinatura(db, assinatura=assinatura)

@app.put("/assinaturas/update/{id_assinatura}", status_code=200, tags=["Assinaturas"],
         description="Atualiza uma assinatura existente na base")
async def update_assinatura( assinatura: schemas.Assinaturas, db : Session = Depends(get_db)):
    db_assinaturas = crud.update_assinatura(db, assinatura=assinatura)
    return db_assinaturas


@app.delete("/assinaturas/delete/{id_assinatura}", status_code=202, tags=["Assinaturas"],
            description="Deleta uma assinatura existente na base")
async def delete_assinatura(id_assinatura: int, db : Session = Depends(get_db)):
    db_assinaturas = crud.get_assinatura_id(db, id_assinatura= id_assinatura)
    if db_assinaturas is None:
        raise HTTPException(status_code=422, detail="Assinatura não encontrado")
    return crud.delete_assinaturas(db, id_assinatura=id_assinatura)


###############
#EXCEPTIONS
###############

#Exception para quando o cliente manda um body preenchido de forma errada
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
