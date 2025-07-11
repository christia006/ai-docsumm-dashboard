from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    original_text = Column(Text)
    summary = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi untuk NER dan Keyword
    entities = relationship("NamedEntity", back_populates="document")
    keywords = relationship("Keyword", back_populates="document")

class NamedEntity(Base):
    __tablename__ = "named_entities"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    entity_text = Column(String)
    entity_type = Column(String) # e.g., PERSON, DATE, ORGANIZATION

    document = relationship("Document", back_populates="entities")

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    keyword_text = Column(String)
    score = Column(Integer) # Atau float, tergantung metode ekstraksi

    document = relationship("Document", back_populates="keywords")