from transformers import pipeline

class NamedEntityRecognizer:
    def __init__(self, model_name="dslim/bert-base-NER"):
        self.ner_pipeline = pipeline("ner", model=model_name, grouped_entities=True)

    def extract_entities(self, text: str) -> list:
        entities = self.ner_pipeline(text)
        # Format ulang output agar lebih mudah disimpan
        formatted_entities = []
        for entity in entities:
            formatted_entities.append({
                "entity_text": entity['word'],
                "entity_type": entity['entity_group'] # Opsi lain: entity['entity']
            })
        return formatted_entities