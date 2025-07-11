from sqlalchemy.orm import Session
from . import models
from ..schemas import document as schemas # Perbaikan: Import 'document' dari 'schemas' dan beri alias 'schemas'

def create_document(db: Session, doc_data: schemas.DocumentCreate):
    db_document = models.Document(
        filename=doc_data.filename,
        original_text=doc_data.original_text,
        summary=doc_data.summary
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()

def create_named_entity(db: Session, entity_data: schemas.NamedEntityCreate, document_id: int):
    db_entity = models.NamedEntity(**entity_data.dict(), document_id=document_id)
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity

def create_keyword(db: Session, keyword_data: schemas.KeywordCreate, document_id: int):
    db_keyword = models.Keyword(**keyword_data.dict(), document_id=document_id)
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword
