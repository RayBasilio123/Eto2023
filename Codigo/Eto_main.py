import pandas as pd
from Modelos.util import run_models_for_horizons, save_results_to_csv, read_station_params, read_station_names, \
    run_model_and_save_results
from Modelos.Eto_models import arvores,florestasAleatorias,xgbs
import warnings
# warnings.filterwarnings("ignore")
horizons = [1, 3, 7, 10]
model_names =["arvores","xgb","florestasAleatorias"]
path= '/home/ray/PycharmProjects/pythonProject1/ETo/2020_Ic/Dados/'

station_name ='PORTO_ALEGRE'
url=(f'https://raw.githubusercontent.com/RayBasilio123/database/main/INMET/CSV/J_Database/{station_name}_J_2014_2020.csv')
dataframe = pd.read_csv(url, sep=",", encoding = "ISO-8859-1")
dataframe=dataframe.drop(columns=['Unnamed: 0'])

data_Itreino = '2014-01-01'
data_Ftreino = '2018-12-31'
data_Itest = '2019-01-01'
data_Ftest = '2020-12-31'
station_names = read_station_names(path+"station_params.json")
attribute_list, model_params_list_arvore = read_station_params(path+"station_params.json", station_name, model_names[0],horizons)
attribute_list, model_params_list_xgbs = read_station_params(path+"station_params.json", station_name, model_names[1],horizons)
attribute_list, model_params_list_florestasAleatorias= read_station_params(path+"station_params.json", station_name,model_names[2],horizons)
for code_execution in range(10):
    run_model_and_save_results(arvores, attribute_list, model_params_list_arvore, model_names[0], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,
                               path+"region_table.csv", code_execution + 1)
    run_model_and_save_results(xgbs, attribute_list, model_params_list_xgbs, model_names[1], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,
                               path+"region_table.csv", code_execution + 1)
    run_model_and_save_results(florestasAleatorias, attribute_list, model_params_list_florestasAleatorias, model_names[2], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,
                               path+"region_table.csv", code_execution + 1)
# for i in [2,3,4,5]:
#     ano_teste = f'201{i}'
#     station_name = f"SETE_LAGOAS_{ano_teste}"
#     url=("/home/ray/PycharmProjects/pythonProject1/ETo/2020_Ic/Dados/SETE_LAGOAS.csv")
#     dataframe = pd.read_csv(url, sep=",", encoding = "ISO-8859-1")
#     dataframe=dataframe.drop(columns=['Unnamed: 0'])
#
#     data_Itreino = '1993-01-01'
#     data_Ftreino = '2011-12-31'
#     data_Itest = f'{ano_teste}-01-01'
#     data_Ftest = f'{ano_teste}-12-31'
#
#     horizons = [1, 3, 7, 10]
#     model_names =["arvores","xgb","florestasAleatorias"]
#
#
#     station_names = read_station_names(path+"station_params_year.json")
#     attribute_list, model_params_list_arvore = read_station_params(path+"station_params_year.json", station_name, model_names[0],horizons)
#     attribute_list, model_params_list_xgbs = read_station_params(path+"station_params_year.json", station_name, model_names[1],horizons)
#     attribute_list, model_params_list_florestasAleatorias= read_station_params(path+"station_params_year.json", station_name,model_names[2],horizons)
#     for code_execution in range(10):
#         run_model_and_save_results(arvores, attribute_list, model_params_list_arvore, model_names[0], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,
#                                    path+"tabela_geral_ano.csv", code_execution + 1)
#         run_model_and_save_results(xgbs, attribute_list, model_params_list_xgbs, model_names[1], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,
#                                    path+"tabela_geral_ano.csv", code_execution + 1)
#         run_model_and_save_results(florestasAleatorias, attribute_list, model_params_list_florestasAleatorias, model_names[2], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,
#                                    path+"tabela_geral_ano.csv", code_execution + 1)
# ano_teste = f'2012'
# station_name = f"SETE_LAGOAS_{ano_teste}"
# url=("/home/ray/PycharmProjects/pythonProject1/ETo/2020_Ic/Dados/SETE_LAGOAS.csv")
# dataframe = pd.read_csv(url, sep=",", encoding = "ISO-8859-1")
# dataframe=dataframe.drop(columns=['Unnamed: 0'])
#
# data_Itreino = '1993-01-01'
# data_Ftreino = '2011-12-31'
# data_Itest = f'{ano_teste}-01-01'
# data_Ftest = f'{ano_teste}-12-31'
#

#
#
# station_names = read_station_names(path+"station_params_year.json")
# attribute_list, model_params_list_arvore = read_station_params(path+"station_params_year.json", station_name, model_names[0],horizons)
# attribute_list, model_params_list_xgbs = read_station_params(path+"station_params_year.json", station_name, model_names[1],horizons)
# attribute_list, model_params_list_florestasAleatorias= read_station_params(path+"station_params_year.json", station_name,model_names[2],horizons)
#
# run_model_and_save_results(arvores, attribute_list, model_params_list_arvore, model_names[0], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,
#                            path+"teste_tabela_geral_ano.csv",  1)
# run_model_and_save_results(xgbs, attribute_list, model_params_list_xgbs, model_names[1], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,
#                            path+"teste_tabela_geral_ano.csv",  1)
# run_model_and_save_results(florestasAleatorias, attribute_list, model_params_list_florestasAleatorias, model_names[2], dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,
#                            path+"teste_tabela_geral_ano.csv", 1)

