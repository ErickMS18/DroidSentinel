<p align="center"><img src="assets/cover.png" alt="DroidSentinel: Android malware detection with machine learning" width="900"></p>

# DroidSentinel

DroidSentinel classifies Android apps as **malware** or **goodware** with machine learning.

You give it an APK file. It extracts static features with [AndroPyTool](https://github.com/alexMyG/AndroPyTool), turns the app's API calls and opcodes into a feature vector, and uses a pre-trained Random Forest model to return a verdict with a confidence score.

The tool grew out of my undergraduate research (PIBIC, PUCPR) on multi-view Android malware detection with dynamic classifier selection. The paper was accepted at CCNC 2027 (see [Research background](#research-background)).

## How it works

```text
app.apk ──► AndroPyTool (Docker) ──► API calls view ─┐
                                 └─► opcodes view ───┴─► variance-threshold selection ──► Random Forest ──► malware / goodware
```

1. The APK in `input/` is copied to a temporary folder.
2. AndroPyTool extracts the static features.
3. The API-call and opcode features are aligned with the features the model expects.
4. The variance-threshold selector and the Random Forest classify the app.
5. The result is appended to `output/resultado.csv`.
6. Temporary files are removed automatically.

## Requirements

- Python 3.9 or newer
- Docker (AndroPyTool runs in a container)
- Git

Python dependencies are listed in `requirements.txt`.

## Installation

Clone the repository:

```bash
git clone https://github.com/ErickMS18/DroidSentinel.git
cd DroidSentinel
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Or, with Conda:

```bash
conda env create -f environment.yml
conda activate ml_gpu_ds
```

### AndroPyTool

Pull the Docker image used for feature extraction:

```bash
docker pull alexmyg/andropytool:latest
docker tag alexmyg/andropytool:latest andropytool:latest
```

Check that Docker is working:

```bash
docker run hello-world
```

## Usage

Copy the APK you want to analyze into `input/`, then run:

```bash
python detector.py
```

Example output (the labels are printed in Portuguese):

```text
Resultado : malware
Confiança : 98.31%
```

`Resultado` is the verdict and `Confiança` is the model's confidence in it.

## Output

Every run appends one line to `output/resultado.csv`:

| Column | Description |
| --- | --- |
| `APK` | Name of the analyzed APK |
| `Classificacao` | Predicted class (malware or goodware) |
| `Confianca` | Confidence of the prediction |
| `APIs` | Number of distinct API calls found in the app |
| `Opcodes` | Number of distinct opcodes found in the app |

## Model files

The classification artifacts live in `model/`:

| File | Role |
| --- | --- |
| `rf_multiview_production.pkl` | Random Forest model used for classification |
| `variance_selector.pkl` | Feature selector applied before classification |
| `feature_names.pkl` | List of features the model expects |

## Project structure

```text
DroidSentinel/
├── detector.py         # entry point: extraction, classification, CSV log
├── model/              # trained model and preprocessing artifacts
├── input/              # put the APK to analyze here
├── output/             # results (resultado.csv)
├── requirements.txt
├── environment.yml
└── .gitignore
```

## Research background

DroidSentinel comes from the research project *Multi-view Android malware detection with dynamic classifier selection*, carried out with Jhonatan Geremias and Prof. Eduardo Viegas at PUCPR.

- **Dataset:** 4,466 Android apps from AndroZoo, balanced between malware and goodware.
- **Views:** API calls and opcodes extracted statically with AndroPyTool, with variance-threshold feature selection.
- **Classifiers:** a pool of KNN, Random Forest, SVM, MLP and Naive Bayes, combined with dynamic selection methods (LCA, DES-KNN) from DESlib.
- **Result:** F1-score of 0.936 in the experiments.
- **Publication:** accepted at CCNC 2027.

The production tool ships a single Random Forest to keep it simple and fast to run.

## Roadmap

- Replace AndroPyTool with an in-house feature extraction pipeline, removing the Docker dependency.
- Batch analysis of several APKs in one run.
