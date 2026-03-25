<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐈 猫翻訳AI リアルタイム</title>
<style>
  body { font-family: sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; background: #1a1a2e; color: white; }
  h1 { text-align: center; font-size: 2em; }
  .btn { width: 100%; padding: 20px; font-size: 1.5em; border: none; border-radius: 15px; cursor: pointer; margin: 10px 0; }
  .start { background: #e94560; color: white; }
  .stop { background: #444; color: white; }
  .result { background: #16213e; border-radius: 15px; padding: 20px; margin: 10px 0; text-align: center; }
  .emotion { font-size: 2em; margin: 10px 0; }
  .message { font-size: 1.2em; color: #a8d8ea; }
  .meter { background: #333; border-radius: 10px; height: 20px; margin: 5px 0; overflow: hidden; }
  .meter-fill { height: 100%; border-radius: 10px; transition: width 0.1s; background: linear-gradient(90deg, #e94560, #f5a623); }
  .stats { display: flex; gap: 10px; margin: 10px 0; }
  .stat { flex: 1; background: #16213e; border-radius: 10px; padding: 10px; text-align: center; }
  .stat-value { font-size: 1.5em; font-weight: bold; color: #e94560; }
  canvas { width: 100%; height: 100px; background: #16213e; border-radius: 10px; display: block; margin: 10px 0; }
  .history { background: #16213e; border-radius: 15px; padding: 15px; margin: 10px 0; max-height: 200px; overflow-y: auto; }
  .history-item { padding: 5px 0; border-bottom: 1px solid #333; font-size: 0.9em; }
  .recording { animation: pulse 1s infinite; }
  @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.5; } }
</style>
</head>
<body>

<h1>🐈 猫翻訳AI</h1>
<p style="text-align:center">猫の声をリアルタイム解析します</p>

<canvas id="waveform"></canvas>

<div class="result" id="result">
  <div class="emotion" id="emotion">🐱</div>
  <div class="message" id="message">録音ボタンを押してください</div>
  <div style="margin:10px 0">信頼度</div>
  <div class="meter"><div class="meter-fill" id="confidence-bar" style="width:0%"></div></div>
  <div id="confidence-text">0%</div>
</div>

<div class="stats">
  <div class="stat">
    <div>🎵 ピッチ</div>
    <div class="stat-value" id="pitch-val">- Hz</div>
  </div>
  <div class="stat">
    <div>🔊 音量</div>
    <div class="stat-value" id="energy-val">-</div>
  </div>
  <div class="stat">
    <div>📊 解析回数</div>
    <div class="stat-value" id="count-val">0</div>
  </div>
</div>

<button class="btn start" id="startBtn" onclick="startRecording()">🎙 録音開始</button>
<button class="btn stop" id="stopBtn" onclick="stopRecording()" style="display:none">⏹ 録音停止</button>

<div class="history" id="history">
  <strong>📋 翻訳履歴</strong><br>
</div>

<script>
let audioContext, analyser, microphone, scriptProcessor;
let isRecording = false;
let analyzeCount = 0;
const canvas = document.getElementById('waveform');
const ctx = canvas.getContext('2d');
canvas.width = canvas.offsetWidth * 2;
canvas.height = 200;

// 猫声を解析する関数
function analyzeCatVoice(pitchHz, energy) {
  let emotion, message, confidence;
  if (pitchHz > 800) {
    emotion = "😾 怒り・警戒";
    message = "「あっちいけ！」「触らないで！」";
    confidence = 0.85;
  } else if (pitchHz > 500 && energy > 0.05) {
    emotion = "😺 要求・お腹すいた";
    message = "「ごはんちょうだい！」「遊んで！」";
    confidence = 0.80;
  } else if (pitchHz > 300 && energy < 0.03) {
    emotion = "😸 甘え・満足";
    message = "「なでて〜」「気持ちいい〜」";
    confidence = 0.75;
  } else if (energy < 0.02) {
    emotion = "😴 静か・リラックス";
    message = "「zzz...」「眠いにゃ」";
    confidence = 0.70;
  } else {
    emotion = "🐱 おしゃべり";
    message = "「にゃにゃにゃ〜」";
    confidence = 0.60;
  }
  return { emotion, message, confidence };
}

// 録音開始
async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new AudioContext();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048;
    microphone = audioContext.createMediaStreamSource(stream);
    scriptProcessor = audioContext.createScriptProcessor(2048, 1, 1);

    microphone.connect(analyser);
    analyser.connect(scriptProcessor);
    scriptProcessor.connect(audioContext.destination);

    isRecording = true;
    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'block';
    document.getElementById('emotion').classList.add('recording');

    let frameCount = 0;
    // リアルタイム処理
    scriptProcessor.onaudioprocess = function(e) {
      const inputData = e.inputBuffer.getChannelData(0);

      // 音量計算
      let sum = 0;
      for (let i = 0; i < inputData.length; i++) sum += inputData[i] * inputData[i];
      const energy = Math.sqrt(sum / inputData.length);

      // ピッチ推定（簡易版）
      const pitch = estimatePitch(inputData, audioContext.sampleRate);

      // 波形描画
      drawWaveform(inputData);

      // 0.5秒ごとに解析（毎フレームだと重い）
      frameCount++;
      if (frameCount % 12 === 0 && energy > 0.01) {
        const result = analyzeCatVoice(pitch, energy);
        updateDisplay(pitch, energy, result);
      }
    };
  } catch(e) {
    alert('マイクへのアクセスを許可してください！');
  }
}

// ピッチ推定（自己相関法）
function estimatePitch(buffer, sampleRate) {
  const SIZE = buffer.length;
  let maxCorr = 0, bestOffset = -1;
  for (let offset = 20; offset < SIZE / 2; offset++) {
    let corr = 0;
    for (let i = 0; i < SIZE / 2; i++) corr += buffer[i] * buffer[i + offset];
    if (corr > maxCorr) { maxCorr = corr; bestOffset = offset; }
  }
  return bestOffset > 0 ? sampleRate / bestOffset : 0;
}

// 波形を描画
function drawWaveform(data) {
  ctx.fillStyle = '#16213e';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#e94560';
  ctx.lineWidth = 2;
  ctx.beginPath();
  const sliceWidth = canvas.width / data.length;
  let x = 0;
  for (let i = 0; i < data.length; i++) {
    const y = (data[i] * canvas.height / 2) + canvas.height / 2;
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    x += sliceWidth;
  }
  ctx.stroke();
}

// 画面を更新
function updateDisplay(pitch, energy, result) {
  analyzeCount++;
  document.getElementById('emotion').textContent = result.emotion;
  document.getElementById('message').textContent = result.message;
  document.getElementById('confidence-bar').style.width = (result.confidence * 100) + '%';
  document.getElementById('confidence-text').textContent = (result.confidence * 100).toFixed(0) + '%';
  document.getElementById('pitch-val').textContent = pitch.toFixed(0) + ' Hz';
  document.getElementById('energy-val').textContent = energy.toFixed(3);
  document.getElementById('count-val').textContent = analyzeCount;

  // 履歴に追加
  const now = new Date().toLocaleTimeString('ja-JP');
  const history = document.getElementById('history');
  const item = document.createElement('div');
  item.className = 'history-item';
  item.textContent = `${now} ${result.emotion} → ${result.message}`;
  history.appendChild(item);
  history.scrollTop = history.scrollHeight;
}

// 録音停止
function stopRecording() {
  isRecording = false;
  if (scriptProcessor) scriptProcessor.disconnect();
  if (microphone) microphone.disconnect();
  if (audioContext) audioContext.close();
  document.getElementById('startBtn').style.display = 'block';
  document.getElementById('stopBtn').style.display = 'none';
  document.getElementById('emotion').classList.remove('recording');
}
</script>
</body>
</html>
```

**③ 「Commit changes」で保存**

**④ GitHub Pagesを有効にする**

リポジトリの **Settings → Pages → Branch: main → Save**

---

## 完成後のURL
```
https://lemlemray.github.io/catvoice/
