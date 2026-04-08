const canvas = document.getElementById("networkCanvas");
const ctx = canvas.getContext("2d");

let width = 0;
let height = 0;
let nodes = [];
const NODE_COUNT = 42;
const MAX_DIST = 170;
let mouse = { x: -9999, y: -9999 };

function resizeCanvas() {
  width = window.innerWidth;
  height = window.innerHeight;
  const dpr = window.devicePixelRatio || 1;

  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

  createNodes();
}

function random(min, max) {
  return Math.random() * (max - min) + min;
}

function createNodes() {
  nodes = [];
  for (let i = 0; i < NODE_COUNT; i++) {
    nodes.push({
      x: random(0, width),
      y: random(0, height),
      vx: random(-0.22, 0.22),
      vy: random(-0.22, 0.22),
      r: random(1.8, 3.8),
      pulse: random(0, Math.PI * 2)
    });
  }
}

function updateNodes() {
  for (const n of nodes) {
    n.x += n.vx;
    n.y += n.vy;
    n.pulse += 0.02;

    if (n.x <= 0 || n.x >= width) n.vx *= -1;
    if (n.y <= 0 || n.y >= height) n.vy *= -1;

    const dx = mouse.x - n.x;
    const dy = mouse.y - n.y;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist < 140) {
      n.x -= dx * 0.002;
      n.y -= dy * 0.002;
    }
  }
}

function drawLinks() {
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i];
      const b = nodes[j];
      const dx = a.x - b.x;
      const dy = a.y - b.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < MAX_DIST) {
        const alpha = 1 - dist / MAX_DIST;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = `rgba(120, 155, 255, ${alpha * 0.22})`;
        ctx.lineWidth = alpha * 1.4;
        ctx.stroke();
      }
    }
  }
}

function drawNodes() {
  for (const n of nodes) {
    const glow = 0.55 + Math.sin(n.pulse) * 0.25;

    ctx.beginPath();
    ctx.arc(n.x, n.y, n.r + glow, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(122, 92, 255, 0.12)";
    ctx.fill();

    ctx.beginPath();
    ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(151, 189, 255, 0.95)";
    ctx.fill();
  }
}

function drawMouseGlow() {
  const gradient = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, 180);
  gradient.addColorStop(0, "rgba(79,124,255,0.10)");
  gradient.addColorStop(1, "rgba(79,124,255,0)");
  ctx.fillStyle = gradient;
  ctx.beginPath();
  ctx.arc(mouse.x, mouse.y, 180, 0, Math.PI * 2);
  ctx.fill();
}

function animate() {
  ctx.clearRect(0, 0, width, height);
  updateNodes();
  drawLinks();
  drawNodes();

  if (mouse.x > -1000) {
    drawMouseGlow();
  }

  requestAnimationFrame(animate);
}

window.addEventListener("resize", resizeCanvas);

window.addEventListener("mousemove", (e) => {
  mouse.x = e.clientX;
  mouse.y = e.clientY;
});

window.addEventListener("mouseleave", () => {
  mouse.x = -9999;
  mouse.y = -9999;
});

resizeCanvas();
animate();