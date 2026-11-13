<p align="center">
  <img src="./assets/banner.svg" alt="Thushanth Mahendran — AI & Data Science" width="100%" />
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/thushanth-mahendran-74a2a7214"><img src="https://img.shields.io/badge/LinkedIn-Thushanth_Mahendran-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="mailto:thushanth.20241544@iit.ac.lk"><img src="https://img.shields.io/badge/Email-Contact_Me-0D1117?style=for-the-badge&logo=gmail&logoColor=EA4335" alt="Email" /></a>
  <a href="https://github.com/Thush099?tab=repositories"><img src="https://img.shields.io/badge/Repositories-AI_%26_ML_Systems-1E293B?style=for-the-badge&logo=github&logoColor=white" alt="Repositories" /></a>
</p>

---

### About Me

- **Education:** BSc (Hons) **Artificial Intelligence & Data Science** undergraduate at **IIT Sri Lanka** (affiliated with **Robert Gordon University**)
- **Industry Experience:** Former **AI Engineering Intern at DecodeLabs** — delivered end-to-end applied ML, NLP recommender, guardrail, and OpenCV/OCR pipelines
- **Engineering Focus:** Multimodal OCR forensics & claim auditing, adversarial tool-agent evaluation, hybrid retrieval (RAG, FActScore NLI, G-Eval), streaming ML observability, and open-source ML tooling

---

### Live GitHub Activity & Language Distribution

<p align="center">
  <img src="./assets/stats.svg" alt="Thushanth Mahendran GitHub Activity, Streaks, and Languages" width="100%" />
</p>

---

### Featured Systems & Benchmarks

<p align="center">
  <a href="https://github.com/Thush099/veridoc-forensics"><img src="./assets/cards/veridoc.svg" width="49%" alt="veridoc-forensics — Multimodal OCR & Claim Verification" /></a>
  <a href="https://github.com/Thush099/traceguard-eval"><img src="./assets/cards/traceguard.svg" width="49%" alt="traceguard-eval — Adversarial Agent Evaluation" /></a>
</p>
<p align="center">
  <a href="https://github.com/Thush099/CM3604_CW"><img src="./assets/cards/cm3604.svg" width="49%" alt="CM3604_CW — FActScore NLI" /></a>
  <a href="https://github.com/Thush099/DecodeLabs-Internship"><img src="./assets/cards/decodelabs.svg" width="49%" alt="DecodeLabs-Internship — Applied AI" /></a>
</p>
<p align="center">
  <a href="https://github.com/seniruvitharanage/domain-ai"><img src="./assets/cards/domain-ai.svg" width="49%" alt="domain-ai — Task Priority ML" /></a>
  <a href="https://github.com/Thush099/CM2604-Churn-Classifier"><img src="./assets/cards/churn.svg" width="49%" alt="CM2604-Churn-Classifier" /></a>
</p>

<details>
<summary><b>View Detailed Methodology & Verified Metrics</b></summary>
<br />

| Repository | Scope & Engineering Details | Verified Results & Highlights |
| :--- | :--- | :--- |
| [**`veridoc-forensics`**](https://github.com/Thush099/veridoc-forensics) | Multimodal document auditor combining OpenCV skew/blur restoration, JPEG Q90 ELA + MAD noise tamper heatmaps, Tesseract OCR, hybrid BM25/TF-IDF claim verification, and FastAPI Studio UI | Restores degraded OCR char accuracy from `0.0%` → `99.7%` (`66.7%` → `99.9%` mean across suite), `100.0%` claim verdict & tamper accuracy, `16` passing `pytest` tests |
| [**`traceguard-eval`**](https://github.com/Thush099/traceguard-eval) | Deterministic multi-step tool-agent sandbox, adversarial prompt-injection & HTTP/JSON fault fuzzer, schema/budget guards, and FastAPI Trace Replay UI | `TraceGuardHardenedAgent` scores **`100.00`** vs `63.33` (`SchemaRetryAgent`) & `39.58` (`NaiveAgent`) on benchmark (`100.00` vs `61.00` vs `37.69` on 30-run fuzz); `17` passing `pytest` tests |
| [**`CM3604_CW`**](https://github.com/Thush099/CM3604_CW) | Automated fact-checking of LLM outputs against BM25 evidence passages with grouped CV ablations & error analysis | Majority baseline `50.68%` (`112/221`) → Lexical overlap `84.16%` (`186/221`) → Fine-tuned DeBERTa NLI `88.24%` (`195/221`) |
| [**`DecodeLabs-Internship`**](https://github.com/Thush099/DecodeLabs-Internship) | Four applied AI capstones spanning input guardrails, customer classification, TF-IDF skill-gap recommendations, and document OCR | Combines OpenCV perspective/contrast normalization with Tesseract extraction across end-to-end runnable modules |
| [**`seniruvitharanage/domain-ai`**](https://github.com/seniruvitharanage/domain-ai) | Contributed priority-scoring ML sub-pipeline merging TF-IDF developer issue text with repository & workflow metadata | Gradient Boosting model trained on `9,120` samples achieving `96.97%` accuracy & weighted F1 on `2,280` test cases |
| [**`CM2604-Churn-Classifier`**](https://github.com/Thush099/CM2604-Churn-Classifier) | Telco customer churn prediction comparing hyperparameter-tuned Decision Tree and Dropout/EarlyStopping Keras MLP | Strict train-only SMOTE oversampling to prevent data leakage under ROC-AUC and generalization-gap evaluation |

</details>

---

### Open-Source Contributions & Enhanced Forks

| Repository | Upstream Project | Engineering Contributions & Verification |
| :--- | :--- | :--- |
| [**`Thush099/chonkie`**](https://github.com/Thush099/chonkie) | [`feyninc/chonkie`](https://github.com/feyninc/chonkie) | Fixed `OverlapRefinery._split_text` & `_recursive_overlap` infinite-loop / whitespace chunk boundary bugs ([`fix/overlap-refinery-recursive-whitespace`](https://github.com/Thush099/chonkie/tree/fix/overlap-refinery-recursive-whitespace), upstream [`#681`](https://github.com/feyninc/chonkie/issues/681)); `89` refinery & recursive chunker tests pass (`4` `from_recipe` tests deselected without `huggingface_hub`) |
| [**`Thush099/cleanlab`**](https://github.com/Thush099/cleanlab) | [`cleanlab/cleanlab`](https://github.com/cleanlab/cleanlab) | Fixed `IndexError` bounds ordering in `token_classification.rank.issues_from_scores` (upstream [`#1338`](https://github.com/cleanlab/cleanlab/issues/1338)) and single-class `K == 1` `ValueError` in `rank.get_normalized_margin_for_each_label` (upstream [`#1356`](https://github.com/cleanlab/cleanlab/issues/1356)) on [`fix/rank-boundary-guards`](https://github.com/Thush099/cleanlab/tree/fix/rank-boundary-guards); `124` upstream/regression tests pass across rank, token classification, util & validation modules |
| [**`Thush099/hiring-agent`**](https://github.com/Thush099/hiring-agent) | [`interviewstreet/hiring-agent`](https://github.com/interviewstreet/hiring-agent) | Resolved scoring clamping, JSON extraction & defensive transform bugs and built [`calibration_audit.py`](https://github.com/Thush099/hiring-agent/blob/feat/offline-rubric-calibration-audit/calibration_audit.py) for offline rubric integrity (`100.0%` tier accuracy, `97.2%` evidence grounding) and counterfactual fairness auditing (`0.00` delta, `1.000` Kendall's τ) on [`feat/offline-rubric-calibration-audit`](https://github.com/Thush099/hiring-agent/tree/feat/offline-rubric-calibration-audit); `13` passing tests |

---

### ML & LLM Engineering Toolkit

A suite of standalone, modular Python packages covering retrieval, LLM faithfulness, production drift monitoring, differential privacy, causal inference, and multimodal attention — each shipped with runnable CLIs and automated `pytest` suites.

<table>
  <tr>
    <td width="50%" valign="top">
      <strong>LLM Systems &amp; Evaluation</strong>
      <ul>
        <li>
          <a href="https://github.com/Thush099/rag-pipeline"><code>rag-pipeline</code></a><br />
          <sub>Okapi BM25 + L2-normalized dense cosine retrieval, Reciprocal Rank Fusion (<code>k=60</code>), cross-encoder proximity re-ranking, and sentence-level <code>[doc_id]</code> citation grounding.</sub>
        </li>
        <li>
          <a href="https://github.com/Thush099/llm-eval-harness"><code>llm-eval-harness</code></a><br />
          <sub>Atomic claim decomposition with numeric/negation contradiction detection, rubric G-Eval scoring, and JSON/Markdown multi-model leaderboards.</sub>
        </li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <strong>ML Observability &amp; Drift Monitoring</strong>
      <ul>
        <li>
          <a href="https://github.com/Thush099/drift-detector"><code>drift-detector</code></a><br />
          <sub>Streaming concept-drift detection via Hoeffding-bound <code>ADWIN</code> and two-sided <code>Page-Hinkley</code> tests paired with adaptive <code>SGDRegressor</code> retraining.</sub>
        </li>
        <li>
          <a href="https://github.com/Thush099/drift-tracker"><code>drift-tracker</code></a><br />
          <sub>Batch feature, prediction, and data-quality observability across <code>PSI</code>, two-sample <code>KS</code>, <code>Jensen-Shannon</code> divergence, unseen category detection, and schema contracts.</sub>
        </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <strong>Data Contracts &amp; Federated Privacy</strong>
      <ul>
        <li>
          <a href="https://github.com/Thush099/data-profiler"><code>data-profiler</code></a><br />
          <sub>Semantic column inference (5 types), IQR/z-score outlier &amp; leakage audits, declarative schema validation, and prioritized dataset remediation plans.</sub>
        </li>
        <li>
          <a href="https://github.com/Thush099/fed-sim"><code>fed-sim</code></a><br />
          <sub>PyTorch <code>DP-FedAvg</code> simulator with Dirichlet non-IID client partitions, per-client L2 update clipping, calibrated Laplace/Gaussian DP noise, and drift logging.</sub>
        </li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <strong>Causal &amp; Multimodal Learning</strong>
      <ul>
        <li>
          <a href="https://github.com/Thush099/uplift-ml"><code>uplift-ml</code></a><br />
          <sub><code>S-Learner</code>, <code>T-Learner</code>, and 3-stage <code>X-Learner</code> causal CATE estimators benchmarked with Qini coefficient, AUUC, PEHE, and decile lift calibration.</sub>
        </li>
        <li>
          <a href="https://github.com/Thush099/fusion-transformer"><code>fusion-transformer</code></a><br />
          <sub>PyTorch multimodal classifier fusing <code>FT-Transformer</code> per-column feature tokenizers with transformer text encoders via bidirectional <code>nn.MultiheadAttention</code>.</sub>
        </li>
      </ul>
    </td>
  </tr>
</table>

---

### Core Stack & Tooling

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Hugging_Face-FFD21E?style=flat-square&logo=huggingface&logoColor=111827" alt="Hugging Face" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" alt="NumPy" />
  <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=111827" alt="SciPy" />
  <img src="https://img.shields.io/badge/Keras-D00000?style=flat-square&logo=keras&logoColor=white" alt="Keras" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="pytest" />
  <img src="https://img.shields.io/badge/SQL-0F766E?style=flat-square&logo=postgresql&logoColor=white" alt="SQL" />
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" alt="Git" />
</p>

<p align="center">
  <sub>Self-hosted SVG telemetry and project showcase cards generated directly from GitHub GraphQL via <a href="./scripts/generate_profile_cards.py"><code>scripts/generate_profile_cards.py</code></a>.</sub>
</p>
