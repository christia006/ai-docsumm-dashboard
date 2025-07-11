from transformers import pipeline
import torch

class DocumentSummarizer:
    def __init__(self):
        # Deteksi device otomatis (cuda jika ada, jika tidak pakai cpu)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Device set to: {self.device}")

        # Inisialisasi pipeline summarizer
        # Model facebook/bart-large-cnn cocok untuk summarization panjang
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0 if torch.cuda.is_available() else -1
        )

    def chunk_text(self, text, max_words=500):
        """
        Memecah teks panjang menjadi potongan (chunk) berisi max_words kata.
        """
        words = text.split()
        for i in range(0, len(words), max_words):
            yield " ".join(words[i:i+max_words])

    def summarize(self, text):
        """
        Summarize teks panjang: pecah jadi chunk, ringkas per chunk,
        lalu gabungkan hasil ringkasan jadi satu ringkasan panjang.
        """
        # Pecah teks panjang menjadi chunk kecil
        chunks = list(self.chunk_text(text, max_words=500))
        summaries = []

        for idx, chunk in enumerate(chunks):
            print(f"Summarizing chunk {idx+1}/{len(chunks)}...")
            summary_result = self.summarizer(
                chunk,
                max_length=150,   # Sesuaikan jika mau ringkasan lebih panjang
                min_length=50,
                do_sample=False
            )
            # Ambil hasil ringkasan dan tambahkan ke list
            summaries.append(summary_result[0]['summary_text'].strip())

        # Gabungkan semua ringkasan menjadi 1 teks seperti paragraf panjang
        final_summary = " ".join(summaries)
        return final_summary
