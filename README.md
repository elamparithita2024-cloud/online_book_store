# 📚 BookVerse - Online Book Store Application with SCM Integration

[![Git SCM](https://img.shields.io/badge/SCM-Git%202.45+-orange.svg)](https://git-scm.com/)
[![CI Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](.github/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v1.1.0-brightgreen.svg)](#)

A modern, full-featured **Online Book Store Application** integrated with **Source Code Management (SCM)** tools (**Git**, automated CI/CD pipeline, Git hooks, and a custom standalone **PySCM** version control engine).

---

## 🌟 Application Features

### 🛒 1. E-Commerce Bookstore Platform
- **Curated Catalog:** 16+ titles across Computer Science, Sci-Fi, Business, Philosophy, Fiction, and Biography with ratings, reviews, stock counts, and high-resolution covers.
- **Instant Search & Multi-Criteria Filtering:** Real-time search across titles, authors, categories, and tags; category filter chips with dynamic book counters; multiple sorting modes (Price, Rating, Title, Featured).
- **Interactive Shopping Cart:** Real-time cart drawer with quantity adjustments, stock availability validation, and promo code discounts (`BOOKSTORE20` for 20% off, `FREESHIP` for free shipping).
- **Book Quick-View Modal:** Full synopsis, excerpt reading sample, community ratings breakdown, and interactive customer review submission form.
- **Multi-Step Checkout Flow:** Shipping address validation, payment method selector (Card, UPI, PayPal, COD), and instant printable invoice receipt generation.
- **Customer Order Tracking:** Dedicated "My Orders" tab with status tracking, date, items ordered, and billing history.
- **Inventory Admin Portal:** Add new book titles, live stock monitors with low-stock warnings, and catalogue reset tools.
- **Theme & Responsiveness:** Dark/Light mode toggle with persistence; completely responsive design across mobile, tablet, and desktop.

### 🛠️ 2. SCM (Source Code Management) Implementation
- **Git Version Control System:** Full Git implementation with conventional commit history (`feat:`, `fix:`, `docs:`, `ci:`, `chore:`), Git Flow branching (`main`, `develop`, `feature/*`), and release tagging (`v1.0.0`, `v1.1.0`).
- **In-App SCM Explorer Dashboard:** Visualizes live Git branches, commit graph timeline, semantic change diffs, and an interactive **Git Commit Simulator** right inside the web application!
- **Standalone Custom SCM Tool (`mini_scm.py`):** A from-scratch, zero-dependency version control engine in Python implementing SHA-1 content-addressable storage, staging index, commit graph DAG, and branch heads.
- **Automated SCM CLI Manager (`scm_tool.py`):** Automates repository status checks, integrity verification, test suites, and zip snapshot backups.
- **Git Hooks (`.githooks/`):** Pre-commit hook for code validation; commit-msg hook enforcing the Conventional Commits specification.
- **CI/CD Pipeline (`.github/workflows/ci.yml`):** GitHub Actions pipeline for automated linting, unit testing, and SCM packaging.

---

## 📂 Project Directory Structure

```
online book store/
├── index.html                   # Complete modern Frontend SPA with SCM Explorer
├── css/
│   └── styles.css               # Responsive design, theme variables, SCM styling
├── js/
│   ├── app.js                   # Application state, cart, checkout, reviews, admin
│   ├── books-data.js            # Comprehensive catalog database (16 books)
│   └── scm-visualizer.js        # Interactive SCM dashboard and Git simulator
├── server.js                    # Dual-mode Node.js backend server with REST API
├── app.py                       # Standalone Python backend server alternative
├── mini_scm.py                  # Standalone SCM Tool implementation ("PySCM")
├── scm_tool.py                  # SCM workflow CLI manager & test verification
├── package.json                 # Node.js manifest and test scripts
├── requirements.txt             # Python specifications
├── run_app.bat                  # One-click Windows application launcher
├── scm_tool.bat                 # Windows SCM launcher wrapper
├── .gitignore                   # SCM ignore configuration
├── .gitattributes               # SCM line ending normalization
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD automation workflow
├── .githooks/
│   ├── pre-commit               # Git hook for sanity & file validation
│   └── commit-msg               # Git hook enforcing Conventional Commits
├── SCM_IMPLEMENTATION.md         # Comprehensive formal SCM Report
└── docs/
    └── SCM_LAB_MANUAL.md        # Academic Lab Manual with Viva Voce Q&A
```

---

## 🚀 Quick Start Guide

### Option 1: Direct Browser Launch (Zero Dependencies)
Simply double-click `index.html` or run:
```powershell
# Open directly in default web browser
start index.html
```

### Option 2: Using the Windows Interactive Launcher
Double-click `run_app.bat` to launch the menu:
```text
  [1] Direct Browser Mode (Zero dependencies, instant launch)
  [2] Node.js Express REST API Server (http://localhost:3000)
  [3] Python Web Server & REST API (http://localhost:8000)
  [4] Launch SCM Automation Tool (Git / PySCM)
```

### Option 3: Run with Node.js
```bash
node server.js
# Access at http://localhost:3000
```

### Option 4: Run with Python
```bash
python app.py
# Access at http://localhost:8000
```

---

## 🛠️ SCM Tool Commands Reference

### 1. Using the PySCM Engine (`mini_scm.py`)
```bash
# Initialize SCM repository
python mini_scm.py init

# Stage modified files
python mini_scm.py add .

# Create a commit
python mini_scm.py commit -m "feat: add shopping cart checkout"

# Check repository status
python mini_scm.py status

# View commit revision history
python mini_scm.py log

# Create and switch branches
python mini_scm.py branch feature/cart
python mini_scm.py checkout feature/cart
```

### 2. Using the SCM Manager (`scm_tool.py`)
```bash
# Verify project integrity and run automated test suites
python scm_tool.py verify

# View SCM status
python scm_tool.py status

# View commit graph
python scm_tool.py log

# Create timestamped project backup snapshot
python scm_tool.py backup
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/books` | Returns array of all available books |
| `GET` | `/api/books/:id` | Returns single book by ID |
| `POST` | `/api/books` | Add new book to catalog (JSON payload) |
| `DELETE`| `/api/books/:id` | Removes book from catalog |
| `GET` | `/api/orders` | Retrieves all customer orders |
| `POST` | `/api/orders` | Creates a new order |
| `GET` | `/api/scm/status` | Returns live SCM engine and branch metrics |

---

## 📖 Academic / Lab Documentation
- **Formal SCM Technical Report:** [SCM_IMPLEMENTATION.md](SCM_IMPLEMENTATION.md)
- **Lab Manual with Viva Questions & Answers:** [docs/SCM_LAB_MANUAL.md](docs/SCM_LAB_MANUAL.md)

---

## 📄 License
This project is licensed under the MIT License.
