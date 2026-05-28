import React, { useEffect, useMemo, useState } from "react";
import { CheckCircle, FlaskConical, Rocket, XCircle } from "lucide-react";
import { evaluateSubmission, fetchTasks } from "./lib/api";
import "./styles.css";

const starterFallback = `def fizzbuzz(n: int) -> list[str]:
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
`;

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [selectedTaskId, setSelectedTaskId] = useState(null);
  const [modelName, setModelName] = useState("manual_submission");
  const [submittedCode, setSubmittedCode] = useState(starterFallback);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTasks().then((items) => {
      setTasks(items);
      if (items.length > 0) {
        setSelectedTaskId(items[0].id);
        setSubmittedCode(items[0].starter_code);
      }
    });
  }, []);

  const selectedTask = useMemo(
    () => tasks.find((task) => task.id === Number(selectedTaskId)),
    [tasks, selectedTaskId]
  );

  function handleTaskChange(event) {
    const task = tasks.find((item) => item.id === Number(event.target.value));
    setSelectedTaskId(task.id);
    setSubmittedCode(task.starter_code);
    setResult(null);
  }

  async function handleEvaluate() {
    setLoading(true);
    setResult(null);

    try {
      const data = await evaluateSubmission({
        task_id: Number(selectedTaskId),
        model_name: modelName,
        submitted_code: submittedCode,
      });

      setResult(data);
    } catch (error) {
      setResult({
        passed: false,
        score: 0,
        test_output: error.message,
        leadership_summary: "Evaluation could not be completed.",
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Portfolio Project</p>
          <h1>Code Model ResearchOps Dashboard</h1>
          <p>
            Evaluate coding model outputs, capture test results, and summarize
            release-readiness for research and leadership audiences.
          </p>
        </div>
        <div className="heroCard">
          <Rocket />
          <strong>Research → Release</strong>
          <span>Experiment tracking for AI coding assistants</span>
        </div>
      </section>

      <section className="grid">
        <div className="card">
          <h2>
            <FlaskConical size={20} /> Coding Task
          </h2>

          <label>Task</label>
          <select value={selectedTaskId || ""} onChange={handleTaskChange}>
            {tasks.map((task) => (
              <option value={task.id} key={task.id}>
                {task.title}
              </option>
            ))}
          </select>

          {selectedTask && (
            <div className="taskDetails">
              <span>{selectedTask.category}</span>
              <span>{selectedTask.difficulty}</span>
              <span>{selectedTask.status}</span>
            </div>
          )}

          <h3>Prompt</h3>
          <pre className="prompt">{selectedTask?.prompt}</pre>

          <label>Model name</label>
          <input
            value={modelName}
            onChange={(event) => setModelName(event.target.value)}
            placeholder="mistral-code-model-v1"
          />
        </div>

        <div className="card">
          <h2>Submitted Code</h2>
          <textarea
            value={submittedCode}
            onChange={(event) => setSubmittedCode(event.target.value)}
            spellCheck="false"
          />
          <button onClick={handleEvaluate} disabled={loading || !selectedTaskId}>
            {loading ? "Evaluating..." : "Run Evaluation"}
          </button>
        </div>
      </section>

      {result && (
        <section className="card result">
          <h2>
            {result.passed ? <CheckCircle /> : <XCircle />}
            Evaluation Result
          </h2>

          <div className="score">
            <strong>{Math.round(result.score * 100)}%</strong>
            <span>{result.passed ? "Passed" : "Needs review"}</span>
          </div>

          <h3>Leadership Summary</h3>
          <p>{result.leadership_summary}</p>

          <h3>Researcher Output</h3>
          <pre>{result.test_output}</pre>
        </section>
      )}
    </main>
  );
}
