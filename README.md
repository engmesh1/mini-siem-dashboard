# Mini SIEM Dashboard 🛡️

[![CI](https://github.com/engmesh1/mini-siem-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/engmesh1/mini-siem-dashboard/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-ready-success)
![License](https://img.shields.io/badge/License-MIT-green)

A lightweight, developer-friendly **Mini SIEM backend** built with **FastAPI** to ingest security events, normalize them into a consistent schema, store them in **SQLite**, and query them via clean APIs.

> **Core loop:** Ingest → Normalize → Store → Query (with Docker + Tests + CI)

---

## Why this project?

Security tooling is often heavy and complex. This project focuses on the **core SIEM flow** in a clean, reproducible MVP:
1. **Ingest** events (JSON: single or batch)
2. **Normalize** fields into a consistent schema
3. **Store** events in SQLite
4. **Query** events efficiently (filters + pagination)
5. **Reproducible** development (Docker + CI + tests)

---

## Features

- **FastAPI** backend with versioned routes (`/api/v1`)
- **Event normalization** pipeline (consistent fields + safe parsing)
- **SQLite** storage
- **Query endpoints** with filters (time range, IP, event type, severity) + pagination
- **Sample data** included for quick testing
- **Pytest** tests (ingest + query flow)
- **Docker + docker-compose** for consistent runs
- **CI workflow** (GitHub Actions)

---

## Tech Stack

- **Backend:** FastAPI, Pydantic
- **Database:** SQLite
- **DevOps:** Docker, Docker Compose, GitHub Actions
- **Testing:** Pytest

---

## Quick Start (Local)

### 1) Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
