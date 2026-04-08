const statusBox = document.getElementById("statusBox");
const summaryBox = document.getElementById("summaryBox");
const detailsBox = document.getElementById("detailsBox");
const agentsBox = document.getElementById("agentsBox");

const metricTasks = document.getElementById("metricTasks");
const metricBlocks = document.getElementById("metricBlocks");
const metricWeak = document.getElementById("metricWeak");
const metricScore = document.getElementById("metricScore");

const tasksList = document.getElementById("tasksList");
const blocksList = document.getElementById("blocksList");
const notesList = document.getElementById("notesList");

let currentInterviewPrompt = "";

function showTab(tabName) {
  document.querySelectorAll(".tab").forEach(btn => btn.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(panel => panel.classList.remove("active"));

  const tabMap = { plan: 0, analyze: 1, replan: 2, live: 3 };
  document.querySelectorAll(".tab")[tabMap[tabName]].classList.add("active");
  document.getElementById(`tab-${tabName}`).classList.add("active");
}

function setStatus(text) {
  statusBox.textContent = text;
}

function setAgents(agents = []) {
  agentsBox.innerHTML = "";
  if (!agents.length) {
    agentsBox.innerHTML = `<span class="chip">OrchestratorAgent</span>`;
    return;
  }

  agents.forEach(agent => {
    const span = document.createElement("span");
    span.className = "chip";
    span.textContent = agent;
    agentsBox.appendChild(span);
  });
}

function formatList(items) {
  if (!items || !items.length) return "<p class='muted'>No items available.</p>";
  return `<ul>${items.map(item => `<li>${item}</li>`).join("")}</ul>`;
}

function setScore(score) {
  metricScore.textContent = score ?? "-";
  metricScore.className = "";

  if (typeof score === "number") {
    if (score >= 8) metricScore.classList.add("score-good");
    else if (score >= 6) metricScore.classList.add("score-mid");
    else metricScore.classList.add("score-low");
  }
}

async function createPlan() {
  const body = {
    user_id: document.getElementById("plan-user").value,
    target_role: document.getElementById("plan-role").value,
    company: document.getElementById("plan-company").value,
    timeline_days: Number(document.getElementById("plan-days").value),
    focus_areas: document.getElementById("plan-focus").value.split(",").map(s => s.trim()).filter(Boolean)
  };

  setStatus("Generating prep plan...");

  const res = await fetch("/prep-plan", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });

  const data = await res.json();

  summaryBox.innerHTML = `
    <p><strong>${data.message}</strong></p>
    <p>Created a personalized prep roadmap for <strong>${body.target_role}</strong> at <strong>${body.company}</strong>.</p>
    <p>Generated <strong>${data.tasks_created || 0}</strong> tasks and <strong>${data.calendar_blocks_created || 0}</strong> study blocks.</p>
    <p><strong>Tools used:</strong> ${(data.tools_used || []).join(", ")}</p>
  `;

  const days = (data.daily_plan || []).map(day => `Day ${day.day}: ${day.topics.join(", ")}`);
  detailsBox.innerHTML = `<p><strong>Generated Daily Plan</strong></p>${formatList(days)}`;

  metricTasks.textContent = data.tasks_created || 0;
  metricBlocks.textContent = data.calendar_blocks_created || 0;
  metricWeak.textContent = 0;
  setScore("-");

  setAgents(data.agents_used || []);
  setStatus("Prep plan ready");
}

async function analyzeMock() {
  const body = {
    user_id: document.getElementById("analyze-user").value,
    question_type: document.getElementById("analyze-type").value,
    prompt: document.getElementById("analyze-prompt").value,
    answer_text: document.getElementById("analyze-answer").value
  };

  setStatus("Analyzing answer...");

  const res = await fetch("/analyze", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });

  const data = await res.json();

  summaryBox.innerHTML = `
    <p><strong>${data.message}</strong></p>
    <p>Readiness score: <strong>${data.score}/10</strong></p>
    <p>${data.summary || ""}</p>
    <p><strong>Tools used:</strong> ${(data.tools_used || []).join(", ")}</p>
  `;

  detailsBox.innerHTML = `
    <p><strong>Strengths</strong></p>
    ${formatList(data.strengths || [])}
    <p><strong>Weak Areas</strong></p>
    ${formatList(data.weak_areas || [])}
    <p><strong>Follow-up Tasks</strong></p>
    ${formatList(data.follow_up_tasks || [])}
  `;

  metricWeak.textContent = (data.weak_areas || []).length;
  setScore(data.score || "-");
  setAgents(data.agents_used || []);
  setStatus("Mock analysis complete");
}

async function replanPrep() {
  const body = {
    user_id: document.getElementById("replan-user").value,
    missed_days: Number(document.getElementById("replan-days").value)
  };

  setStatus("Replanning...");

  const res = await fetch("/replan", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });

  const data = await res.json();

  summaryBox.innerHTML = `
    <p><strong>${data.message}</strong></p>
    <p>Your preparation flow was adjusted after missed study days.</p>
    <p><strong>Tools used:</strong> ${(data.tools_used || []).join(", ")}</p>
  `;

  detailsBox.innerHTML = `
    <p><strong>Updated Focus Areas</strong></p>
    ${formatList(data.new_focus || [])}
  `;

  setAgents(data.agents_used || []);
  setStatus("Replan ready");
}

async function startMockInterview() {
  const body = {
    user_id: document.getElementById("live-user").value,
    interview_type: document.getElementById("live-type").value
  };

  setStatus("Starting mock interview...");

  const res = await fetch("/mock-interview/start", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });

  const data = await res.json();

  currentInterviewPrompt = data.prompt || "";
  document.getElementById("live-question").textContent = currentInterviewPrompt;

  summaryBox.innerHTML = `
    <p><strong>${data.message}</strong></p>
    <p>Interview type: <strong>${data.interview_type}</strong></p>
    <p><strong>Tools used:</strong> ${(data.tools_used || []).join(", ")}</p>
  `;

  detailsBox.innerHTML = `
    <p><strong>Current Question</strong></p>
    <p>${currentInterviewPrompt}</p>
  `;

  setAgents(data.agents_used || []);
  setStatus("Mock interview started");
}

async function evaluateMockInterview() {
  const body = {
    user_id: document.getElementById("live-user").value,
    interview_type: document.getElementById("live-type").value,
    prompt: currentInterviewPrompt,
    answer_text: document.getElementById("live-answer").value
  };

  setStatus("Evaluating interview answer...");

  const res = await fetch("/mock-interview/evaluate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });

  const data = await res.json();

  summaryBox.innerHTML = `
    <p><strong>${data.message}</strong></p>
    <p>Interview response score: <strong>${data.score}/10</strong></p>
    <p>${data.summary || ""}</p>
    <p><strong>Tools used:</strong> ${(data.tools_used || []).join(", ")}</p>
  `;

  detailsBox.innerHTML = `
    <p><strong>Strengths</strong></p>
    ${formatList(data.strengths || [])}
    <p><strong>Weak Areas</strong></p>
    ${formatList(data.weak_areas || [])}
    <p><strong>Follow-up Tasks</strong></p>
    ${formatList(data.follow_up_tasks || [])}
  `;

  metricWeak.textContent = (data.weak_areas || []).length;
  setScore(data.score || "-");
  setAgents(data.agents_used || []);
  setStatus("Interview evaluation complete");
}

async function loadDashboard() {
  const userId =
    document.getElementById("plan-user").value ||
    document.getElementById("analyze-user").value ||
    document.getElementById("replan-user").value ||
    document.getElementById("live-user").value ||
    "sony_1";

  setStatus("Loading dashboard...");

  const res = await fetch(`/user/${userId}/dashboard`);
  const data = await res.json();

  const tasks = (data.tasks || []).slice(0, 6).map(t => t.title || "Untitled task");
  const blocks = (data.calendar_blocks || []).slice(0, 6).map(b => `${b.title} (${b.date})`);
  const notes = (data.notes || []).slice(0, 6).map(n => `${n.topic}: ${n.content}`);

  tasksList.innerHTML = tasks.length ? tasks.map(t => `<li>${t}</li>`).join("") : `<li class="muted">No tasks yet</li>`;
  blocksList.innerHTML = blocks.length ? blocks.map(b => `<li>${b}</li>`).join("") : `<li class="muted">No calendar blocks yet</li>`;
  notesList.innerHTML = notes.length ? notes.map(n => `<li>${n}</li>`).join("") : `<li class="muted">No notes yet</li>`;

  summaryBox.innerHTML = `
    <p><strong>Dashboard loaded successfully.</strong></p>
    <p>Fetched persisted tasks, calendar blocks, and notes for <strong>${userId}</strong>.</p>
  `;

  detailsBox.innerHTML = `
    <p><strong>Stored Data Summary</strong></p>
    <ul>
      <li>Prep plans: ${(data.prep_plans || []).length}</li>
      <li>Tasks: ${(data.tasks || []).length}</li>
      <li>Calendar blocks: ${(data.calendar_blocks || []).length}</li>
      <li>Notes: ${(data.notes || []).length}</li>
      <li>Mock sessions: ${(data.mock_sessions || []).length}</li>
    </ul>
  `;

  metricTasks.textContent = (data.tasks || []).length;
  metricBlocks.textContent = (data.calendar_blocks || []).length;
  metricWeak.textContent = (data.notes || []).length;

  setStatus("Dashboard ready");
}