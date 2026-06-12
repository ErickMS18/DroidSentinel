# DroidSentinel

O DroidSentinel é uma ferramenta para classificação de aplicativos Android utilizando técnicas de Machine Learning.

A ferramenta recebe um arquivo APK, realiza a extração de características estáticas por meio do AndroPyTool e utiliza um modelo Random Forest previamente treinado para classificar a aplicação como **malware** ou **goodware**.

## Requisitos

Para instalar e executar o projeto é necessário possuir:

* Python 3.9 ou superior
* Docker
* Git

As dependências Python estão listadas no arquivo `requirements.txt`.

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

Opcionalmente, é possível utilizar o ambiente Conda:

```bash
conda env create -f environment.yml
conda activate ml_gpu_ds
```

## Instalação do AndroPyTool

Baixe a imagem Docker utilizada para a extração das características:

```bash
docker pull alexmyg/andropytool:latest
docker tag alexmyg/andropytool:latest andropytool:latest
```

Verifique se o Docker está funcionando corretamente:

```bash
docker run hello-world
```

## Arquivos do Modelo

Os arquivos responsáveis pela classificação estão armazenados no diretório:

```text
model/
```

Arquivos:

```text
rf_multiview_production.pkl
variance_selector.pkl
feature_names.pkl
```

Funções:

* `rf_multiview_production.pkl`: modelo Random Forest utilizado na classificação.
* `variance_selector.pkl`: seletor de características aplicado antes da classificação.
* `feature_names.pkl`: lista das features esperadas pelo modelo.

## Estrutura de Diretórios

```text
DroidSentinel/
│
├── detector.py
├── model/
├── input/
├── output/
├── requirements.txt
├── environment.yml
└── .gitignore
```

### input/

Diretório utilizado para armazenar o APK que será analisado.

### output/

Diretório onde são armazenados os resultados gerados pela ferramenta.

### model/

Contém os modelos e artefatos necessários para classificação.

## Executando a Aplicação

Copie o APK desejado para o diretório:

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

## Resultado CSV

Os resultados são armazenados em:

```text
output/resultado.csv
```

Cada execução adiciona uma nova linha ao arquivo.

| Coluna        | Descrição                                                       |
| ------------- | --------------------------------------------------------------- |
| APK           | Nome do APK analisado                                           |
| Classificacao | Resultado da predição                                           |
| Confianca     | Confiança associada à classificação                             |
| APIs          | Quantidade de APIs distintas identificadas durante a análise    |
| Opcodes       | Quantidade de opcodes distintos identificados durante a análise |

## Funcionamento

Durante a execução:

1. O APK presente em `input/` é copiado para uma área temporária.
2. O AndroPyTool realiza a extração das características estáticas.
3. As features de APIs e opcodes são processadas.
4. O modelo Random Forest realiza a classificação.
5. O resultado é salvo em `output/resultado.csv`.
6. Os arquivos temporários são removidos automaticamente.

## Observação

A versão atual utiliza o AndroPyTool para extração de características. Futuras versões do DroidSentinel deverão incorporar um pipeline próprio de extração de features, reduzindo dependências externas.
