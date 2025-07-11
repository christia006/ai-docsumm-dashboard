from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class DocumentSummarizer:
    def __init__(self):
        # Pilih device otomatis
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Device set to: {self.device}")

        # Ganti model ke bart-large-cnn yang cocok untuk long document summarization
        model_name = "facebook/bart-large-cnn"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Pipeline summarizer
        self.summarizer = pipeline(
            "summarization",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )

        # Max input tokens yang aman (512 untuk BART)
        self.max_input_tokens = self.model.config.max_position_embeddings or 1024

    def chunk_text(self, text, max_tokens=500):
        """
        Memecah teks panjang jadi potongan chunk yang tokennya tidak melebihi max_tokens.
        """
        words = text.split()
        current_chunk = []
        current_len = 0

        for word in words:
            # Hitung panjang token perkiraan
            current_len += len(self.tokenizer.tokenize(word))
            if current_len >= max_tokens:
                yield " ".join(current_chunk)
                current_chunk = []
                current_len = 0
            current_chunk.append(word)

        if current_chunk:
            yield " ".join(current_chunk)

    def summarize(self, text):
        """
        Ringkas teks panjang: pecah jadi chunk, ringkas tiap chunk,
        lalu gabungkan hasil jadi paragraf panjang.
        """
        # Pecah jadi chunk dengan token <= max_input_tokens - buffer
        chunks = list(self.chunk_text(text, max_tokens=self.max_input_tokens - 10))
        summaries = []

        print(f"Total chunks: {len(chunks)}")

        for idx, chunk in enumerate(chunks):
            print(f"Summarizing chunk {idx+1}/{len(chunks)}...")
            # Sesuaikan max_length agar tidak melebihi config.max_length
            # BART biasanya config.max_length default 142, bisa diperbesar sedikit
            summary_result = self.summarizer(
                chunk,
                max_length=180,  # atur sesuai kebutuhan, <= config.max_length
                min_length=60,
                do_sample=False
            )
            summaries.append(summary_result[0]['summary_text'].strip())

        final_summary = " ".join(summaries)
        return final_summary
