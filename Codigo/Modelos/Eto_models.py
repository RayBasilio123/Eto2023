import numpy as np
import pandas as pd
import math
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from .metrics import calculate_mae, calculate_nse, calculate_mbe, calculate_rmse
from .Eto_experiments import get_x2
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from matplotlib import pyplot as plt
import warnings
import joblib
from lime.lime_tabular import LimeTabularExplainer
import os

warnings.filterwarnings("ignore")

def generate_lime_explanations(model, x_test_sample, feature_names, class_names, output_path):
    print(f"Generating LIME explanation for model {model.__class__.__name__}")
    explainer = LimeTabularExplainer(x_test_sample, feature_names=feature_names, class_names=class_names, verbose=True, mode='regression')
    exp = explainer.explain_instance(x_test_sample[0], model.predict)
    exp.save_to_file(output_path)
    print(f"LIME explanation saved to {output_path}")

def train_test(df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest):
    tabela = get_x2(df, lista, lags, Eto, lags_eto)
    selecao_treino = (tabela[0]['Data'] >= data_Itreino) & (tabela[0]['Data'] <= data_Ftreino)
    selecao_teste = (tabela[0]['Data'] >= data_Itest) & (tabela[0]['Data'] <= data_Ftest)

    x1_train = tabela[0][selecao_treino].drop("Data", axis=1)
    x1_test = tabela[0][selecao_teste].drop("Data", axis=1)

    y1_train = df[variavel_Alvo][selecao_treino]
    y1_test = df[variavel_Alvo][selecao_teste]

    x1_train = x1_train[tabela[1]:]
    y1_train = y1_train[tabela[1]:]

    return x1_train, x1_test, y1_train, y1_test  # Retorna DataFrames

def train_model(model_class, model_params, df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_path, lime_save_dir):
    model = model_class(**model_params)

    x1_train, x1_test, y1_train, y1_test = train_test(df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest)

    model.fit(x1_train, y1_train)
    y1_pred = model.predict(x1_test)
    mse = mean_squared_error(y1_test, y1_pred)
    std_mse = np.std(np.sqrt((y1_pred - y1_test) ** 2))

    mbe = calculate_mbe(y1_test, y1_pred)
    nse = calculate_nse(y1_test, y1_pred)
    rmse = calculate_rmse(y1_test, y1_pred)
    mae = calculate_mae(y1_test, y1_pred)

    # Salvar o modelo treinado
    joblib.dump(model, model_save_path)

    # Gerar explicações LIME
    lime_output_path = os.path.join(lime_save_dir, f"lime_explanation_{model_class.__name__}_horizon_{horizon}.html")
    x1_test_sample = x1_test.values[:5]  # Converte para ndarray
    feature_names = x1_test.columns.tolist()  # Extrai os nomes das colunas do DataFrame
    class_names = ["Eto"]
    generate_lime_explanations(model, x1_test_sample, feature_names, class_names, lime_output_path)

    return lista, lags, Eto, lags_eto, rmse, mae, nse, mbe, model.__class__.__name__

def arvore(df, model_params, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_path, lime_save_dir):
    return train_model(DecisionTreeRegressor, model_params, df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_path, lime_save_dir)

def xgb(df, model_params, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_path, lime_save_dir):
    return train_model(XGBRegressor, model_params, df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_path, lime_save_dir)

def florestaAleatoria(df, model_params, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_path, lime_save_dir):
    return train_model(RandomForestRegressor, model_params, df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_path, lime_save_dir)

def apply_model_to_list(model_func, df, list_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_dir, lime_save_dir):
    lista_colunas = ["list", "list_lags", variavel_Alvo, "lags_Target", "rmse", "mae", "nse", "mbe", "forecast_horizon", "model", "selection_attribute_type"]
    tb = pd.DataFrame(columns=lista_colunas)
    print(model_func.__name__)

    for x in range(len(list_parametros)):
        model_save_path = os.path.join(model_save_dir, f"{model_func.__name__}_horizon_{horizon}_model_{x}.joblib")
        a = model_func(df, model_params_list[x], list_parametros[x][0], list_parametros[x][1], list_parametros[x][2], list_parametros[x][3], variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_path, lime_save_dir)

        tb.loc[x, 'list'] = a[0]
        tb.loc[x, 'list_lags'] = a[1]
        tb.loc[x, variavel_Alvo] = a[2]
        tb.loc[x, 'lags_Target'] = a[3]
        tb.loc[x, "rmse"] = a[4]
        tb.loc[x, 'mae'] = a[5]
        tb.loc[x, 'nse'] = a[6]
        tb.loc[x, 'mbe'] = a[7]
        tb.loc[x, 'forecast_horizon'] = horizon
        tb.loc[x, 'model'] = model_func.__name__
        tb.loc[x, 'selection_attribute_type'] = x

    return tb

def arvores(df, arvore_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_dir, lime_save_dir):
    return apply_model_to_list(arvore, df, arvore_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_dir, lime_save_dir)

def xgbs(df, xgbs_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_dir, lime_save_dir):
    return apply_model_to_list(xgb, df, xgbs_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_dir, lime_save_dir)

def florestasAleatorias(df, florestas_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_dir, lime_save_dir):
    return apply_model_to_list(florestaAleatoria, df, florestas_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon, model_save_dir, lime_save_dir)
