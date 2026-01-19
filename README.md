# Bias Detector
A Django-based web application that detects **linguistic bias in news articles** using a fine-tuned transformer model.  
The system analyzes article text sentence-by-sentence and classifies it into one of four custom bias categories derived from modern media-literacy frameworks.

The project integrates **web scraping**, **natural language processing**, and **interactive frontend tooling** to provide an accessible interface for analyzing bias in online news sources.

---

## Overview
Bias Detector allows users to enter the URL of a news article.  
The application:

1. **Fetches and parses the article** using `newspaper3k`
2. **Splits the article into sentences** with NLTK
3. **Runs each sentence through a fine-tuned DistilBERT model**
4. **Aggregates all predictions** and selects the majority category
5. **Displays the final predicted bias label** to the user

This produces a simple, interpretable classification that reflects the dominant linguistic tone or bias present in the text.

## Bias Categories
Based on the model’s training and the label mapping in the code, articles are classified into exactly **one** of the following:

- **0 — Neutral**  
- **1 — Nationalistic Bias**  
- **2 — Sensationalism / Emotional Language**  
- **3 — Religious / Cultural Bias**

These labels are assigned via `predict_bias()` in `views.py`, which performs a majority-vote over per-sentence predictions.

## Key Features

### 🔍 Article URL Analysis
- Users input a **URL**, not raw text  
- The backend:
  - validates the URL  
  - fetches the page  
  - extracts title + article text  
  - returns a clean JSON response  

### 🧠 Transformer-Based NLP (DistilBERT)
- Loaded once at server start via:
  ```python
  tokenizer = AutoTokenizer.from_pretrained("bias_model")
  model = AutoModelForSequenceClassification.from_pretrained("bias_model")
  ```
- Per-sentence inference with:
  - tokenization  
  - truncation to 512 tokens  
  - padding  
  - softmax → `argmax` for final label  
- **No confidence score is shown** — only the final category label

### 🧮 Majority-Vote Classification
For each sentence:
```
prediction = argmax(model(sentence))
```
Then:
```
most_common_label = Counter(predictions).most_common(1)
```

### 🎨 Interactive Frontend UI
Included JavaScript logic (`detect.js`, `layout.js`) supports:
- smooth, animated UI transitions  
- dynamic response rendering
- JavaScript handles:
  - submitting the URL
  - disabling button during analysis
  - displaying results dynamically
  - toggling article text visibility

## Architecture

```
biasdetector/
│   views.py              → NLP inference + analysis API
│   models.py             → feedback model (optional)
│   static/biasdetector/  → JS, SVG assets
│   templates/            → HTML UI
│
biasdetection/            → Django project configuration
│   settings.py
│   urls.py
│
manage.py                 → Django management script
distilbert.py             → (placeholder for model wrapper; currently included in views.py)
db.sqlite3                → local database
```

**Main workflow:**

1. Frontend sends POST → `/api/analyze/`  
2. Django fetches article → parses text  
3. `predict_bias(text)` called  
4. JSON returned to JS  
5. UI updates with:
   - article title  
   - predicted bias  
   - “Show text” toggle  

## Installation

Requires **Python 3.9+**.

```bash
git clone https://github.com/shrisay/bias-detector
cd bias-detector
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download NLTK data (first run only):

```python
import nltk
nltk.download('punkt')
```

Run database migrations:

```bash
python manage.py migrate
```

Start server:

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

## Usage

1. Go to **“Bias Detector”** page  
2. Enter a valid article URL  
3. Wait for analysis  
4. View:
   - **Predicted Bias Category**
   - Article title
   - (Optional) full article text toggle

Example JSON returned by the backend:

```json
{
  "title": "Sample News Article",
  "text": "Full article text here...",
  "url": "https://example.com",
  "bias": "Nationalistic Bias"
}
```

---

## Future Improvements
- Add confidence scores or distribution over all categories  
- Highlight biased sentences using token-level attention  
- Support raw text input (not only URLs)  
- Extend categories to include more nuanced biases  
- Move NLP logic into a dedicated `distilbert.py` module  
- Deploy on Render / Vercel / Docker  

---

## Example
An example output is included in the repository as a text file.

