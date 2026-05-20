from purrseapp import InputValidator

# ── Tests for InputValidator ──────────────────────────────

def test_valid_desc():
    v = InputValidator()
    value, error = v.validate_description('Grocery run')
    assert value == 'Grocery run'
    assert error is None

def test_empty_desc():
    v = InputValidator()
    value, error = v.validate_description('')
    assert value is None
    assert error == 'INVALID INPUT'

def test_desc_has_digits():
    v = InputValidator()
    value, error = v.validate_description('Food 3x')
    assert value is None
    assert error == 'INVALID INPUT'

def test_valid_mood():
    v = InputValidator()
    value, error = v.validate_mood('happy')
    assert value == 'happy'
    assert error is None

def test_valid_cost():
    v = InputValidator()
    value, error = v.validate_cost('150.50')
    assert value == 150.50
    assert error is None

def test_negative_cost():
    v = InputValidator()
    value, error = v.validate_cost('-5')
    assert value is None
    assert error == 'INVALID INPUT'

def test_zero_cost():
    v = InputValidator()
    value, error = v.validate_cost('0')
    assert value == 0.0
    assert error is None

def test_nonnumeric_cost():
    v = InputValidator()
    value, error = v.validate_cost('abc')
    assert value is None
    assert error == 'INVALID INPUT'
