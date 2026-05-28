const API_BASE = "http://127.0.0.1:8000";

export async function fetchTasks() {
  const response = await fetch(`${API_BASE}/tasks`);
  if (!response.ok) throw new Error("Failed to fetch tasks");
  return response.json();
}

export async function evaluateSubmission(payload) {
  const response = await fetch(`${API_BASE}/evaluate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) throw new Error("Evaluation failed");
  return response.json();
}

export async function fetchRuns() {
  const response = await fetch(`${API_BASE}/runs`);
  if (!response.ok) throw new Error("Failed to fetch runs");
  return response.json();
}
