# 💰 Personal Expense Tracker

A Python command-line app to log, categorise, and analyse your daily expenses — with monthly reports, budget alerts, and search filters. All data is saved locally in a CSV file.

---

## ✨ Features

- **Add expenses** with amount, category, description, tags, and date
- **8 categories** — Food & Dining, Transport, Shopping, Entertainment, Education, Health, Utilities, Other
- **Monthly reports** — category-wise breakdown with visual bars and percentage of total spend
- **Budget tracking** — set a monthly budget and see how much is left (or over!)
- **Search & filter** — by keyword, category, or date range
- **Delete last entry** — quick undo for mistakes
- **Persistent storage** — all data saved in `expenses.csv`, survives across sessions

---

## 🚀 How to Run

**1. Install Python** (3.8 or above) from [python.org](https://python.org)

**2. No extra libraries needed** — uses only Python built-ins

**3. Run the app:**
```bash
python expense_tracker.py
```

---

## 🗂️ Menu Options

```
1 → Add expense
2 → View all expenses
3 → Monthly report & category breakdown
4 → Search / filter expenses
5 → Set monthly budget
6 → Delete last entry
7 → Quit
```

---

## 📊 Sample Monthly Report

```
── 2024-06 ──────────────────────────────────────
Category               Spent        % of Total
─────────────────────────────────────────────────
Food & Dining        ₹3,200.00       42.1%  ████████
Transport            ₹1,500.00       19.7%  ███
Shopping             ₹1,200.00       15.8%  ███
Education            ₹1,000.00       13.2%  ██
Entertainment          ₹700.00        9.2%  █
─────────────────────────────────────────────────
TOTAL                ₹7,600.00

Budget: ₹8,000.00  |  Remaining: ₹400.00
```

---

## 📁 Files

```
expense_tracker.py      # Main application file
expenses.csv            # Auto-generated — stores all your expense records
budget_config.json      # Auto-generated — stores your budget settings
```

---

## 🛠️ Built With

- Python 3
- Built-in libraries only: `csv`, `json`, `os`, `datetime`, `collections`

---

## 👩‍💻 Author

**Ananya J** — 2nd Year B.Tech CSE, Anurag University  
[GitHub](https://github.com/nyanya0) · [LinkedIn](https://linkedin.com/in/ananya-j-748265357)
