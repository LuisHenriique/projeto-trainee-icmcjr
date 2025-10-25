"""para maior organização, este arquivo contém funções de tratamento de dados de colunas específicas"""

import numpy as np
import pandas as pd

def preenche_nulos_com_mediana(df, coluna):
    """preenche valores nulos em uma coluna numérica com a mediana"""
    mediana = df[coluna].median()
    print(f"    preenchendo valores nulos em '{coluna}' com a mediana = {mediana}")
    df[coluna] = df[coluna].fillna(mediana)
    return df

def preenche_nulos_com_moda(df, coluna):
    """preenche valores nulos em uma coluna categórica com a moda"""
    moda = df[coluna].mode()[0]
    print(f"    preenchendo valores nulos em '{coluna}' com a moda = {moda}")
    df[coluna] = df[coluna].fillna(moda)
    return df

def preenche_nulos_com_media(df, coluna):
    """preenche valores nulos em uma coluna numérica com a média"""
    media = df[coluna].mean()
    print(f"    preenchendo valores nulos em '{coluna}' com a média = {media}")
    df[coluna] = df[coluna].fillna(media)
    return df