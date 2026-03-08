from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from src.utils import logger_projeto
import csv
import os 

# Criação do aplicativo da API
aplicativo_api = FastAPI(
    title="Datathon - FIAP",
    description="API para estimar o risco de defasagem escolar de estudantes.",
    version="1.0.0"
)

# Local onde vai ser salvo o modelo.
CAMINHO_DO_MODELO = "modelos_salvos/modelo_regressao_logistica.joblib"

# Tenta carregar o modelo
try:
    modelo_preditivo = joblib.load(CAMINHO_DO_MODELO)
    print("Modelo de Regressão Logística carregado com sucesso na API!")
except FileNotFoundError:
    modelo_preditivo = None
    print(f"Atenção: O modelo não foi encontrado no caminho {CAMINHO_DO_MODELO}.")

# Schema da API
class DadosDoEstudante(BaseModel):
    IDA: float  # Indicador de Aprendizagem
    IEG: float  # Indicador de Engajamento
    IAA: float  # Indicador de Auto Avaliação
    IPS: float  # Indicador Psicossocial

    class Config:
        # Exemplo de preenchimento para facilitar os testes da banca avaliadora
        json_schema_extra = {
            "example": {
                "IDA": 6.5,
                "IEG": 7.2,
                "IAA": 8.0,
                "IPS": 6.0
            }
        }

@aplicativo_api.post("/predict")
def prever_risco_de_defasagem(dados_entrada: DadosDoEstudante):
    """
    Recebe os indicadores educacionais de um estudante e retorna se há risco de defasagem (1) ou não (0).
    """
    # Verifica se o modelo foi carregado
    if modelo_preditivo is None:
        raise HTTPException(
            status_code=500, 
            detail="Erro interno: O modelo preditivo não foi encontrado no servidor."
        )

    # Transformando os dados recebidos via API em um df
    dados_para_previsao = pd.DataFrame([dados_entrada.model_dump()])

    try:
        # Predict dos dados
        resultado_da_previsao = modelo_preditivo.predict(dados_para_previsao)
        
        # Convertendo o resultado em um número inteiro
        risco_calculado = int(resultado_da_previsao[0])
        
        # Gravando o que a API recebeu e o que ela respondeu
        logger_projeto.info(
            f"Previsão realizada - Dados: {dados_entrada.model_dump()} | Resultado: {risco_calculado}"
        )
        
        # Salvando os dados da API em um CSV de produção
        caminho_log_producao = "dados/dados_producao_api.csv"
        arquivo_ja_existe = os.path.isfile(caminho_log_producao)
        
        # Adiciona os valores no final do log
        with open(caminho_log_producao, mode='a', newline='') as arquivo_csv:
            escritor = csv.writer(arquivo_csv, delimiter=',')
            
            # Se o arquivo não existir, adiciona o cabeçalho.
            if not arquivo_ja_existe:
                escritor.writerow(['IDA', 'IEG', 'IAA', 'IPS', 'Defasagem'])
                
            # Gravando dados
            escritor.writerow([
                dados_entrada.IDA, 
                dados_entrada.IEG, 
                dados_entrada.IAA, 
                dados_entrada.IPS, 
                risco_calculado
            ])
        
        # Retornando a resposta em formato json
        # Avalia se o risco calculado deu positivo ou negativo e retorna a resposta de acordo com isso
        if(risco_calculado == 1):
            return {
                "risco_de_defasagem": risco_calculado,
                "mensagem": "Estudante apresenta risco de defasagem escolar"
            }
            
        else:
            return {
                "risco_de_defasagem": risco_calculado,
                "mensagem": "Estudante não apresenta risco de defasagem escolar"
            }
            
    except Exception as erro:
        # Se algo der errado na hora de calcular, retorna um erro.
        raise HTTPException(
            status_code=500, 
            detail=f"Ocorreu um erro ao tentar realizar a previsão: {str(erro)}"
        )