import pandas as pd
from evidently import Dataset, DataDefinition, Report
from evidently.presets import DataDriftPreset

def gerar_painel_de_monitoramento(dados_referencia: pd.DataFrame, dados_atuais: pd.DataFrame):
    """
    Gera o painel visual em HTML usando a API atualizada do Evidently.
    O DataDriftPreset analisa automaticamente tanto as variáveis 
    educacionais quanto a variável alvo (Defasagem).
    """
    
    definicao_dos_dados = DataDefinition()
    
    # Convertendo os DataFrames do Pandas para o formato Dataset do Evidently
    dataset_ref = Dataset.from_pandas(dados_referencia, data_definition=definicao_dos_dados)
    dataset_atual = Dataset.from_pandas(dados_atuais, data_definition=definicao_dos_dados)
    
    # Cria o relatório usando apenas o DataDriftPreset
    relatorio = Report([
        DataDriftPreset()
    ])

    # Executa a comparação
    resultado_avaliacao = relatorio.run(dataset_atual, dataset_ref)

    # Salva o HTML a partir do objeto retornado
    nome_arquivo = "monitoramento_drift_estudantes.html"
    resultado_avaliacao.save_html(nome_arquivo)
    
    print(f"Painel de monitoramento gerado com sucesso: {nome_arquivo}")
    return nome_arquivo