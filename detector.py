import os
import json
import glob
import shutil
import joblib
import subprocess
import pandas as pd

# ==========================================
# CONFIGURAÇÃO
# ==========================================

APK_FOLDER = "input"
TEMP_FOLDER = "temp"
OUTPUT_FOLDER = "output"

MODEL_PATH = "model/rf_multiview_production.pkl"
SELECTOR_PATH = "model/variance_selector.pkl"
FEATURES_PATH = "model/feature_names.pkl"

# ==========================================
# CARREGAR MODELO
# ==========================================

model = joblib.load(MODEL_PATH)

selector = joblib.load(SELECTOR_PATH)

feature_names = joblib.load(FEATURES_PATH)

print("Modelo carregado.")

# ==========================================
# ENCONTRAR APK
# ==========================================

apk_files = glob.glob(
    os.path.join(APK_FOLDER, "*.apk")
)

if len(apk_files) == 0:
    raise Exception(
        "Nenhum APK encontrado na pasta input."
    )

apk_path = apk_files[0]

print(f"APK encontrado: {apk_path}")

# ==========================================
# PREPARAR TEMP
# ==========================================

if os.path.exists(TEMP_FOLDER):
    shutil.rmtree(
        TEMP_FOLDER,
        ignore_errors=True
    )

os.makedirs(
    TEMP_FOLDER,
    exist_ok=True
)

temp_apk_path = os.path.join(
    TEMP_FOLDER,
    os.path.basename(apk_path)
)

shutil.copy2(
    apk_path,
    temp_apk_path
)

# ==========================================
# EXECUTAR ANDROPYTOOL
# ==========================================

print("\nExecutando AndroPyTool...")

subprocess.run(
    [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{os.path.abspath(TEMP_FOLDER)}:/apks",
        "andropytool:latest",
        "-s",
        "/apks"
    ],
    check=True
)

print("Extração concluída.")

# ==========================================
# LOCALIZAR JSON
# ==========================================

json_files = glob.glob(
    os.path.join(
        TEMP_FOLDER,
        "Features_files",
        "*-analysis.json"
    )
)

if len(json_files) == 0:
    raise Exception(
        "JSON não foi gerado."
    )

json_path = json_files[0]

print(f"JSON encontrado: {json_path}")

# ==========================================
# CARREGAR JSON
# ==========================================

with open(json_path, "r") as f:
    data = json.load(f)

static = data.get(
    "Static_analysis",
    {}
)

api_calls = static.get(
    "API calls",
    {}
)

opcodes = static.get(
    "Opcodes",
    {}
)

# ==========================================
# MONTAR FEATURES
# ==========================================

row = {}

for api, count in api_calls.items():
    row[f"api_{api}"] = count

for opcode, count in opcodes.items():
    row[f"opcode_{opcode}"] = count

sample = pd.DataFrame([row])

sample = sample.reindex(
    columns=feature_names,
    fill_value=0
)

sample = selector.transform(sample)

# ==========================================
# PREDIÇÃO
# ==========================================

prediction = model.predict(sample)[0]

probabilities = model.predict_proba(sample)[0]

confidence = max(probabilities) * 100

# ==========================================
# RESULTADO
# ==========================================

print("\n==========================")
print("ANDROID MALWARE DETECTOR")
print("==========================")

print(f"\nResultado : {prediction}")
print(f"Confiança : {confidence:.2f}%")

# ==========================================
# SALVAR CSV
# ==========================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

apk_name = os.path.basename(apk_path)

resultado_df = pd.DataFrame([{

    "APK": apk_name,

    "Classificacao": prediction,

    "Confianca": round(confidence, 2),

    "APIs": len(api_calls),

    "Opcodes": len(opcodes)

}])

csv_path = os.path.join(
    OUTPUT_FOLDER,
    "resultado.csv"
)

if os.path.exists(csv_path):

    resultado_df.to_csv(
        csv_path,
        mode="a",
        header=False,
        index=False
    )

else:

    resultado_df.to_csv(
        csv_path,
        index=False
    )

print(
    f"\nResultado salvo em: {csv_path}"
)

# ==========================================
# LIMPEZA
# ==========================================

print("\nRemovendo arquivos temporários...")

try:

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.path.abspath(TEMP_FOLDER)}:/apks",
            "alpine:latest",
            "sh",
            "-c",
            "rm -rf /apks/*"
        ],
        check=True
    )

except Exception as e:

    print(
        f"\nAviso durante limpeza Docker: {e}"
    )

shutil.rmtree(
    TEMP_FOLDER,
    ignore_errors=True
)

print("\nArquivos temporários removidos.")