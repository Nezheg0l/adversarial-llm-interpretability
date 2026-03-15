
# Adversarial AI Research: Semantic Drift & Alignment Degradation

This repository contains the source code, experimental framework, and empirical data for an AI Safety research project. We investigate how Large Language Models (LLMs) can be compromised through **Multi-turn Semantic Drift**—a technique where a model-attacker subtly shifts the conversation context to bypass outbound safety filters.

## 🔬 Research Methodology
Unlike traditional "jailbreak" methods (direct attacks), our approach employs:
*   **Target (Victim):** Llama-3.1-8B-Instruct (via `llama-cpp-python`).
*   **Attacker (Red-Teamer):** DeepSeek-R1 (14B) acting as a reasoning-based adversary (using Ollama).
*   **Mechanistic Analysis:** We perform logit-based safety analysis, extracting raw token probabilities (P_refusal) to quantify the model's internal defense activation.
*   **Exploration Strategy:** Implemented Beam Search to generate multiple attack vectors at each turn, selecting the one that minimizes the target's refusal probability while maintaining semantic continuity.

## 📊 Key Findings
Our experiments (N=80+ runs) demonstrate:
1. **Logit Volatility:** Target models exhibit high sensitivity to semantic context, showing sudden spikes in refusal probabilities when specific trigger terms are detected.
2. **Semantic Stagnation:** Tight constraints on semantic drift (similarity thresholds) often lead the attacker into local minima, preventing the completion of the attack.
3. **Defense Bypass:** We successfully identified a "verification gap" where models become susceptible to prompt injection when the conversation depth increases and contextual focus drifts.

## 📂 Repository Contents
- `academic_research_suite.py`: The core experimental framework.
- `academic_results_v4_FINAL.csv`: Comprehensive dataset (ASR, P_refusal, similarity scores).
- `plot_*.png`: Visualizations of refusal trajectories and attack outcomes.

## 🚀 Getting Started
1. **Prerequisites:** Python 3.10+, CUDA-enabled GPU (RTX 3060 12GB used for development).
2. **Setup:**
   ```bash
   pip install llama-cpp-python sentence-transformers pandas matplotlib seaborn
   ```
3. **Execution:**
   ```bash
   python3 academic_research_suite.py
   ```

---
*Created as part of an independent AI Safety & Mechanistic Interpretability research project.*
