# Mini SIEM Dashboard

[![CI](https://github.com/engmesh1/mini-siem-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/engmesh1/mini-siem-dashboard/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-ready-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

A lightweight, developer-friendly **Mini SIEM backend** built with **FastAPI** to ingest security events, normalize them into a consistent schema, store them in **SQLite**, and query them through clean APIs.

> هدف المشروع: محاكاة “حلقة الـ SIEM الأساسية” بشكل نظيف وقابل للاختبار:  
**Ingest → Normalize → Store → Query** (مع Docker + CI)

---

## Why this project?
Security tooling غالبًا معقد وثقيل. هذا المشروع يركز على الأساسيات العملية التي تهم الـ SOC والـ Backend:
1. **Ingest** للأحداث (JSON)
2. **Normalize** لتوحيد الحقول
3. **Store** في قاعدة بيانات خفيفة (SQLite)
4. **Query** بفلاتر منطقية (وقت, IP, نوع الحدث, الشدة…)
5. **Reproducible** تشغيل ثابت (Docker + CI + Tests)

---

## Features
- FastAPI backend مع versioned routes (`/api/v1`)
- Event normalization pipeline (حقول موحدة + parsing آمن)
- SQLite storage
- Query endpoints مع فلاتر + pagination
- Sample data جاهزة للتجربة
- Pytest tests (ingest + query flow)
- Docker + docker-compose
- CI workflow (GitHub Actions)

---

## Tech Stack
- **Python 3.12+**
- **FastAPI**
- **SQLite**
- **Pytest**
- **Docker / Docker Compose**
- **GitHub Actions (CI)**

---

## Project Structure
```text
.
├── backend/
│   ├── app/
│   │   ├── api/v1/routes.py
│   │   ├── core/config.py
│   │   ├── db/database.py
│   │   ├── models/schemas.py
│   │   ├── services/normalize.py
│   │   └── main.py
│   ├── tests/test_ingest_and_query.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── docs/architecture.md
├── sample_data/events.sample.json
├── docker-compose.yml
└── Makefile
