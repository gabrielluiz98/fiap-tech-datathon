import pandas as pd
import os
from src.pre_processamento import limpar_e_filtrar_dados
from src.monitoramento import gerar_painel_de_monitoramento

print("Carregando base de referência histórica...")
# Carregando dados que foram usados no treinamento.
df_2022 = pd.read_csv("dados/BASE DE DADOS PEDE 2024 - DATATHON - PEDE2022.csv", sep=',').rename(columns={'Defas': 'Defasagem'})
df_2023 = pd.read_csv("dados/BASE DE DADOS PEDE 2024 - DATATHON - PEDE2023.csv", sep=',')
df_2024 = pd.read_csv("dados/BASE DE DADOS PEDE 2024 - DATATHON - PEDE2024.csv", sep=',')

# Juntando e limpando dados
dados_brutos_referencia = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)
dados_referencia = limpar_e_filtrar_dados(dados_brutos_referencia)

# Base com dados novos
caminho_producao = "dados/dados_producao_api.csv"

if not os.path.exists(caminho_producao):
    print("Ainda não há dados recebidos pela API para gerar o monitoramento.")
else:
    print("Carregando dados recebidos pela API...")
    # Lendo o log gerado pela nossa API
    df_atual = pd.read_csv(caminho_producao, sep=',')
    
    # Convertendo os tipos de dados para garantir compatibilidade com a referência
    for col in ['IDA', 'IEG', 'IAA', 'IPS']:
        df_atual[col] = df_atual[col].astype(float)
    df_atual['Defasagem'] = df_atual['Defasagem'].astype(int)

    # Geração do dash
    print("Gerando relatório de monitoramento...")
    gerar_painel_de_monitoramento(dados_referencia, df_atual)