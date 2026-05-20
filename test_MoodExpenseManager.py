# test_MoodExpenseManager.py
import os
from purrseapp import MoodExpenseManager

def test_add_expense_integration():
    mgr = MoodExpenseManager()
    initial = len(mgr.expense_list)
    mgr.add_expense('food', 'Lunch', 'happy', '120.0')
    assert len(mgr.expense_list) == initial + 1
    if os.path.exists('purrserecord.csv'):
        os.remove('purrserecord.csv')

def test_add_invalid_blocked():
    mgr = MoodExpenseManager()
    initial = len(mgr.expense_list)
    mgr.add_expense('food', 'Lunch 2x', 'happy', '120.0')
    assert len(mgr.expense_list) == initial
    if os.path.exists('purrserecord.csv'):
        os.remove('purrserecord.csv')

def test_delete_expense_integration():
    mgr = MoodExpenseManager()
    mgr.add_expense('food', 'Lunch',  'happy', '100.0')
    mgr.add_expense('food', 'Dinner', 'bored', '200.0')
    before = len(mgr.expense_list)
    mgr.delete_expense(0)
    assert len(mgr.expense_list) == before - 1
    if os.path.exists('purrserecord.csv'):
        os.remove('purrserecord.csv')

def test_mood_analyzer_updates_after_add():
    mgr = MoodExpenseManager()
    mgr.add_expense('food', 'Lunch', 'happy', '300.0')
    assert mgr.mood_analyzer.get_top_mood() == 'happy'
    if os.path.exists('purrserecord.csv'):
        os.remove('purrserecord.csv')

def test_cost_calculator_accessible():
    mgr = MoodExpenseManager()
    mgr.add_expense('food', 'Lunch', 'happy', '150.0')
    total = mgr.cost_calculator.get_grand_total()
    assert total >= 150.0
    if os.path.exists('purrserecord.csv'):
        os.remove('purrserecord.csv')