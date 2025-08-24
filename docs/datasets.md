# 📊 Dataset Catalog

## 1. Software Defect Dataset

**Source**: [Kaggle - Software Defect Prediction](https://www.kaggle.com/datasets/)

**Domain Type**: Scientific / Engineering

**License**: CC-BY-4.0

**Description**:  
This dataset contains historical software project data and associated defect labels. It is intended for use in defect prediction, software reliability analysis, and quality assurance studies.

**Files Included**:
- `software_defects.csv` – Raw dataset
- `cleaned_software_defects.csv` – Cleaned and validated version
- `data.db` – SQLite database version

**ETL Process**:  
Implemented in `scripts/ingest.py`, the ETL pipeline loads the CSV, removes null rows, normalizes column names, and exports to cleaned CSV and SQLite DB.

---

## How to Use
- Run the ETL script:  
  ```bash
  python3 scripts/ingest.py
