from transformers import pipeline

# Load pre-trained summarization model (DistilBART fine-tuned on CNN/DailyMail)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Read input text from volume-mounted file (provided by orchestrator)
with open("/data/input.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Generate summary with defined length bounds
summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]

# Output the summary (captured by orchestrator as stdout)
print(summary)
