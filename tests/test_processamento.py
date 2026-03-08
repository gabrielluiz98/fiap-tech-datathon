import pandas as pd
import numpy as np
import pytest

# Importando a função que criamos no nosso arquivo principal
from src.pre_processamento import limpar_e_filtrar_dados

def test_limpar_e_filtrar_dados_cenario_completo():
    """
    Testa se a função de limpeza consegue lidar com vírgulas, 
    remover colunas desnecessárias e apagar linhas com dados faltando.
    """
    # 1. Preparando o nosso cenário de teste (Mock)
    # Simulamos como os dados costumam chegar do arquivo CSV bruto
    dados_brutos_simulados = pd.DataFrame({
        'IDA': ['8,5', '7,0', '9,2', '5,5'],    # Números com vírgula em formato de texto
        'IEG': ['7,1', '6,5', np.nan, '4,0'],   # np.nan simula um "dado em branco" (nulo)
        'IAA': [9.0, 8.0, 8.5, 6.0],            # Misturando com números normais para ver se a função lida bem
        'IPS': ['7,5', '8,0', '9,0', '5,0'],
        'Defasagem': [0.0, 1.0, 0.0, np.nan],   # Defasagem faltando na última linha
        'Coluna_Extra': ['X', 'Y', 'Z', 'W']    # Coluna inútil que não está no nosso dicionário
    })

    # 2. Rodando a função que queremos testar
    resultado_limpo = limpar_e_filtrar_dados(dados_brutos_simulados)

    # 3. VALIDAÇÃO 1: As colunas corretas foram mantidas e as extras descartadas?
    colunas_que_devem_sobrar = ['IDA', 'IEG', 'IAA', 'IPS', 'Defasagem']
    assert list(resultado_limpo.columns) == colunas_que_devem_sobrar, "As colunas filtradas não batem com o esperado."

    # 4. VALIDAÇÃO 2: As linhas com dados nulos sumiram?
    # A linha de índice 2 não tem IEG. A linha de índice 3 não tem Defasagem.
    # Das 4 linhas iniciais, só devem sobrar as 2 primeiras que estão completas.
    assert len(resultado_limpo) == 2, "As linhas com valores nulos não foram removidas corretamente."

    # 5. VALIDAÇÃO 3: As vírgulas viraram ponto decimal? 
    # O valor '8,5' da primeira linha deve ter virado o número 8.5
    # Usamos o iloc[0] para pegar a primeira linha do resultado
    assert resultado_limpo.iloc[0]['IDA'] == 8.5, "A conversão de vírgula para ponto falhou na coluna IDA."
    
    # 6. VALIDAÇÃO 4: O tipo de dado da Defasagem virou inteiro?
    # É uma exigência do nosso modelo que a variável alvo seja 0 ou 1
    assert pd.api.types.is_integer_dtype(resultado_limpo['Defasagem']), "A coluna Defasagem não foi convertida para número inteiro."


def test_limpar_e_filtrar_dados_aceita_alias_defas():
    dados_brutos_simulados = pd.DataFrame({
        'IDA': ['8,5', '7,0'],
        'IEG': ['7,1', '6,5'],
        'IAA': [9.0, 8.0],
        'IPS': ['7,5', '8,0'],
        'Defas': [0.0, 1.0],
    })

    resultado_limpo = limpar_e_filtrar_dados(dados_brutos_simulados)

    assert 'Defasagem' in resultado_limpo.columns
    assert 'Defas' not in resultado_limpo.columns
    assert len(resultado_limpo) == 2


def test_limpar_e_filtrar_dados_sem_coluna_alvo_dispara_erro_claro():
    dados_brutos_simulados = pd.DataFrame({
        'IDA': ['8,5', '7,0'],
        'IEG': ['7,1', '6,5'],
        'IAA': [9.0, 8.0],
        'IPS': ['7,5', '8,0'],
    })

    with pytest.raises(ValueError, match="Defasagem"):
        limpar_e_filtrar_dados(dados_brutos_simulados)