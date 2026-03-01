const form = document.getElementById('similarityForm');
const resultDiv = document.getElementById('result');
const submitBtn = form.querySelector("button");
const loadingContainer = document.getElementById('loadingContainer');
const loadingMessage = document.getElementById('loadingMessage');
const canvas = document.getElementById('similarityCircle');
const ctx = canvas.getContext('2d');

let dotCount = 0;
let loadingInterval;

// Spinner animation
function startLoadingAnimation() {
  loadingContainer.style.display = "flex";
  dotCount = 0;
  loadingMessage.textContent = "We are analyzing your audio";
  loadingInterval = setInterval(() => {
    dotCount = (dotCount + 1) % 4;
    loadingMessage.textContent = "We are analyzing your audio" + ".".repeat(dotCount);
  }, 500);
}

function stopLoadingAnimation() {
  clearInterval(loadingInterval);
  loadingContainer.style.display = "none";
}

// Clear canvas and result
function clearSimilarityCircle() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  resultDiv.textContent = "";
  resultDiv.className = "";
}

// Draw similarity circle
function drawSimilarityCircle(score) {
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = 70;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Background circle
  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
  ctx.fillStyle = '#eee';
  ctx.fill();

  // Foreground arc
  const endAngle = 2 * Math.PI * score;
  ctx.beginPath();
  ctx.moveTo(centerX, centerY);
  ctx.arc(centerX, centerY, radius, -Math.PI/2, -Math.PI/2 + endAngle, false);
  ctx.fillStyle = score > 0.8 ? '#28a745' : '#dc3545';
  ctx.fill();

  // Inner circle to make it donut
  ctx.beginPath();
  ctx.arc(centerX, centerY, radius - 20, 0, 2 * Math.PI);
  ctx.fillStyle = '#f4f7f9';
  ctx.fill();

  // Text
  ctx.fillStyle = '#333';
  ctx.font = '20px sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(Math.round(score * 100) + '%', centerX, centerY);
}

// Clear chart when selecting new files
document.getElementById('file1').addEventListener('change', clearSimilarityCircle);
document.getElementById('file2').addEventListener('change', clearSimilarityCircle);

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const file1 = document.getElementById('file1').files[0];
  const file2 = document.getElementById('file2').files[0];

  if (!file1 || !file2) {
    resultDiv.textContent = "Please select both audio files.";
    resultDiv.className = "error";
    return;
  }

  const formData = new FormData();
  formData.append('file1', file1);
  formData.append('file2', file2);

  resultDiv.textContent = "";
  resultDiv.className = "";
  submitBtn.disabled = true;
  submitBtn.textContent = "Processing...";
  startLoadingAnimation();

  try {
    const response = await fetch('http://127.0.0.1:8000/compute_similarity/', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error("API request failed");

    const data = await response.json();
    const score = data.similarity_score;

    drawSimilarityCircle(score);

    if(score > 0.8){
      resultDiv.className = "success";
      resultDiv.textContent = `Similarity: ${Math.round(score*100)}% ✅ Likely same speaker`;
    } else {
      resultDiv.className = "error";
      resultDiv.textContent = `Similarity: ${Math.round(score*100)}% ❌ Different speaker`;
    }

  } catch (err) {
    console.error(err);
    resultDiv.textContent = "Error computing similarity.";
    resultDiv.className = "error";
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Compute Similarity";
    stopLoadingAnimation();
  }
});