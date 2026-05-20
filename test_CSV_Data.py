import os
from purrseapp import InfoInput, CSV_Data

# ── Tests for CSV_Data ────────────────────────────────────

def test_save_csv():
    csv = CSV_Data('test_save.csv')
    csv.save([InfoInput('Meds', 'worried', 300.0, 'medical')])
    assert os.path.exists('test_save.csv')
    os.remove('test_save.csv')

def test_load_count():
    csv = CSV_Data('test_count.csv')
    csv.save([
        InfoInput('Meds',    'worried', 300.0, 'medical'),
        InfoInput('Jeepney', 'tired',    25.0, 'transpo'),
    ])
    loaded = csv.load()
    assert len(loaded) == 2
    os.remove('test_count.csv')

def test_load_fields():
    csv = CSV_Data('test_fields.csv')
    csv.save([InfoInput('Meds', 'worried', 300.0, 'medical')])
    loaded = csv.load()
    assert loaded[0].description == 'Meds'
    assert loaded[0].mood        == 'worried'
    assert loaded[0].cost        == 300.0
    assert loaded[0].category    == 'medical'
    os.remove('test_fields.csv')

def test_load_missing():
    csv = CSV_Data('this_does_not_exist.csv')
    assert csv.load() == []
