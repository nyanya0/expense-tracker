import csv
import os
import json
from datetime import datetime, date
from collections import defaultdict

# ── Colour helpers ────────────────────────────────────────────────────────────
def col(text, code): return f"\033[{code}m{text}\033[0m"
def green(t):  return col(t, "92")
def red(t):    return col(t, "91")
def cyan(t):   return col(t, "96")
def yellow(t): return col(t, "93")
def bold(t):   return col(t, "1")
def dim(t):    return col(t, "2")

DATA_FILE   = "expenses.csv"
CONFIG_FILE = "budget_config.json"

CATEGORIES = [
    "Food & Dining",
    "Transport",
    "Shopping",
    "Entertainment",
    "Education",
    "Health",
    "Utilities",
    "Other",
]

FIELDNAMES = ["date", "amount", "category", "description", "tags"]

# ── File helpers ──────────────────────────────────────────────────────────────
def init_csv():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()

def load_expenses():
    init_csv()
    with open(DATA_FILE, newline="") as f:
        return list(csv.DictReader(f))

def save_expense(entry):
    init_csv()
    with open(DATA_FILE, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow(entry)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"monthly_budget": 0, "category_budgets": {}}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

# ── UI helpers ────────────────────────────────────────────────────────────────
def banner():
    print(cyan(bold("""
  ╔═══════════════════════════════════════════════╗
  ║       💰  Personal Expense Tracker  💰        ║
  ║     Track · Analyse · Stay on Budget          ║
  ╚═══════════════════════════════════════════════╝
""")))

def pick_category():
    print("\n  Categories:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"   {i}. {c}")
    while True:
        raw = input("\n  Pick a number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(CATEGORIES):
            return CATEGORIES[int(raw) - 1]
        print(red("  Invalid. Enter a number from the list."))

def fmt_inr(amount):
    return f"₹{float(amount):,.2f}"

def separator():
    print(dim("  " + "─" * 52))

# ── Core features ─────────────────────────────────────────────────────────────
def add_expense():
    print(cyan(bold("\n  ── Add Expense ──")))

    # Amount
    while True:
        raw = input("  Amount (₹): ").strip()
        try:
            amount = float(raw)
            if amount <= 0: raise ValueError
            break
        except ValueError:
            print(red("  Enter a positive number."))

    # Category
    category = pick_category()

    # Description
    desc = input("  Description (optional): ").strip() or "—"

    # Tags
    tags = input("  Tags (comma-separated, optional): ").strip() or ""

    # Date
    date_raw = input("  Date (YYYY-MM-DD, leave blank for today): ").strip()
    if not date_raw:
        entry_date = str(date.today())
    else:
        try:
            datetime.strptime(date_raw, "%Y-%m-%d")
            entry_date = date_raw
        except ValueError:
            print(yellow("  Invalid date format — using today."))
            entry_date = str(date.today())

    entry = {
        "date": entry_date,
        "amount": f"{amount:.2f}",
        "category": category,
        "description": desc,
        "tags": tags,
    }
    save_expense(entry)
    print(green(f"\n  ✅  Saved: {fmt_inr(amount)} → {category} on {entry_date}"))


def view_all():
    expenses = load_expenses()
    if not expenses:
        print(yellow("\n  No expenses recorded yet."))
        return

    print(cyan(bold(f"\n  ── All Expenses ({len(expenses)} records) ──")))
    separator()
    print(f"  {'Date':<12}{'Amount':>10}  {'Category':<20}  {'Description'}")
    separator()
    for e in sorted(expenses, key=lambda r: r["date"], reverse=True):
        print(f"  {e['date']:<12}{fmt_inr(e['amount']):>10}  {e['category']:<20}  {e['description']}")
    separator()
    total = sum(float(e["amount"]) for e in expenses)
    print(bold(f"  {'TOTAL':>44}  {fmt_inr(total)}"))


def monthly_report():
    expenses = load_expenses()
    if not expenses:
        print(yellow("\n  No expenses to report."))
        return

    # Pick month
    months = sorted({e["date"][:7] for e in expenses}, reverse=True)
    print(cyan(bold("\n  ── Monthly Report ──")))
    print("  Available months:")
    for i, m in enumerate(months, 1):
        print(f"   {i}. {m}")
    while True:
        raw = input("\n  Pick a month number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(months):
            selected = months[int(raw) - 1]
            break
        print(red("  Invalid choice."))

    filtered = [e for e in expenses if e["date"].startswith(selected)]
    if not filtered:
        print(yellow("  No expenses for that month."))
        return

    by_cat = defaultdict(float)
    for e in filtered:
        by_cat[e["category"]] += float(e["amount"])

    total = sum(by_cat.values())
    cfg   = load_config()
    budget = cfg.get("monthly_budget", 0)

    print(cyan(bold(f"\n  ── {selected} ──")))
    separator()
    print(f"  {'Category':<22} {'Spent':>10}  {'% of Total':>10}")
    separator()
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        pct = (amt / total * 100) if total else 0
        bar = "█" * int(pct / 5)
        print(f"  {cat:<22} {fmt_inr(amt):>10}  {pct:>8.1f}%  {green(bar)}")
    separator()
    print(bold(f"  {'TOTAL':<22} {fmt_inr(total):>10}"))

    if budget:
        remaining = budget - total
        colour = green if remaining >= 0 else red
        print(colour(f"\n  Budget: {fmt_inr(budget)}  |  Remaining: {fmt_inr(remaining)}"))
        if remaining < 0:
            print(red(f"  ⚠️  Over budget by {fmt_inr(abs(remaining))}!"))


def search_expenses():
    expenses = load_expenses()
    print(cyan(bold("\n  ── Search Expenses ──")))
    print("  Search by:  1. Keyword   2. Category   3. Date range\n")
    mode = input("  Choose: ").strip()

    if mode == "1":
        kw = input("  Keyword: ").strip().lower()
        results = [e for e in expenses
                   if kw in e["description"].lower() or kw in e["tags"].lower()]
    elif mode == "2":
        category = pick_category()
        results = [e for e in expenses if e["category"] == category]
    elif mode == "3":
        start = input("  Start date (YYYY-MM-DD): ").strip()
        end   = input("  End date   (YYYY-MM-DD): ").strip()
        results = [e for e in expenses if start <= e["date"] <= end]
    else:
        print(red("  Invalid choice.")); return

    if not results:
        print(yellow("\n  No matching expenses found."))
        return

    print(cyan(bold(f"\n  Found {len(results)} result(s):")))
    separator()
    for e in sorted(results, key=lambda r: r["date"], reverse=True):
        print(f"  {e['date']}  {fmt_inr(e['amount']):>10}  {e['category']:<20}  {e['description']}")
    separator()
    total = sum(float(e["amount"]) for e in results)
    print(bold(f"  Total: {fmt_inr(total)}"))


def set_budget():
    cfg = load_config()
    print(cyan(bold("\n  ── Set Budget ──")))
    raw = input(f"  Monthly budget (current: {fmt_inr(cfg['monthly_budget'])}): ₹").strip()
    try:
        cfg["monthly_budget"] = float(raw)
        save_config(cfg)
        print(green(f"  ✅  Monthly budget set to {fmt_inr(cfg['monthly_budget'])}"))
    except ValueError:
        print(red("  Invalid amount."))


def delete_last():
    expenses = load_expenses()
    if not expenses:
        print(yellow("\n  Nothing to delete.")); return
    last = sorted(expenses, key=lambda r: r["date"])[-1]
    print(yellow(f"\n  Last entry: {last['date']}  {fmt_inr(last['amount'])}  {last['category']}  {last['description']}"))
    confirm = input("  Delete this? (y/n): ").strip().lower()
    if confirm == "y":
        expenses = [e for e in expenses if e != last]
        with open(DATA_FILE, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDNAMES)
            w.writeheader()
            w.writerows(expenses)
        print(green("  ✅  Deleted."))
    else:
        print("  Cancelled.")


# ── Main menu ─────────────────────────────────────────────────────────────────
def main():
    banner()
    init_csv()
    while True:
        print(bold("\n  ── Menu ─────────────────────────────────"))
        print("   1 → Add expense")
        print("   2 → View all expenses")
        print("   3 → Monthly report & category breakdown")
        print("   4 → Search / filter expenses")
        print("   5 → Set monthly budget")
        print("   6 → Delete last entry")
        print("   7 → Quit")
        print(bold("  ─────────────────────────────────────────"))
        choice = input("\n  Choose: ").strip()

        if   choice == "1": add_expense()
        elif choice == "2": view_all()
        elif choice == "3": monthly_report()
        elif choice == "4": search_expenses()
        elif choice == "5": set_budget()
        elif choice == "6": delete_last()
        elif choice == "7":
            print(cyan("\n  Goodbye! Stay on budget 💸\n")); break
        else:
            print(red("  Please enter 1–7."))

if __name__ == "__main__":
    main()
