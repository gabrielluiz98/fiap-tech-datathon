import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def separar_dados_treino_e_teste(dados_prontos: pd.DataFrame):
    """
    Separa os dados entre o que o modelo vai usar para aprender (features) 
    e o que ele precisa adivinhar (target/alvo). Depois, divide em blocos de treino e teste.
    """
    if dados_prontos.empty:
        raise ValueError("A base de treino está vazia após o pré-processamento.")

    # A variável alvo original é Defasagem (valores como -2, -1, 0, 1...).
    # Para o problema de negócio da API (risco de defasagem), foi transformado em binário:
    # 1 = em risco (defasagem negativa), 0 = sem risco.
    atributos_preditivos_x = dados_prontos.drop(columns=['Defasagem'])
    variavel_alvo_y = (dados_prontos['Defasagem'] < 0).astype(int)

    # Dividindo os dados: 80% para train e 20% para test.
    x_treino, x_teste, y_treino, y_teste = train_test_split(
        atributos_preditivos_x, 
        variavel_alvo_y, 
        test_size=0.2, 
        random_state=42,
        stratify=variavel_alvo_y
    )
    
    return x_treino, x_teste, y_treino, y_teste

def treinar_modelo_regressao_logistica(x_treino, y_treino):
    """
    Inicializa e treina o nosso modelo base (Regressão Logística).
    É um modelo excelente para começar porque é simples, rápido e muito interpretável.
    """
    # Criando pipeline
    modelo_regressao_logistica = Pipeline(
        steps=[
            ('escalonador', StandardScaler()),
            ('modelo', LogisticRegression(max_iter=1500, random_state=42, class_weight='balanced')),
        ]
    )
    
    # Treinando o modelo
    modelo_regressao_logistica.fit(x_treino, y_treino)
    
    return modelo_regressao_logistica

def avaliar_desempenho_do_modelo(modelo_treinado, x_teste, y_teste):
    """
    Aplica as previsões na base de teste e calcula as métricas para sabermos se 
    o modelo é confiável o suficiente para ir para produção.
    """
    # Roda o modelo nos dados de teste para ter as métricacs de desempenho
    previsoes_feitas_pelo_modelo = modelo_treinado.predict(x_teste)
    
    # Métricas de desempenho do modelo
    acuracia = accuracy_score(y_teste, previsoes_feitas_pelo_modelo)
    revocacao = recall_score(y_teste, previsoes_feitas_pelo_modelo, zero_division=0)
    pontuacao_f1 = f1_score(y_teste, previsoes_feitas_pelo_modelo, zero_division=0)
    
    print("\n--- AVALIAÇÃO DO MODELO DE DEFASAGEM ESCOLAR ---")
    print(f"Acurácia Global: {acuracia:.2f} (Taxa de acertos gerais)")
    print(f"F1-Score: {pontuacao_f1:.2f} (Equilíbrio entre precisão e revocação)")
    
    # Justificativa técnica exigida pelo projeto sobre a confiabilidade do modelo
    print(f"\nMétrica Principal de Negócio - Revocação (Recall): {revocacao:.2f}")
    print("Justificativa: Para a Associação Passos Mágicos, a Revocação é a métrica mais confiável.")
    print("Ela mede a capacidade do modelo de encontrar todos os alunos que REALMENTE estão em defasagem.")
    print("Em um cenário educacional, é preferível ter um 'Falso Positivo' (dar atenção a um aluno que não precisava tanto)")
    print("do que um 'Falso Negativo' (deixar passar despercebido um aluno que está ficando para trás).")
    print("-" * 50)
    
    return acuracia, revocacao

def salvar_modelo_treinado(modelo_treinado, caminho_salvamento: str):
    """
    Pega o modelo que já aprendeu os padrões e salva no disco.
    Isso é necessário para que a nossa API consiga carregar o modelo sem precisar treinar tudo de novo.
    """
    joblib.dump(modelo_treinado, caminho_salvamento)
    print(f"\nSucesso! Modelo salvo e empacotado em: {caminho_salvamento}")

def executar_pipeline_treinamento(dados_limpos_estudantes: pd.DataFrame, caminho_pasta_modelos: str):
    """
    Função principal que orquestra todo o processo de treino, avaliação e salvamento.
    """
    print("Iniciando a separação de dados para treino e teste...")
    x_treino, x_teste, y_treino, y_teste = separar_dados_treino_e_teste(dados_limpos_estudantes)
    
    print("Treinando o modelo de Regressão Logística...")
    modelo_final = treinar_modelo_regressao_logistica(x_treino, y_treino)
    
    print("Avaliando os resultados...")
    avaliar_desempenho_do_modelo(modelo_final, x_teste, y_teste)
    
    # Salvando no diretório especificado
    caminho_completo_arquivo = f"{caminho_pasta_modelos}/modelo_regressao_logistica.joblib"
    salvar_modelo_treinado(modelo_final, caminho_completo_arquivo)