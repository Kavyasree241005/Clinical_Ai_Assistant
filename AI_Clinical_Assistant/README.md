# AI-Based Clinical Conversation Structuring and Decision Support System

## Project Overview

This project is an AI-powered healthcare documentation and clinical recommendation system designed to process doctor–patient conversations and convert them into structured clinical records.

The system performs:
- Clinical entity extraction
- Disease prediction
- SOAP clinical summary generation
- PDF/EMR-style report generation

The architecture is designed with:
- modular AI pipelines
- local processing
- healthcare confidentiality
- explainable machine learning

---

# Problem Statement

Develop an AI-powered system capable of processing doctor–patient clinical conversations and automatically generating structured clinical documentation, provisional clinical recommendations, and downloadable reports.

---

# Key Features

## Clinical Entity Extraction
Extract:
- symptoms
- duration
- medications
- severity
- body parts
- age/gender information

---

## Clinical Prediction Layer
Predict:
- possible disease/condition
- clinical category
- referral department
- consultation priority

using:
- TF-IDF Vectorization
- Logistic Regression
- Random Forest

---

## SOAP Clinical Summary Generation
Automatically generate:
- Subjective
- Objective
- Assessment
- Plan

using:
- Local LLM
- Jinja2 templates

---

## PDF / EMR Report Generation
Generate:
- structured PDF reports
- EMR-style summaries
- downloadable clinical documentation

---

# Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| NLP | spaCy + MedSpaCy |
| ML Models | Logistic Regression + Random Forest |
| Vectorization | TF-IDF |
| LLM | Phi-3 |
| LLM Runtime | Ollama |
| Backend | FastAPI |
| Templates | Jinja2 |
| PDF Generation | ReportLab |
| Data Processing | Pandas + NumPy |

---

# Project Architecture

```text
Clinical Transcript
         ↓
Entity Extraction
         ↓
TF-IDF Vectorization
         ↓
Logistic Regression + Random Forest
         ↓
Prediction Output
         ↓
SOAP Generator
(LLM + Jinja2)
         ↓
Structured Clinical Summary
         ↓
PDF Report Generator