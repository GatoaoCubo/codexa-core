# Knowledge Extraction Module | mentor_agent

**Purpose**: Content extraction from multiple file formats (RASCUNHO → raw text)
**Version**: 1.0.0 | **Updated**: 2025-11-18

---

## 🎯 OVERVIEW

First stage of the 4-stage knowledge processing pipeline. Extracts raw content from diverse file formats into clean, structured text ready for classification.

**Pipeline Position**: Extract → Classify → Synthesize → Validate

---

## 📥 SUPPORTED FILE FORMATS

### Text Documents
- **PDF** (.pdf) - Priority format for guides/ebooks
- **Markdown** (.md) - Already structured content
- **Text** (.txt) - Plain text notes
- **Word** (.docx) - Documents from sellers
- **HTML** (.html) - Web pages/blog posts

### Structured Data
- **JSON** (.json) - API responses, structured data
- **CSV** (.csv) - Spreadsheet data, product catalogs
- **Excel** (.xlsx) - Reports, tables, data analysis

### Media
- **Video** (.mp4, .mov, .avi) - Tutorials, courses (extract transcript)
- **Audio** (.mp3, .wav, .m4a) - Podcasts, voice notes (transcribe)
- **Images** (.png, .jpg, .jpeg) - Screenshots, infographics (OCR)

---

## 🔧 EXTRACTION METHODS

### Method 1: PDF Extraction

**Use Case**: Most common format for guides, ebooks, documentation

**Process**:
```python
import PyPDF2
from pdfminer.high_level import extract_text

def extract_pdf(file_path):
    # Try pdfminer first (better text extraction)
    try:
        text = extract_text(file_path)
        if len(text) > 100:  # Minimum viable content
            return clean_text(text)
    except:
        pass

    # Fallback to PyPDF2
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return clean_text(text)
    except Exception as e:
        return {"error": f"PDF extraction failed: {e}"}

def clean_text(text):
    # Remove excessive whitespace
    text = ' '.join(text.split())
    # Fix common PDF artifacts
    text = text.replace('\x00', '')
    # Normalize line breaks
    text = text.replace('\r\n', '\n')
    return text
```

**Expected Output**: Clean text string (5,000-50,000 chars typical)

**Common Issues**:
- Scanned PDFs (no text layer) → Requires OCR
- Multi-column layouts → Extract sequentially, may need reordering
- Embedded images → Extract separately if text embedded

---

### Method 2: Video Transcript Extraction

**Use Case**: YouTube tutorials, course videos, recorded webinars

**Process**:
```python
from youtube_transcript_api import YouTubeTranscriptApi
import whisper

def extract_video(video_source):
    # If YouTube URL, try transcript API first
    if "youtube.com" in video_source or "youtu.be" in video_source:
        video_id = extract_video_id(video_source)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
            text = ' '.join([entry['text'] for entry in transcript])
            return {"text": text, "method": "youtube_api"}
        except:
            pass

    # Fallback: Download + Whisper transcription
    try:
        model = whisper.load_model("base")
        result = model.transcribe(video_source, language="pt")
        return {"text": result["text"], "method": "whisper"}
    except Exception as e:
        return {"error": f"Video extraction failed: {e}"}
```

**Expected Output**: Transcript text (10,000-100,000 chars for 30-60 min video)

**Post-Processing**:
- Remove filler words ("né", "tipo", "assim")
- Add paragraph breaks at natural pauses
- Fix transcription errors (common PT-BR mistakes)

---

### Method 3: Image OCR

**Use Case**: Screenshots, infographics, printed material photos

**Process**:
```python
from PIL import Image
import pytesseract
import cv2
import numpy as np

def extract_image(image_path):
    try:
        # Preprocessing for better OCR
        img = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply thresholding
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # OCR with Portuguese
        text = pytesseract.image_to_string(thresh, lang='por')

        return {"text": text, "confidence": "medium"}
    except Exception as e:
        return {"error": f"OCR failed: {e}"}
```

**Expected Output**: Extracted text (accuracy 60-95% depending on image quality)

**Quality Indicators**:
- High confidence: Clear screenshots, high-DPI scans
- Medium: Photos of printed material, slight blur
- Low: Handwriting, low-quality photos (may need manual review)

---

### Method 4: Structured Data (JSON/CSV)

**Use Case**: API responses, product catalogs, research data

**Process**:
```python
import json
import pandas as pd

def extract_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert to readable text format
    if isinstance(data, dict):
        text = json.dumps(data, indent=2, ensure_ascii=False)
    elif isinstance(data, list):
        # Extract key fields from list of objects
        text = "\n\n".join([str(item) for item in data])

    return {"text": text, "format": "json"}

def extract_csv(file_path):
    df = pd.read_csv(file_path)

    # Convert to markdown table
    text = df.to_markdown(index=False)

    # Add summary stats if numeric
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        text += "\n\n## Summary Stats\n"
        text += df[numeric_cols].describe().to_markdown()

    return {"text": text, "format": "csv", "rows": len(df)}
```

**Expected Output**: Formatted text representation of structured data

---

### Method 5: Web Page (HTML)

**Use Case**: Blog posts, documentation, marketplace listings

**Process**:
```python
from bs4 import BeautifulSoup
import requests

def extract_html(url_or_file):
    # If URL, fetch content
    if url_or_file.startswith('http'):
        response = requests.get(url_or_file)
        html = response.text
    else:
        with open(url_or_file, 'r', encoding='utf-8') as f:
            html = f.read()

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Remove scripts, styles, nav
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()

    # Extract main content
    main_content = soup.find('main') or soup.find('article') or soup.find('body')

    # Get text with structure
    text = main_content.get_text(separator='\n', strip=True)

    return {"text": text, "source": url_or_file}
```

**Expected Output**: Clean text content without HTML tags/scripts

---

## 🧹 POST-EXTRACTION CLEANING

**Apply to all extracted content**:

```python
def clean_extracted_content(text):
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Fix encoding issues
    text = text.encode('utf-8', 'ignore').decode('utf-8')

    # Remove URLs (if not needed)
    # text = re.sub(r'http\S+', '', text)

    # Normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove repeated punctuation
    text = re.sub(r'([!?.]){3,}', r'\1', text)

    # Fix common PT-BR issues
    text = text.replace(' , ', ', ').replace(' . ', '. ')

    return text.strip()
```

---

## 📊 EXTRACTION QUALITY ASSESSMENT

**Immediate Quality Check**:

```python
def assess_extraction_quality(extracted_text):
    quality = {
        "length": len(extracted_text),
        "issues": [],
        "confidence": "high"
    }

    # Check minimum viable length
    if len(extracted_text) < 100:
        quality["issues"].append("Too short (< 100 chars)")
        quality["confidence"] = "low"

    # Check for extraction artifacts
    artifact_ratio = len(re.findall(r'[^\w\s]', extracted_text)) / len(extracted_text)
    if artifact_ratio > 0.3:
        quality["issues"].append("High special character ratio (> 30%)")
        quality["confidence"] = "medium"

    # Check language (should be mostly Portuguese or English)
    pt_words = len(re.findall(r'\b(que|para|com|uma|este|isso|como)\b', extracted_text, re.I))
    en_words = len(re.findall(r'\b(the|and|for|with|this|that|how)\b', extracted_text, re.I))
    if pt_words < 3 and en_words < 3:
        quality["issues"].append("Language detection uncertain")
        quality["confidence"] = "low"

    return quality
```

**Confidence Levels**:
- **High** (>90%): Clean extraction, minimal artifacts, clear language
- **Medium** (60-90%): Some artifacts, but usable content
- **Low** (<60%): Significant issues, may need manual review or different extraction method

---

## 🔄 FALLBACK STRATEGY

**If primary extraction fails**:

1. **Try alternative method** (e.g., PyPDF2 → pdfminer → OCR for PDFs)
2. **Partial extraction** (extract first N pages if full extraction fails)
3. **Manual upload** (ask seller to copy-paste content if automated fails)
4. **Error reporting** (log failure + suggest alternative format)

**Example**:
```python
def extract_with_fallback(file_path):
    methods = [
        ("Primary", extract_primary),
        ("Fallback 1", extract_fallback1),
        ("Fallback 2", extract_fallback2)
    ]

    for method_name, method_func in methods:
        try:
            result = method_func(file_path)
            if result and len(result.get("text", "")) > 100:
                result["extraction_method"] = method_name
                return result
        except Exception as e:
            print(f"{method_name} failed: {e}")
            continue

    return {"error": "All extraction methods failed", "file": file_path}
```

---

## 📋 EXTRACTION CHECKLIST

Before moving to Classification stage:

- [ ] File format detected correctly
- [ ] Extraction method executed without errors
- [ ] Minimum 100 chars extracted (viable content)
- [ ] Text encoding is UTF-8
- [ ] Special character ratio < 30%
- [ ] Language detected (PT-BR or EN)
- [ ] Extraction quality assessed (high/medium/low)
- [ ] Fallback attempted if primary failed

---

## 📤 OUTPUT FORMAT

**Expected output structure**:

```json
{
  "status": "success | partial | failed",
  "text": "Extracted content as clean text...",
  "metadata": {
    "source_file": "RASCUNHO/guia_ml.pdf",
    "file_type": "pdf",
    "extraction_method": "pdfminer",
    "extracted_chars": 15420,
    "quality_confidence": "high",
    "extraction_time": "2.3s"
  },
  "issues": [],
  "next_stage": "classification"
}
```

---

**Status**: Stage 1 of knowledge processing pipeline
**Integration**: Called by knowledge_processor_HOP before classification
**Performance**: Target <5s per file (PDF/text), <30s per video (transcription)