import os
import json
import pandas as pd


def run_models_for_horizons(model_func, df, parametros_list, model_params_list_list, variavel_Alvo, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,code_execution):
    results = []

    for i, horizon in enumerate(horizons):
        print(f"Executando {model_func.__name__} para horizonte {horizon} dias")
        parametros = parametros_list[i]
        model_params_list = model_params_list_list[i]
        result = model_func(df, parametros, model_params_list, variavel_Alvo, data_Itreino, data_Ftreino, data_Itest, data_Ftest,horizon)
        result["horizon"] = horizon
        result["station_name"] = station_name.capitalize()
        result["code_execution"] = code_execution
        results.append(result)

    return pd.concat(results, ignore_index=True)


def save_results_to_csv(results, output_file):
    if os.path.exists(output_file):
        results.to_csv(output_file, mode="a", header=False, index=False)
    else:
        results.to_csv(output_file, index=False)


def read_station_params(json_file, station_name, model_name,horizons):
    with open(json_file, 'r') as file:
        data = json.load(file)

    station_data = data["station_data"][station_name]

    atributo_list = station_data["atributo_list"]
    model_params = station_data[f"model_params_{model_name}"]

    attribute_list = [atributo_list[str(h)] for h in horizons]
    model_params_list_list = [model_params[f"params_list_{h}"] for h in horizons]

    return attribute_list, model_params_list_list
def read_station_names(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    station_names = list(data["station_data"].keys())
    return station_names

def run_model_and_save_results(model, attribute_list, model_params_list, model_name, dataframe, horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name, output_file,code_execution):
    result = run_models_for_horizons(model, dataframe, attribute_list, model_params_list, "Eto", horizons, data_Itreino, data_Ftreino, data_Itest, data_Ftest, station_name,code_execution)
    save_results_to_csv(result, output_file)
