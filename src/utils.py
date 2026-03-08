import logging
import os

def configurar_log_do_projeto():
    """
    Configura o sistema de logs para registrar as atividades da API 
    em um arquivo chamado 'monitoramento_projeto.log'.
    """
    caminho_log = "monitoramento_projeto.log"
    
    logging.basicConfig(
        filename=caminho_log,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    return logging.getLogger("MonitoramentoPassosMagicos")

# Inicializando o logger para ser usado em outros módulos
logger_projeto = configurar_log_do_projeto()