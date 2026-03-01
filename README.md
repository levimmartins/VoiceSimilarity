# Voice Similarity App

This project is a **voice similarity detection application** that analyzes audio clips to identify potential matches between speakers. It is designed as a research/hackathon demo and works entirely on anonymized or consented datasets.

---

## Overview

The app uses **audio embeddings** from two models:

1. **VostralRealTime** – Provides rich real-time audio representations capturing prosodic and acoustic features.
2. **WavLM** – A state-of-the-art speech representation model that encodes voice characteristics.

The embeddings from these two models are **concatenated** to form a combined feature vector for each audio clip. This concatenation leverages complementary strengths from both models: Vostral captures fine-grained prosodic cues, while WavLM captures broader speech patterns.

Once embeddings are concatenated, the app computes the **Euclidean distance** between feature vectors. Lower distances indicate higher similarity between speakers.

---

## Features

- Extracts embeddings from multiple audio sources
- Concatenates embeddings from VostralRealTime and WavLM
- Computes speaker similarity using Euclidean distance
- Visualizes similarity score
- Designed for **same voice, different content** detection
- Works with anonymized or consented datasets to respect privacy

---

## Usage

1. Input audio files in a supported format (WAV).  
2. The app extracts embeddings from both models.  
3. Concatenated embeddings are used to compute Euclidean distances.  
4. Similarity scores are output.

---

## Technical Notes

- Euclidean distance is used for simplicity and interpretability  
- The system is **not intended to identify real individuals**.  
- Built with FastAPI
---

## License

To update...

---

## Acknowledgements

- **VostralRealTime** – Mistral AI  
- **WavLM** – Microsoft  