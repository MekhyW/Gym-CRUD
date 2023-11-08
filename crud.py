from sqlalchemy.orm import Session

import models
import schemas

###############
#MEMBROS
###############

def get_membros(db: Session):
    return db.query(models.Membros)

def get_membro_id(db : Session, id_membro : int):
    return db.query(models.Membros).filter(models.Membros.id_membro == id_membro).first()

def get_membro_celular(db : Session, celular : int):
    return db.query(models.Membros).filter(models.Membros.celular == celular).first()

def crate_membro(db : Session, membro: schemas.MembrosCreate):
    db_membro = models.Membros(nome = membro.nome, sobrenome = membro.sobrenome, celular = membro.celular)
    db.add(db_membro)
    db.commit()
    db.refresh(db_membro)
    return db_membro

def update_membro (db : Session, membro: schemas.MembrosBase):
    db_membro = db.query(models.Membros).filter(models.Membros.id_membro == membro.id_membro).first()
    if membro.nome:
        db_membro.nome = membro.nome
    if membro.sobrenome:
        db_membro.sobrenome = membro.sobrenome
    if membro.celular:
        db_membro.celular = membro.celular
    db.commit()
    db.refresh(db_membro)
    return db_membro

def delete_membro (db : Session, id_membro: int):
    db_membro = db.query(models.Membros).filter(models.Membros.id_membro == id_membro).first()
    db.delete(db_membro)
    db.commit()
    return {'Deletado': db_membro}


###############
#PLANOS
###############

def get_planos(db: Session):
    return db.query(models.Planos)

def get_planos_id(db : Session, id_plano : int):
    return db.query(models.Planos).filter(models.Planos.id_plano == id_plano).first()

def get_planos_nome(db : Session, nome : str):
    return db.query(models.Planos).filter(models.Planos.nome == nome).first()

def create_plano(db :Session, plano: schemas.PlanosCreate):
    db_plano = models.Planos(nome = plano.nome, preco = plano.preco )
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano

def update_plano (db : Session, plano: schemas.PlanosBase):
    db_plano = db.query(models.Planos).filter(models.Planos.id_plano == plano.id_plano).first()
    if plano.nome:
        db_plano.nome = plano.nome
    if plano.preco:
        db_plano.preco = plano.preco
    db.commit()
    db.refresh(db_plano)
    return db_plano

def delete_plano (db : Session, id_plano: int):
    db_plano= db.query(models.Planos).filter(models.Planos.id_plano == id_plano).first()
    db.delete(db_plano)
    db.commit()
    return {'Deletado': db_plano}


###############
#ASSINATURAS (MEMBRO-PLANO)
###############

def get_assinaturas(db: Session):
    return db.query(models.Assinaturas)

def get_assinatura_id(db : Session, id_assinatura : int):
    return db.query(models.Assinaturas).filter(models.Assinaturas.id_assinatura == id_assinatura).first()

def create_assinatura(db :Session, assinatura: schemas.AssinaturasCreate):
    db_assinatura = models.Assinaturas(ativo = assinatura.ativo, data_ativacao = assinatura.data_ativacao, id_membro = assinatura.id_membro, id_plano = assinatura.id_plano )
    db.add(db_assinatura)
    db.commit()
    db.refresh(db_assinatura)
    return db_assinatura

def update_assinatura (db : Session, assinatura: schemas.Assinaturas):
    db_assinatura = db.query(models.Assinaturas).filter(models.Assinaturas.id_assinatura == assinatura.id_assinatura).first()
    if assinatura.ativo is not None:
        db_assinatura.ativo = assinatura.ativo
    if assinatura.data_ativacao:
        db_assinatura.data_ativacao = assinatura.data_ativacao
    if assinatura.id_membro:
        db_assinatura.id_membro = assinatura.id_membro
    if assinatura.id_plano:
        db_assinatura.id_plano = assinatura.id_plano
    db.commit()
    db.refresh(db_assinatura)
    return db_assinatura

def delete_assinaturas (db : Session, id_assinatura: int):
    db_assinaturas= db.query(models.Assinaturas).filter(models.Assinaturas.id_assinatura == id_assinatura).first()
    db.delete(db_assinaturas)
    db.commit()
    return {'Deletado': db_assinaturas}
