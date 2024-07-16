import pandas as pd
from Modelos.util import run_models_for_horizons, save_results_to_csv, read_station_params, read_station_names, run_model_and_save_results
from Modelos.Eto_models import arvores, florestasAleatorias, xgbs
import os

# Defina os caminhos
path = "C:/Users/rayba/PycharmProjects/Eto2023/Dados/"
model_save_dir = "C:/Users/rayba/PycharmProjects/Eto2023/ModelosTreinados/"
lime_save_dir = "/LimeExplicacoes2/"

# Certifique-se de que os diretórios de salvamento existam
os.makedirs(model_save_dir, exist_ok=True)
os.makedirs(lime_save_dir, exist_ok=True)

# Loop para os anos de teste
for i in [5]:
    ano_teste = f'201{i}'
    station_name = f"SETE_LAGOAS_{ano_teste}"
    url = path + "SETE_LAGOAS.csv"

    dataframe = pd.read_csv(url, sep=",", encoding="ISO-8859-1")
    dataframe = dataframe.drop(columns=['Unnamed: 0'])

    data_Itreino = '1993-01-01'
    data_Ftreino = '2011-12-31'
    data_Itest = f'{ano_teste}-01-01'
    data_Ftest = f'{ano_teste}-12-31'

    horizons = [1,3,7,10]
    model_names = ["arvores", "xgb", "florestasAleatorias"]

    station_names = read_station_names(path + "station_params_year.json")
    attribute_list_arvore, model_params_list_arvore = read_station_params(path + "station_params_year.json", station_name, model_names[0], horizons)
    attribute_list_xgbs, model_params_list_xgbs = read_station_params(path + "station_params_year.json", station_name, model_names[1], horizons)
    attribute_list_florestasAleatorias, model_params_list_florestasAleatorias = read_station_params(path + "station_params_year.json", station_name, model_names[2], horizons)

    for code_execution in range(1):
        run_model_and_save_results(arvores, attribute_list_arvore, model_params_list_arvore, model_names[0], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name, path + "tabela_geral_ano2.csv", code_execution + 1, model_save_dir, lime_save_dir)
        run_model_and_save_results(xgbs, attribute_list_xgbs, model_params_list_xgbs, model_names[1], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name, path + "tabela_geral_ano2.csv", code_execution + 1, model_save_dir, lime_save_dir)
        run_model_and_save_results(florestasAleatorias, attribute_list_florestasAleatorias, model_params_list_florestasAleatorias, model_names[2], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name, path + "tabela_geral_ano2.csv", code_execution + 1, model_save_dir, lime_save_dir)
