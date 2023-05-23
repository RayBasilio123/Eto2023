import numpy as np
import pandas as pd
import math
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from .metrics import calculate_mae,calculate_nse,calculate_mbe,calculate_rmse
from .Eto_experiments import get_x2
from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor
from matplotlib import pyplot
import warnings

warnings.filterwarnings("ignore")


def train_test(df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest):
    # def train_test(df, lista,lags,Eto,lags_eto,variavel_Alvo,data_Itest= '2015-01-01',data_Ftest= '2015-12-31',data_Itreino='1993-01-01',data_Ftreino='2011-12-31'):
    tabela = get_x2(df, lista, lags, Eto, lags_eto)
    print("\nTreino_Aqui\n", tabela[0])
    selecao_treino = (tabela[0]['Data'] >= data_Itreino) & (tabela[0]['Data'] <= data_Ftreino)
    selecao_teste = (tabela[0]['Data'] >= data_Itest) & (tabela[0]['Data'] <= data_Ftest)

    x1_train = tabela[0][selecao_treino].drop("Data", axis=1)
    x1_test = tabela[0][selecao_teste].drop("Data", axis=1)

    y1_train = df[variavel_Alvo][selecao_treino]
    y1_test = df[variavel_Alvo][selecao_teste]

    x1_train = x1_train[tabela[1]:]
    y1_train = y1_train[tabela[1]:]

    # print("***************************************")
    # print(x1_train.shape,"x1_train",tabela[1],"Maxx")
    # #[6569 rows x 10 columns] x1_train
    # print("*****************++*********************")
    # print(x1_test.shape,"x1_test")
    # print("******************---********************")
    # print(y1_train.shape,"y1_train")
    # print("****************1234*********************")
    # print(y1_test.shape,"y1_test")
    # print("*****************asddfg******************")

    return x1_train.values, x1_test.values, y1_train, y1_test


def train_model(model_class, model_params, df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino,
                data_Itest, data_Ftest,horizon):
    # Crie o modelo com os hiperparâmetros fornecidos
    model = model_class(**model_params)

    x1_train, x1_test, y1_train, y1_test = train_test(
        df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest
    )

    model.fit(x1_train, y1_train)
    print("------------------")
    print(model.__class__.__name__)
    y1_pred = model.predict(x1_test)
    mse = mean_squared_error(y1_test, y1_pred)
    std_mse = np.std(np.sqrt((y1_pred - y1_test) ** 2))

    mbe = calculate_mbe(y1_test, y1_pred)
    nse = calculate_nse(y1_test, y1_pred)
    rmse = calculate_rmse(y1_test, y1_pred)
    mae = calculate_mae(y1_test, y1_pred)
    print("std_mse", round(std_mse, 2))
    fig, ax = pyplot.subplots()

    ax.plot(np.arange(y1_test.shape[0]), y1_test,label=f' Forecast Horizon {horizon} - Expected {model.__class__.__name__}')
    ax.plot(y1_pred, label=f' Forecast Horizon {horizon} - Predicted {model.__class__.__name__}')
    ax.legend(bbox_to_anchor=(0.5, 1.05), loc='lower center', borderaxespad=0)

    fig.tight_layout()  # Ajusta automaticamente o layout
    pyplot.subplots_adjust(top=0.85)  # Ajuste a área do gráfico para criar espaço na parte superior
    pyplot.show()

    return lista, lags, Eto, lags_eto, rmse, mae, nse, mbe, model.__class__.__name__


def arvore(df, model_params, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest,
           data_Ftest,horizon):
    return train_model(DecisionTreeRegressor, model_params, df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino,
                       data_Ftreino, data_Itest, data_Ftest,horizon)


def xgb(df, model_params, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest,
        data_Ftest,horizon):
    return train_model(XGBRegressor, model_params, df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino,
                       data_Ftreino, data_Itest, data_Ftest,horizon)


def florestaAleatoria(df, model_params, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino, data_Ftreino,
                      data_Itest, data_Ftest,horizon):
    return train_model(RandomForestRegressor, model_params, df, lista, lags, Eto, lags_eto, variavel_Alvo, data_Itreino,
                       data_Ftreino, data_Itest, data_Ftest,horizon)


def apply_model_to_list(model_func, df, list_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino,
                        data_Itest, data_Ftest,horizon):
    lista_colunas = ["list", "list_lags", variavel_Alvo, "lags_Target",
                     "rmse", "mae", "nse", "mbe", "forecast_horizon","model","selection_attribute_type"]

    tb = pd.DataFrame(columns=lista_colunas)
    print(model_func.__name__)

    for x in range(len(list_parametros)):
        a = model_func(df, model_params_list[x], list_parametros[x][0], list_parametros[x][1],
                       list_parametros[x][2], list_parametros[x][3],
                       variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest, horizon)

        tb.loc[x, 'list'] = a[0]
        tb.loc[x, 'list_lags'] = a[1]
        tb.loc[x, variavel_Alvo] = a[2]
        tb.loc[x, 'lags_Target'] = a[3]
        tb.loc[x, "rmse"] = a[4]
        tb.loc[x, 'mae'] = a[5]
        tb.loc[x, 'nse'] = a[6]
        tb.loc[x, 'mbe'] = a[7]
        tb.loc[x, 'forecast_horizon'] = horizon
        tb.loc[x, 'model'] =model_func.__name__
        tb.loc[x, 'selection_attribute_type'] =x

    print(tb)

    return tb


def arvores(df, arvore_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest,
            data_Ftest,horizon):
    return apply_model_to_list(arvore, df, arvore_parametros, model_params_list, variavel_Alvo, data_Itreino,
                               data_Ftreino, data_Itest, data_Ftest,horizon)


def xgbs(df, xgbs_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest,horizon):
    return apply_model_to_list(xgb, df, xgbs_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino,
                               data_Itest, data_Ftest,horizon)


def florestasAleatorias(df, florestas_parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest,
                        data_Ftest,horizon):
    return apply_model_to_list(florestaAleatoria, df, florestas_parametros, model_params_list, variavel_Alvo, data_Itreino,
                               data_Ftreino, data_Itest, data_Ftest,horizon)
