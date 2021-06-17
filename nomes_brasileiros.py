import pandas as pd

df = pd.read_csv("TrainingDatasets/Nomes/nomes_pre_tratados_famosos.csv")


def lista_nomes(df1=df, val=''):
    names = [x for x in df1["names"]]
    nomes_tratados = []
    for x in names:
        for y in x.split("|"):
            nomes_tratados.append(y)
    value = [z for z in nomes_tratados if z != val]
    string_list = [each_string.lower() for each_string in value]
    return string_list
