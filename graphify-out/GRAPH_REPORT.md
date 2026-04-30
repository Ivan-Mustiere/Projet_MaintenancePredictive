# Graph Report - src  (2026-04-30)

## Corpus Check
- Corpus is ~1,188 words - fits in a single context window. You may not need a graph.

## Summary
- 45 nodes · 39 edges · 12 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Data Loading|Data Loading]]
- [[_COMMUNITY_Model Training Pipelines|Model Training Pipelines]]
- [[_COMMUNITY_Feature Engineering|Feature Engineering]]
- [[_COMMUNITY_Model Inference|Model Inference]]
- [[_COMMUNITY_TrainTest Split|Train/Test Split]]
- [[_COMMUNITY_Model Evaluation|Model Evaluation]]
- [[_COMMUNITY_Package Root|Package Root]]
- [[_COMMUNITY_Configuration|Configuration]]
- [[_COMMUNITY_Utils Package|Utils Package]]
- [[_COMMUNITY_Features Package|Features Package]]
- [[_COMMUNITY_Data Package|Data Package]]
- [[_COMMUNITY_Models Package|Models Package]]

## God Nodes (most connected - your core abstractions)
1. `build_features()` - 4 edges
2. `load_sensor()` - 4 edges
3. `_cycle_stats()` - 3 edges
4. `_fft_features()` - 3 edges
5. `load_ps2()` - 3 edges
6. `load_fs1()` - 3 edges
7. `load_profile()` - 3 edges
8. `load_target()` - 3 edges
9. `train_with_tracking()` - 3 edges
10. `split_cycles()` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Data Loading"
Cohesion: 0.24
Nodes (10): load_fs1(), load_profile(), load_ps2(), load_sensor(), load_target(), Load PS2 pressure sensor — 6000 points/cycle at 100 Hz., Load FS1 flow sensor — 600 points/cycle at 10 Hz., Load profile file containing target labels and system conditions. (+2 more)

### Community 1 - "Model Training Pipelines"
Cohesion: 0.2
Nodes (5): _cv_score(), optimize_with_optuna(), Find best hyperparameters via Optuna for the given model type., Train pipeline with cross-validation and log metrics to MLflow., train_with_tracking()

### Community 2 - "Feature Engineering"
Cohesion: 0.38
Nodes (6): build_features(), _cycle_stats(), _fft_features(), Compute FFT spectral energy features for each cycle., Build feature matrix from PS2 and FS1 sensor arrays.      Aggregates each sensor, Compute statistical features for one sensor array (n_cycles, n_points).

### Community 3 - "Model Inference"
Cohesion: 0.5
Nodes (2): predict_cycle(), Return prediction and probability for one or more cycles.

### Community 4 - "Train/Test Split"
Cohesion: 0.67
Nodes (2): Split into train (first TRAIN_CYCLES) and test (remaining).      The test set mu, split_cycles()

### Community 5 - "Model Evaluation"
Cohesion: 0.67
Nodes (0): 

### Community 6 - "Package Root"
Cohesion: 1.0
Nodes (0): 

### Community 7 - "Configuration"
Cohesion: 1.0
Nodes (0): 

### Community 8 - "Utils Package"
Cohesion: 1.0
Nodes (0): 

### Community 9 - "Features Package"
Cohesion: 1.0
Nodes (0): 

### Community 10 - "Data Package"
Cohesion: 1.0
Nodes (0): 

### Community 11 - "Models Package"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **12 isolated node(s):** `Compute statistical features for one sensor array (n_cycles, n_points).`, `Compute FFT spectral energy features for each cycle.`, `Build feature matrix from PS2 and FS1 sensor arrays.      Aggregates each sensor`, `Load a sensor file. Returns array of shape (n_cycles, n_points).`, `Load PS2 pressure sensor — 6000 points/cycle at 100 Hz.` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Package Root`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Configuration`** (1 nodes): `config.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Utils Package`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Features Package`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Data Package`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Models Package`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Compute statistical features for one sensor array (n_cycles, n_points).`, `Compute FFT spectral energy features for each cycle.`, `Build feature matrix from PS2 and FS1 sensor arrays.      Aggregates each sensor` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._