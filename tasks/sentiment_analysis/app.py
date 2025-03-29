from transformers import pipeline

# Load sentiment analysis model (fine-tuned RoBERTa)
classifier = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")

# Read input text from mounted Docker volume
with open("/data/input.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Run sentiment classification
result = classifier(text)[0]
sentiment = result["label"]
confidence = round(result["score"] * 100, 2)

# Output standardized result
print(f"Sentiment: {sentiment.upper()} (Confidence: {confidence}%)")
