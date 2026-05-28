from purrseapp import InfoInput, MoodAnalyzer

# ── Tests for MoodAnalyzer ────────────────────────────────

def test_top_mood():
    expenses = [
        InfoInput('Lunch',  'happy', 120.0, 'food'),
        InfoInput('Dinner', 'bored',  80.0, 'food'),
        InfoInput('Bus',    'tired',  50.0, 'transpo'),
    ]
    ma = MoodAnalyzer(expenses)
    ma.analyze()
    assert ma.get_top_mood() == 'happy'

def test_mood_accumulates():
    expenses = [
        InfoInput('Lunch', 'happy',  80.0, 'food'),
        InfoInput('Snack', 'happy',  40.0, 'food'),
        InfoInput('Bus',   'tired', 200.0, 'transpo'),
    ]
    ma = MoodAnalyzer(expenses)
    ma.analyze()
    assert ma.get_top_mood() == 'tired'

def test_mood_auto_analyze():
    expenses = [InfoInput('Coffee', 'calm', 60.0, 'food')]
    ma = MoodAnalyzer(expenses)
    assert ma.get_top_mood() == 'calm'

def test_mood_empty():
    ma = MoodAnalyzer([])
    ma.analyze()
    assert ma.get_top_mood() is None
