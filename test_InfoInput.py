import pytest
from purrseapp import InfoInput


def test_infoinput_stores_description():
    e = InfoInput("Lunch", "happy", 100.0, "food")
    assert e.description == "Lunch"

def test_infoinput_stores_mood():
    e = InfoInput("Lunch", "happy", 100.0, "food")
    assert e.mood == "happy"

def test_infoinput_stores_cost():
    e = InfoInput("Lunch", "happy", 100.0, "food")
    assert e.cost == 100.0

def test_infoinput_stores_category():
    e = InfoInput("Lunch", "happy", 100.0, "food")
    assert e.category == "food"

def test_infoinput_cost_is_float():
    e = InfoInput("Lunch", "happy", 100.0, "food")
    assert isinstance(e.cost, float)

def test_infoinput_fields_are_independent():
    a = InfoInput("Lunch",  "happy", 100.0, "food")
    b = InfoInput("Dinner", "bored", 200.0, "transpo")
    assert a.description != b.description
    assert a.mood        != b.mood
    assert a.cost        != b.cost
    assert a.category    != b.category

def test_infoinput_zero_cost():
    e = InfoInput("Freebie", "excited", 0.0, "food")
    assert e.cost == 0.0

def test_infoinput_all_categories():
    for cat in ["food", "medical", "transpo", "utilities"]:
        e = InfoInput("Test", "okay", 50.0, cat)
        assert e.category == cat