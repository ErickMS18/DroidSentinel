# DroidSentinel

Detector de malware Android baseado em Machine Learning.

O sistema recebe um APK, extrai suas características utilizando o AndroPyTool e realiza a classificação entre:

* Malware
* Goodware

## Requisitos

* Python 3.9+
* Docker
* Imagem Docker do AndroPyTool

## Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/DroidSentinel.git
cd DroidSentinel
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

ou

```bash
conda env create -f environment.yml
conda activate ml_gpu_ds
```

Baixe a imagem do AndroPyTool:

```bash
docker pull alexmyg/andropytool:latest
docker tag alexmyg/andropytool:latest andropytool:latest
```

## Utilização

Coloque um APK dentro da pasta:

```text
input/
```

Execute:

```bash
python detector.py
```

Exemplo de saída:

```text
Resultado : malware
Confiança : 98.31%
```

Os resultados são armazenados em:

```text
output/resultado.csv
```

## Estrutura

```text
DroidSentinel
│
├── detector.py
├── model/
├── input/
├── output/
├── requirements.txt
└── environment.yml
```

## Observação

A versão atual utiliza o AndroPyTool para extração de features. Futuras versões substituirão essa dependência por um pipeline próprio de extração de características.
