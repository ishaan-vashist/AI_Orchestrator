from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

with open("/data/input.txt", "r", encoding="utf-8") as f:
    text = f.read()

summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]

print(summary)
