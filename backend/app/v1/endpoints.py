from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import io
from pypdf import PdfReader

from ...db.database import get_db
from ...db import crud, models
from ...schemas import document as schemas_doc
from ...ml.summarizer import DocumentSummarizer
from ...ml.ner import NamedEntityRecognizer
from ...ml.keyword_extractor import KeywordExtractor

router = APIRouter()

summarizer = DocumentSummarizer()
ner = NamedEntityRecognizer()
keyword_extractor = KeywordExtractor()

@router.post("/summarize-document/", response_model=schemas_doc.Document)
async def upload_and_summarize_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # --- DEBUGGING: Cetak tipe konten file yang diterima ---
    print(f"Received file content type: {file.content_type}")
    # --- AKHIR DEBUGGING ---

    original_text = ""
    filename = file.filename

    if file.content_type == "text/plain":
        original_text = (await file.read()).decode("utf-8")
    elif file.content_type == "application/pdf":
        try:
            pdf_bytes = await file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_file)
            
            for page in reader.pages:
                original_text += page.extract_text() + "\n"
            
            if not original_text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="PDF file contains no readable text or is empty."
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to process PDF file: {e}. Ensure it's a valid PDF."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Only plain text (.txt) and PDF (.pdf) are supported."
        )

    summary = summarizer.summarize(original_text)
    entities = ner.extract_entities(original_text)
    keywords = keyword_extractor.extract_keywords(original_text)

    doc_data = schemas_doc.DocumentCreate(
        filename=filename,
        original_text=original_text,
        summary=summary
    )
    db_document = crud.create_document(db=db, doc_data=doc_data)

    for entity_data in entities:
        crud.create_named_entity(db=db, entity_data=schemas_doc.NamedEntityCreate(**entity_data), document_id=db_document.id)

    for keyword_data in keywords:
        crud.create_keyword(db=db, keyword_data=schemas_doc.KeywordCreate(**keyword_data), document_id=db_document.id)

    db.refresh(db_document)
    return db_document

@router.get("/documents/", response_model=List[schemas_doc.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return documents

@router.get("/documents/{document_id}", response_model=schemas_doc.Document)
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document
