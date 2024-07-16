import joblib
from lime.lime_tabular import LimeTabularExplainer
import pandas as pd


def load_model(model_path):
    return joblib.load(model_path)


def generate_lime_explanations(model, x_test_sample, feature_names, class_names):
    explainer = LimeTabularExplainer(x_test_sample, feature_names=feature_names, class_names=class_names, verbose=True,
                                     mode='regression')
    exp = explainer.explain_instance(x_test_sample[0], model.predict)
    exp.show_in_notebook(show_table=True)


# Exemplo de uso
if __name__ == "__main__":
    # Modifique os caminhos conforme necessário
    model_save_path = "C:/Users/rayba/PycharmProjects/Eto2023/ModelosTreinados/arvore_horizon_1_model_0.joblib"
    data_path = "C:/Users/rayba/PycharmProjects/Eto2023/Dados/SETE_LAGOAS.csv"

    # Carregue o modelo
    model = load_model(model_save_path)

    # Carregue os dados de teste
    df = pd.read_csv(data_path, sep=",", encoding="ISO-8859-1")
    df = df.drop(columns=['Unnamed: 0'])

    # Pré-processamento dos dados (substitua pelas suas funções de pré-processamento)
    from Modelos.Eto_experiments import get_x2

    lista = []  # Lista de atributos
    lags = []  # Lags
    Eto = []  # Eto
    lags_eto = []  # Lags de Eto
    tabela = get_x2(df, lista, lags, Eto, lags_eto)
    data_Itest = '2012-01-01'
    data_Ftest = '2012-12-31'
    selecao_teste = (tabela[0]['Data'] >= data_Itest) & (tabela[0]['Data'] <= data_Ftest)
    x1_test = tabela[0][selecao_teste].drop("Data", axis=1).values

    # Defina os nomes das colunas e das classes
    feature_names = df.columns.tolist()
    class_names = ["Eto"]

    # Gere as explicações LIME
    generate_lime_explanations(model, x1_test[:5], feature_names,
                               class_names)  # Ajuste o número de amostras conforme necessário
