from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from fastapi import HTTPException

class DocumentSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.max_char_length = 4000  # chunk size

    def _summarize_chunk(self, text_chunk: str) -> str:
        inputs = self.tokenizer(
            text_chunk,
            max_length=self.tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)
        summary_ids = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=150,
            min_length=30,
            num_beams=4,
            early_stopping=True
        )
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    def summarize(self, text: str) -> str:
        if len(text) <= self.max_char_length:
            return self._summarize_chunk(text)

        chunks = [text[i:i+self.max_char_length] for i in range(0, len(text), self.max_char_length)]
        summaries = []
        for idx, chunk in enumerate(chunks):
            try:
                summaries.append(self._summarize_chunk(chunk))
            except Exception as e:
                print(f"Failed to summarize chunk {idx}: {e}")
        return " ".join(summaries).strip()
