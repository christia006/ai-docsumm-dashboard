from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class NamedEntityBase(BaseModel):
    entity_text: str
    entity_type: str

class NamedEntityCreate(NamedEntityBase):
    pass

class NamedEntity(NamedEntityBase):
    id: int
    document_id: int

    class Config:
        orm_mode = True

class KeywordBase(BaseModel):
    keyword_text: str
    score: int

class KeywordCreate(KeywordBase):
    pass

class Keyword(KeywordBase):
    id: int
    document_id: int

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    filename: str
    original_text: str

class DocumentCreate(DocumentBase):
    summary: str

class Document(DocumentBase):
    id: int
    summary: str
    uploaded_at: datetime
    entities: List[NamedEntity] = []
    keywords: List[Keyword] = []

    class Config:
        orm_mode = True