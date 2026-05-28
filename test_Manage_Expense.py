import os
from purrseapp import Manage_Expense, CSV_Data

# ── Tests for Manage_Expense ──────────────────────────────

def test_add_expense():
    expense_list = []
    mgr = Manage_Expense(expense_list, CSV_Data('test_mgr1.csv'))
    mgr.add_expense('food', 'Lunch', 'happy', '120.0')
    assert len(expense_list) == 1
    assert expense_list[0].description == 'Lunch'
    os.remove('test_mgr1.csv')

def test_add_blocked():
    expense_list = []
    mgr = Manage_Expense(expense_list, CSV_Data('test_mgr2.csv'))
    mgr.add_expense('food', 'Lunch 2x', 'happy', '120.0')
    assert len(expense_list) == 0
    assert mgr.desc_error == True

def test_delete_expense():
    expense_list = []
    mgr = Manage_Expense(expense_list, CSV_Data('test_mgr3.csv'))
    mgr.add_expense('food', 'Lunch',  'happy', '100.0')
    mgr.add_expense('food', 'Dinner', 'bored', '200.0')
    mgr.delete_expense(0)
    assert len(expense_list) == 1
    assert expense_list[0].description == 'Dinner'
    os.remove('test_mgr3.csv')

def test_delete_invalid_index ():
    expense_list = []
    mgr = Manage_Expense(expense_list, CSV_Data('test_mgr4.csv'))
    mgr.add_expense('food', 'Lunch', 'happy', '100.0')
    mgr.delete_expense(99)
    assert len(expense_list) == 1
    os.remove('test_mgr4.csv')
