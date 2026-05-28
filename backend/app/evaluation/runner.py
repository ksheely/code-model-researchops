import subprocess
import tempfile
from pathlib import Path


def run_python_evaluation(submitted_code: str, tests_code: str) -> dict:
    '''
    Writes submitted code and tests into a temporary directory,
    runs pytest, and returns a structured result.

    Expected convention:
    - Submitted code is saved as solution.py
    - Tests import from solution.py
    '''
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        solution_file = tmp_path / "solution.py"
        test_file = tmp_path / "test_solution.py"

        solution_file.write_text(submitted_code, encoding="utf-8")
        test_file.write_text(tests_code, encoding="utf-8")

        result = subprocess.run(
            ["python", "-m", "pytest", "-q", str(test_file)],
            cwd=tmp_path,
            text=True,
            capture_output=True,
            timeout=10,
        )

        output = (result.stdout or "") + "\n" + (result.stderr or "")
        passed = result.returncode == 0

        # Simple score for starter version.
        # Upgrade idea: parse pytest output for partial scoring.
        score = 1.0 if passed else 0.0

        return {
            "passed": passed,
            "score": score,
            "test_output": output.strip(),
        }


def make_leadership_summary(model_name: str, task_title: str, passed: bool, score: float) -> str:
    if passed:
        return (
            f"{model_name} successfully completed '{task_title}' with a score of {score:.0%}. "
            "This task is ready for validation against broader regression coverage."
        )

    return (
        f"{model_name} did not complete '{task_title}' successfully. "
        f"Current score: {score:.0%}. Recommendation: keep in experiment status and review failure output."
    )
