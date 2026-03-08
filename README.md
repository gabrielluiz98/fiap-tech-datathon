# 🚀 Datathon: Case Passos Mágicos - Machine Learning Engineering

## 1) Visão Geral do Projeto

**Objetivo:**
Este projeto foi desenvolvido para apoiar a missão da Associação Passos Mágicos de transformar a vida de crianças e jovens. O objetivo central é prever o risco de defasagem escolar de cada estudante, permitindo intervenções pedagógicas e psicológicas preventivas.

**Solução Proposta:**
Foi construída uma pipeline completa de Machine Learning aplicando as melhores práticas de MLOps. A solução engloba a extração e limpeza dos dados históricos (2022 a 2024) , treinamento de um modelo de Regressão Logística (focado em alta revocação/recall), empacotamento em contêiner, disponibilização via API REST e um sistema integrado de monitoramento contínuo para detecção de _Data Drift_.

**Stack Tecnológica:**

- **Linguagem:** Python 3.10

- **Frameworks de ML & Dados:** `pandas`, `scikit-learn`

- **API:** `FastAPI`, `uvicorn`

- **Serialização:** `joblib`

- **Testes Unitários:** `pytest` (com cobertura superior a 80%)

- **Monitoramento:** `evidently` (geração de reports HTML e logs de predição)

- **Empacotamento:** Docker

---

## 2) Estrutura do Projeto

```text
projeto-datathon/
│
├── app/
│   └── api_principal.py          # Código da API e endpoints
│
├── modelos_salvos/               # Diretório do modelo serializado (.joblib)
│   └── modelo_regressao_logistica.joblib
│
├── src/
│   ├── pre_processamento.py      # Funções de limpeza e tratamento de features
│   ├── treinamento_modelo.py     # Lógica de divisão de dados, treino e avaliação
│   └── monitoramento.py          # Geração do painel de Drift (Evidently)
│
├── testes/
│   └── test_pre_processamento.py # Testes unitários do pipeline de dados
│
├── Dockerfile                    # Instruções para empacotamento do ambiente
├── requirements.txt              # Dependências do projeto
├── gerar_dashboard.py            # Script para execução do monitoramento de Drift
├── executar_treino.py            # Script disparador do treinamento
└── README.md                     # Documentação principal

```

---

## 3) Instruções de Deploy e Execução

Para garantir a reprodutibilidade, este projeto pode ser executado localmente ou via Docker.

**Pré-requisitos:**

- Python 3.10+ ou Docker instalado.
- Os arquivos CSV originais da base de dados devem estar na raiz do projeto.

### Opção A: Execução via Docker (Recomendado)

O Docker garante que o modelo será executado em um ambiente isolado.

1. **Construir a imagem:**

```bash
docker build -t passos-magicos-api .

```

2. **Subir o contêiner:**

```bash
docker run -d -p 8000:8000 passos-magicos-api

```

A API estará disponível em `http://localhost:8000`.

### Opção B: Execução Local (Ambiente Virtual)

1. **Instalar dependências:**

```bash
pip install -r requirements.txt

```

2. **Executar os testes unitários:**

```bash
pytest testes/ -v

```

3. **Treinar o modelo (gera o arquivo .joblib):**

```bash
python executar_treino.py

```

4. **Iniciar a API:**

```bash
uvicorn app.api_principal:aplicativo_api --host 0.0.0.0 --port 8000

```

---

## 4) Exemplos de Chamadas à API

A API expõe o endpoint `/predict`, que recebe os dados educacionais do aluno e retorna a previsão.

**Exemplo de requisição via cURL:**

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "IDA": 6.5,
  "IEG": 7.2,
  "IAA": 8.0,
  "IPS": 6.0
}'

```

**Exemplo de Resposta (Output):**

```json
{
  "risco_de_defasagem": 1,
  "mensagem": "Estudante apresenta risco de defasagem escolar."
}
```

_(Nota: O valor `1` indica risco de defasagem, enquanto `0` indica ausência de risco)._

---

## 5) Etapas do Pipeline de Machine Learning

Nossa arquitetura foi desenhada para cobrir todo o ciclo de vida do dado:

1.  **Pré-processamento dos Dados:** Carregamento dos dados de 2022, 2023 e 2024. Padronização da nomenclatura da variável alvo (`Defas` para `Defasagem`) e tratamento de separadores decimais (conversão de vírgulas para pontos float).

2.  **Engenharia de Features:** Seleção das variáveis mais explicativas definidas no dicionário de dados: IDA (Aprendizagem), IEG (Engajamento), IAA (Auto Avaliação) e IPS (Psicossocial).

3.  **Treinamento e Validação:** Divisão da base em 80% treino e 20% teste. O modelo escolhido foi a **Regressão Logística** devido à sua alta interpretabilidade e velocidade de inferência.

4.  **Avaliação do Modelo:** A métrica principal de negócio priorizada foi a **Revocação (Recall)**. No contexto educacional, minimizar falsos negativos (não identificar um aluno que precisa de ajuda) é muito mais crítico do que minimizar falsos positivos.

5.  **Monitoramento Contínuo (Drift):** A API salva em tempo real os dados recebidos em um log (arquivo CSV). Através do script `gerar_dashboard.py`, a biblioteca `Evidently` compara a distribuição desses novos dados com a base histórica de treino, gerando um painel HTML interativo (`monitoramento_drift_estudantes.html`) para monitoramento de _Data Drift_.
# fiap-tech-datathon
