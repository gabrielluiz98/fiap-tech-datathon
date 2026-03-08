import pandas as pd


def _normalizar_colunas_e_alvo(dados: pd.DataFrame) -> pd.DataFrame:
    """Padroniza nomes de colunas e unifica o nome da variável alvo."""
    dados_normalizados = dados.copy()
    dados_normalizados.columns = dados_normalizados.columns.astype(str).str.strip()

    # Altera o nome da coluna defas para defasagem
    if 'Defasagem' not in dados_normalizados.columns and 'Defas' in dados_normalizados.columns:
        dados_normalizados = dados_normalizados.rename(columns={'Defas': 'Defasagem'})

    return dados_normalizados

def carregar_e_unificar_bases(caminho_csv_2022: str, caminho_csv_2023: str, caminho_csv_2024: str) -> pd.DataFrame:
    """
    Carrega os dados dos três anos disponíveis e unifica tudo em um único DataFrame.
    Trata a diferença de nomenclatura da variável alvo entre os anos antes da junção.
    """
    # Lendo os arquivos CSV
    dados_ano_2022 = _normalizar_colunas_e_alvo(pd.read_csv(caminho_csv_2022, sep=',', engine='python'))
    dados_ano_2023 = _normalizar_colunas_e_alvo(pd.read_csv(caminho_csv_2023, sep=',', engine='python'))
    dados_ano_2024 = _normalizar_colunas_e_alvo(pd.read_csv(caminho_csv_2024, sep=',', engine='python'))

    # A base de 2022 chama a variável de 'Defas', enquanto 2023 e 2024 chamam de 'Defasagem'.
    # Padronização dos dados
    dados_ano_2022 = dados_ano_2022.rename(columns={'Defas': 'Defasagem'})

    # Empilhando as três bases de dados. 
    dados_completos_estudantes = pd.concat(
        [dados_ano_2022, dados_ano_2023, dados_ano_2024], 
        ignore_index=True
    )
    
    return dados_completos_estudantes

def limpar_e_filtrar_dados(dados_brutos: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona apenas as colunas essenciais para o nosso modelo de Regressão Logística,
    trata os tipos de dados (como vírgulas em números decimais) e remove valores nulos.
    """
    dados_brutos = _normalizar_colunas_e_alvo(dados_brutos)

    # Verifica se tem a coluna defasagem
    if 'Defasagem' not in dados_brutos.columns:
        raise ValueError(
            "A coluna alvo 'Defasagem' não foi encontrada. "
            "Verifique se os dados possuem 'Defasagem' ou 'Defas'."
        )
    # Selecionando as features principais
    colunas_essenciais = ['IDA', 'IEG', 'IAA', 'IPS', 'Defasagem']
    
    # Garantindo que vai ser filtrado apenas coluans que existem no df
    colunas_presentes = [coluna for coluna in colunas_essenciais if coluna in dados_brutos.columns]
    dados_filtrados = dados_brutos[colunas_presentes].copy()

    # Removendo linhas que não tem defasagem
    dados_filtrados = dados_filtrados.dropna(subset=['Defasagem'])

    # Selecionando indicadores
    colunas_de_indicadores = ['IDA', 'IEG', 'IAA', 'IPS']
    
    # Faz uma verificação e transforma valores de string em numéricos
    for coluna in colunas_de_indicadores:
        if coluna in dados_filtrados.columns:
            if pd.api.types.is_string_dtype(dados_filtrados[coluna]):
                serie_limpa = dados_filtrados[coluna].astype(str).str.strip().str.replace(',', '.', regex=False)
                dados_filtrados[coluna] = pd.to_numeric(serie_limpa, errors='coerce')
            else:
                dados_filtrados[coluna] = pd.to_numeric(dados_filtrados[coluna], errors='coerce')

    # Remove os dados nulos.
    dados_finais_limpos = dados_filtrados.dropna().copy()

    # Convertendo coluna defasagem para inteiro
    dados_finais_limpos['Defasagem'] = dados_finais_limpos['Defasagem'].astype(int)
    
    return dados_finais_limpos

def executar_pipeline_pre_processamento(caminho_2022: str, caminho_2023: str, caminho_2024: str) -> pd.DataFrame:
    """
    Função principal que orquestra o carregamento, unificação e limpeza dos dados.
    """
    dados_unificados = carregar_e_unificar_bases(caminho_2022, caminho_2023, caminho_2024)
    dados_prontos_para_treino = limpar_e_filtrar_dados(dados_unificados)
    
    
    return dados_prontos_para_treino