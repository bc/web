---
layout: default
title: "Browser-Based ML Inference Guide"
description: "Comprehensive comparison of tools and frameworks for running ML models directly in the browser."
date: 2025-11-12
permalink: /guides/browser-based-inference/
---

# Browser-Based ML Inference Guide

Run machine learning models directly in the browser without server backends. This guide compares the major frameworks and tools available.

## Complete Comparison Table

<style>
.inference-table {
  font-size: 0.85rem;
  margin: 2rem 0;
}
.inference-table th, .inference-table td {
  padding: 0.5rem;
  text-align: left;
}
.inference-table th {
  background: linear-gradient(90deg, #FF9398 0%, #49c5b6 100%);
  color: white;
  font-weight: 600;
}
.inference-table tr:nth-child(odd) {
  background: #f5f5f5;
}
.inference-table tr:hover {
  background: #e8e8e8;
}
</style>

| Tool | Type | Free? | Best For | Performance | Setup | Browser Support | Mobile Ready |
|------|------|-------|----------|-------------|-------|-----------------|--------------|
| **TensorFlow.js** | Inference | ✓ | Browser ML, real-time | ⭐⭐⭐⭐ (WebGL) | Medium | All modern | Partial |
| **ONNX Runtime Web** | Inference | ✓ | High-perf inference | ⭐⭐⭐⭐⭐ (WebGPU) | Medium | Chrome, Edge | Limited |
| **MediaPipe** | Detection | ✓ | Face/pose tracking | ⭐⭐⭐⭐ | Easy | All modern | ✓ Yes |
| **Transformers.js** | NLP | ✓ | Text models | ⭐⭐⭐ | Easy | All modern | ✓ Yes |
| **Whisper Web** | Audio | ✓ | Speech recognition | ⭐⭐⭐ | Medium | Modern | Limited |
| **Runway ML** | General | Freemium | Creative ML | ⭐⭐⭐⭐ | Easy | Web app | ✓ Yes |
| **ml.js** | Utilities | ✓ | Lightweight ML | ⭐⭐⭐ | Easy | All modern | ✓ Yes |
| **OpenCV.js** | Vision | ✓ | Computer vision | ⭐⭐⭐⭐ | Hard | All modern | Limited |
{:.inference-table}

## Detailed Breakdowns

### 1. TensorFlow.js

**Free** | **Open Source** | **JavaScript Library**

Machine learning library for JavaScript that runs in the browser and on Node.js. Essential for real-time ML applications.

**Key Features:**
- Run ML models directly in the browser (no server needed)
- GPU acceleration via WebGL or WebGPU
- Convert PyTorch/TensorFlow models to browser format
- Pre-trained models for common tasks
- Automatic differentiation for training in the browser

**Relevant to Your Work:**
- Run LipNet inference in real-time on client
- Process audio for lip-sync without server latency
- Integrate with MediaPipe for face tracking
- Optimize models with quantization for mobile

[→ TensorFlow.js Docs](https://www.tensorflow.org/js){:.button} [→ GitHub](https://github.com/tensorflow/tfjs){:.button}

---

### 2. ONNX Runtime Web

**Free** | **Open Source** | **JavaScript Library**

High-performance runtime for ONNX models in the browser with WebGPU support for next-gen performance.

**Advantages:**
- Better performance than TensorFlow.js for many models
- WebGPU support (3-5× faster than WebGL)
- Supports quantized models natively
- Works offline after model download

**Performance Metrics:**
- WebGL: 77-225ms latency (ResNet50)
- WebGPU: 30-50fps effective inference
- CPU fallback: 10-30fps effective

[→ Official Site](https://onnxruntime.ai/){:.button}

---

### 3. MediaPipe

**Free** | **Open Source** | **Multi-Platform**

Google's framework for building multimodal machine learning pipelines. Excellent for face tracking, pose detection, and hand tracking.

**Core Solutions (Relevant to Avatar Work):**
- **Face Mesh:** 468-point face landmark detection in real-time
- **Face Landmarker:** Enhanced face detection with iris tracking
- **Hand Tracking:** Real-time hand gesture recognition
- **Pose Estimation:** Full-body pose tracking

**Use Cases:**
- Real-time facial expression tracking for avatar control
- Mouth position detection for lip-sync synchronization
- Combine with LipNet for more natural mouth animation
- Mobile-friendly (works on iOS and Android)

**Performance:**
- Desktop: 30+ FPS (Chrome)
- Mobile: 15-25 FPS (Android), 6-7 FPS (iOS)

[→ Official Site](https://mediapipe.dev/){:.button}

---

### 4. Transformers.js

**Free** | **Open Source** | **JavaScript Library**

State-of-the-art NLP models run directly in the browser. Perfect for text processing without server calls.

**Available Models:**
- Text classification
- Named entity recognition
- Question answering
- Summarization
- Translation

[→ GitHub](https://github.com/xenova/transformers.js){:.button}

---

### 5. OpenCV.js

**Free** | **Open Source** | **JavaScript Binding**

JavaScript binding of OpenCV for computer vision tasks in the browser.

**Capabilities:**
- Image processing
- Feature detection
- Object tracking
- Calibration and 3D reconstruction

[→ Official Docs](https://docs.opencv.org/4.5.2/d5/d10/tutorial_js_root.html){:.button}

---

## Performance Comparison by Task

### Face Tracking (Desktop)

| Framework | FPS | Latency | Quality |
|-----------|-----|---------|---------|
| MediaPipe Face Mesh | 30+ | 30-50ms | ⭐⭐⭐⭐ |
| TensorFlow.js | 25-30 | 40-60ms | ⭐⭐⭐ |
| Custom ONNX | 30+ | 20-40ms | ⭐⭐⭐⭐⭐ |
{:.inference-table}

### Model Inference (WebGL vs WebGPU)

| Model | WebGL | WebGPU | CPU |
|-------|-------|--------|-----|
| ResNet50 | 77-225ms | 20-40ms | 500-800ms |
| MobileNet | 30-50ms | 10-20ms | 100-150ms |
| BERT | 1000-2000ms | 200-500ms | 5000-10000ms |
{:.inference-table}

### Mobile Performance (Browser)

| Framework | iOS | Android | Notes |
|-----------|-----|---------|-------|
| MediaPipe | 6-7 FPS | 15-25 FPS | Face tracking |
| TensorFlow.js | 5-10 FPS | 15-20 FPS | Model dependent |
| OpenCV.js | Limited | 10-15 FPS | Limited support |
{:.inference-table}

## Choosing the Right Tool

```
START: I want to run ML in my browser

├─ Do you need face/pose tracking?
│  ├─ YES → Use MediaPipe
│  └─ NO → Continue
│
├─ Do you need maximum performance?
│  ├─ YES → Use ONNX Runtime Web (WebGPU)
│  └─ NO → Continue
│
├─ Do you need NLP capabilities?
│  ├─ YES → Use Transformers.js
│  └─ NO → Continue
│
├─ Do you have a model to convert?
│  ├─ TensorFlow/PyTorch → Use TensorFlow.js
│  ├─ ONNX format → Use ONNX Runtime Web
│  └─ Other → Research model conversion first
│
└─ For general CV: Use OpenCV.js
```

## Implementation Tips

**For Real-Time Performance:**
1. Use quantized models (INT8/FP16)
2. Leverage GPU acceleration (WebGL/WebGPU)
3. Cache model loads
4. Use Web Workers for inference to avoid blocking UI

**For Model Conversion:**
- TensorFlow → TensorFlow.js: Use `tensorflowjs_converter`
- PyTorch → ONNX → ONNX Runtime Web
- Check model format compatibility before converting

**For Production Deployment:**
- Lazy load models
- Monitor memory usage
- Provide fallback for unsupported browsers
- Test on actual mobile devices

---

**Ready to build?** [Schedule a consultation](/meet/) or [email me](mailto:brian.cohn@kaspect.com)
