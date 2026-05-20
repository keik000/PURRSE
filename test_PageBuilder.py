# test_PageBuilder.py
from purrseapp import PageBuilder, InfoInput, Manage_Expense, CSV_Data

def test_page_start_contains_html():
    b    = PageBuilder()
    html = b.build_page_start()
    assert '<!DOCTYPE html>' in html
    assert '<body' in html

def test_page_end_contains_footer():
    b    = PageBuilder()
    html = b.build_page_end()
    assert 'purrpose' in html
    assert '</html>' in html

def test_site_header_contains_title():
    b    = PageBuilder()
    html = b.build_site_header()
    assert 'PURR$E' in html
    assert 'Expense tracker' in html.lower() or 'mood' in html.lower()

def test_stats_bar_shows_total():
    b    = PageBuilder()
    html = b.build_stats_bar(250.0, 'food', 'happy')
    assert '250.00'  in html
    assert 'FOOD'    in html
    assert 'HAPPY'   in html

def test_stats_bar_none_values():
    b    = PageBuilder()
    html = b.build_stats_bar(0.0, None, None)
    assert 'NONE' in html

def test_expense_rows_filters_by_category():
    expenses = [
        InfoInput('Lunch', 'happy', 120.0, 'food'),
        InfoInput('Bus',   'tired',  50.0, 'transpo'),
    ]
    b    = PageBuilder()
    html = b.build_expense_rows(expenses, 'food')
    assert 'Lunch' in html
    assert 'Bus'   not in html

def test_input_form_contains_fields():
    expense_list = []
    mgr  = Manage_Expense(expense_list, CSV_Data('test_pb.csv'))
    b    = PageBuilder()
    html = b.build_input_form('food', mgr)
    assert 'description' in html
    assert 'mood'        in html
    assert 'cost'        in html

def test_category_card_shows_total():
    expenses = [InfoInput('Lunch', 'happy', 200.0, 'food')]
    mgr      = Manage_Expense(expenses, CSV_Data('test_pb2.csv'))
    b        = PageBuilder()
    html     = b.build_category_card('😸🍜', 'food', expenses, {'food': 200.0}, mgr)
    assert '200.00' in html
    assert 'FOOD'   in html