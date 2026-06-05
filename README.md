# DroidSentinel

Detector de malware Android baseado em Machine Learning.

O sistema recebe um APK, extrai características estáticas utilizando o AndroPyTool e realiza a classificação entre:

* Malware
* Goodware

## Requisitos

* Python 3.9+
* Docker Desktop (Windows) ou Docker Engine (Linux)
* Imagem Docker do AndroPyTool

## Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/DroidSentinel.git
cd DroidSentinel
```

Instale as dependências utilizando uma das opções abaixo.

### Opção 1 - pip

```bash
pip install -r requirements.txt
```

### Opção 2 - Conda

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

## Resultado CSV

Cada execução adiciona uma nova linha ao arquivo `resultado.csv`.

| Coluna        | Descrição                                                                           |
| ------------- | ----------------------------------------------------------------------------------- |
| APK           | Nome do APK analisado                                                               |
| Classificacao | Resultado da predição (malware ou goodware)                                         |
| Confianca     | Probabilidade associada à classificação                                             |
| APIs          | Quantidade de APIs distintas identificadas durante a extração de características    |
| Opcodes       | Quantidade de opcodes distintos identificados durante a extração de características |

## Estrutura

```text
DroidSentinel
│
├── detector.py
├── input/
├── model/
├── output/
├── temp/
├── requirements.txt
└── environment.yml
```

## Observações

* Apenas um APK deve estar presente na pasta `input` por execução.
* A pasta `temp` é criada e removida automaticamente durante o processamento.
* A versão atual utiliza o AndroPyTool para extração de características.
* Futuras versões substituirão essa dependência por um pipeline próprio de extração de features.
