import os
import pytest
from purrseapp import MoodExpenseManager, CSV_Data

TEST_CSV = "test_purrserecord.csv"


def make_mgr():
    return MoodExpenseManager(CSV_Data(TEST_CSV))


def teardown_function():
    if os.path.exists(TEST_CSV):
        os.remove(TEST_CSV)


def test_add_saves_expense():
    mgr = make_mgr()
    initial = len(mgr.expense_list)
    mgr.add_expense("food", "Lunch", "happy", "120.0")
    assert len(mgr.expense_list) == initial + 1


def test_add_creates_csv():
    mgr = make_mgr()
    mgr.add_expense("medical", "Checkup", "worried", "500.0")
    assert os.path.exists(TEST_CSV)


def test_add_invalid_is_blocked():
    mgr = make_mgr()
    initial = len(mgr.expense_list)
    mgr.add_expense("food", "Lunch 2x", "happy", "120.0")
    assert len(mgr.expense_list) == initial


def test_delete_removes_one():
    mgr = make_mgr()
    mgr.add_expense("food", "Lunch", "happy", "100.0")
    mgr.add_expense("food", "Dinner", "bored", "200.0")
    before = len(mgr.expense_list)
    mgr.delete_expense(0)
    assert len(mgr.expense_list) == before - 1


def test_delete_removes_correct_item():
    mgr = make_mgr()
    mgr.add_expense("food", "Lunch", "happy", "100.0")
    mgr.add_expense("food", "Dinner", "bored", "200.0")
    mgr.delete_expense(0)
    assert mgr.expense_list[0].description == "Dinner"


def test_delete_bad_index_ignored():
    mgr = make_mgr()
    mgr.add_expense("food", "Lunch", "happy", "100.0")
    before = len(mgr.expense_list)
    mgr.delete_expense(99)
    assert len(mgr.expense_list) == before


def test_top_mood_after_add():
    mgr = make_mgr()
    mgr.add_expense("food", "Lunch", "happy", "300.0")
    assert mgr.mood_analyzer.get_top_mood() == "happy"


def test_top_mood_after_delete():
    mgr = make_mgr()
    mgr.add_expense("food", "Lunch", "happy", "50.0")
    mgr.add_expense("food", "Snack", "tired", "300.0")
    assert mgr.mood_analyzer.get_top_mood() == "tired"
    mgr.delete_expense(1)
    assert mgr.mood_analyzer.get_top_mood() == "happy"


def test_grand_total_is_correct():
    mgr = make_mgr()
    mgr.add_expense("food", "Lunch", "happy", "150.0")
    assert mgr.cost_calculator.get_grand_total() >= 150.0


def test_grand_total_across_categories():
    mgr = make_mgr()
    mgr.add_expense("food",    "Lunch",   "happy",   "100.0")
    mgr.add_expense("transpo", "Bus",     "tired",    "50.0")
    mgr.add_expense("medical", "Checkup", "worried", "200.0")
    assert mgr.cost_calculator.get_grand_total() == 350.0


def test_reload_keeps_data():
    mgr = make_mgr()
    mgr.add_expense("food", "Lunch", "happy", "120.0")
    reloaded = make_mgr()
    assert len(reloaded.expense_list) == 1
    assert reloaded.expense_list[0].description == "Lunch"
    assert reloaded.expense_list[0].cost == 120.0