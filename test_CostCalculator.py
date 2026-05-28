from purrseapp import InfoInput, CostCalculator

# ── Tests for CostCalculator ──────────────────────────────

def test_food_total():
    expenses = [
        InfoInput('Lunch',  'happy', 120.0, 'food'),
        InfoInput('Dinner', 'bored',  80.0, 'food'),
        InfoInput('Bus',    'tired',  50.0, 'transpo'),
    ]
    calc   = CostCalculator(expenses)
    totals = calc.get_category_totals()
    assert totals['food'] == 200.0

def test_transpo_total():
    expenses = [
        InfoInput('Lunch', 'happy', 120.0, 'food'),
        InfoInput('Bus',   'tired',  50.0, 'transpo'),
    ]
    calc   = CostCalculator(expenses)
    totals = calc.get_category_totals()
    assert totals['transpo'] == 50.0

def test_missing_category():
    expenses = [InfoInput('Lunch', 'happy', 100.0, 'food')]
    calc   = CostCalculator(expenses)
    totals = calc.get_category_totals()
    assert totals.get('medical') is None

def test_grand_total():
    expenses = [
        InfoInput('Lunch',  'happy', 120.0, 'food'),
        InfoInput('Bus',    'tired',  50.0, 'transpo'),
        InfoInput('Dinner', 'bored',  80.0, 'food'),
    ]
    calc = CostCalculator(expenses)
    assert calc.get_grand_total() == 250.0

def test_grand_total_empty():
    calc = CostCalculator([])
    assert calc.get_grand_total() == 0.0

def test_top_category():
    expenses = [
        InfoInput('Lunch',  'happy', 120.0, 'food'),
        InfoInput('Dinner', 'bored',  80.0, 'food'),
        InfoInput('Bus',    'tired',  50.0, 'transpo'),
    ]
    calc = CostCalculator(expenses)
    top_cat, top_amt = calc.get_top_category()
    assert top_cat == 'food'
    assert top_amt == 200.0
