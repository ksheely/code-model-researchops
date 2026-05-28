from app.evaluation.runner import run_python_evaluation


def test_runner_passes_valid_solution():
    submitted_code = '''
def add(a, b):
    return a + b
'''
    tests_code = '''
from solution import add

def test_add():
    assert add(2, 3) == 5
'''
    result = run_python_evaluation(submitted_code, tests_code)
    assert result["passed"] is True
    assert result["score"] == 1.0


def test_runner_fails_invalid_solution():
    submitted_code = '''
def add(a, b):
    return a - b
'''
    tests_code = '''
from solution import add

def test_add():
    assert add(2, 3) == 5
'''
    result = run_python_evaluation(submitted_code, tests_code)
    assert result["passed"] is False
    assert result["score"] == 0.0
