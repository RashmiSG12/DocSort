from transformers import pipeline

# Load zero-shot classifier (only once)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Predefined labels
LABELS = ["Educational notes", "Academic certificate", "Electricity or shopping bill", "Miscellaneous document"]

LABEL_MAP = {
    "Educational notes": "notes",
    "Academic certificate": "certificates",
    "Electricity or shopping bill": "bills",
    "Miscellaneous document": "others"
}


def classify_text_zero_shot(text: str) -> str:
    if not text.strip():
        return "others"
    
    result = classifier(text, LABELS)
    top_label = result["labels"][0]
    return LABEL_MAP.get(top_label, "others")  # top predicted label
