from src.pre_processamento import executar_pipeline_pre_processamento
from src.treinamento_modelo import executar_pipeline_treinamento
import os

# Cria a pasta para o modelo de IA, caso ela não exista.
os.makedirs("modelos_salvos", exist_ok=True)

# Limpando os dados
print("Iniciando processamento dos arquivos CSV...")
dados_prontos = executar_pipeline_pre_processamento(
    "dados/BASE DE DADOS PEDE 2024 - DATATHON - PEDE2022.csv",
    "dados/BASE DE DADOS PEDE 2024 - DATATHON - PEDE2023.csv",
    "dados/BASE DE DADOS PEDE 2024 - DATATHON - PEDE2024.csv"
)

# Treinando e salvando
executar_pipeline_treinamento(dados_prontos, "modelos_salvos")