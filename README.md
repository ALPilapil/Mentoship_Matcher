# 🤝 Mentoship_Matcher

A Streamlit web app that intelligently pairs "bigs" and "littles" based on their responses to a set of questions. Using semantic similarity embeddings and user-defined category weights, this tool helps organizations make more meaningful and personalized matches.

## 🔍 Overview

This project is designed to support mentorship programs, student orgs, or any matching-based system where it's important to connect individuals based on shared values, interests, or traits.

### Key Features:
- 📂 Upload your own CSV with responses for "bigs" and "littles"
- 🧠 Uses semantic similarity (e.g., BERT embeddings) to compare answers
- ⚖️ Customize the weight of each category to emphasize different matching priorities
- 📊 View and download the final ranked matches

---

## 🗂️ Example Use Case

- **Bigs and Littles**: Matching mentors and mentees in student organizations
- **Buddies**: Pairing incoming students with current members
- **General**: As long as there are two groups of people it works

---

## 🚀 How It Works

1. **Upload CSVs**  
   Upload one CSV file: making sure every person has one role or both. Each row should represent a person and each column a question/category.

2. **Adjust Weights**  
   Customize how much each category should influence the match score.

3. **Matching Logic**  
   For each big, the app:
   - Encodes answers using a sentence transformer
   - Compares answers with every little using cosine similarity
   - Applies user-defined weights per category
   - Ranks littles from most to least compatible

4. **Results**  
   See ranked matches instantly, with options to download results as CSV.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python
- **Semantic Embeddings**: Sentence-BERT (or similar transformer models)
- **Data Handling**: Pandas, NumPy

---

## 📁 CSV Format

Both bigs and littles CSVs should follow this format:

| name  |  role  | q2_response | q3_response | ... |
|-------|--------|-------------|-------------|-----|
| Alice | mentee | Very social | Dog person  | ... |

Ensure:
- There is a name and role column
- Data contains only information related to matching for best results

---

## ⚙️ Use
use the website here: https://bsls-matcher.streamlit.app/
