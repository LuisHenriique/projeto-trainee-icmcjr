"""para maior organização, este arquivo contém funções de tratamento de dados mais específicos"""

import numpy as np
import pandas as pd

"""
funções para tratamento específico de colunas com valores nulos ---
"""

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

def preenche_nulos(df):
    """função "principal" para preencher valores nulos. apenas chama as demais funções acima para cada caso específico"""
    # para maior precisão, cada coluna com valores nulos (e a estratégia usada para preenchê-los) é tratada individualmente
    # a estratégia decidida para cada coluna foi feita à parte com base na análise dos dados, explicado em main.ipynb
    # além disso, também no notebook, verifica-se que não existem outliers para as dadas colunas, então não são tratados aqui
    df = preenche_nulos_com_mediana(df, 'DistanceFromHome')
    df = preenche_nulos_com_moda(df, 'EnvironmentSatisfaction')
    df = preenche_nulos_com_moda(df, 'OverTime')
    df = preenche_nulos_com_media(df, 'HourlyRate')
    df = preenche_nulos_com_moda(df, 'BusinessTravel')
    df = preenche_nulos_com_moda(df, 'Gender')
    df = preenche_nulos_com_moda(df, 'JobInvolvement')
    df = preenche_nulos_com_moda(df, 'PerformanceRating')

    return df

"""
funções para verificação/tratamento de outliers ---
"""

def calcula_lim_iqr(coluna):
    """calcula a amplitude interquartil de uma coluna"""
    Q1 = coluna.quantile(0.25) # 1° quartil
    Q3 = coluna.quantile(0.75) # 3° quartil 
    IQR = Q3 - Q1 # amplitude interquartil
    
    limite_inferior = Q1 - (1.5 * IQR) # lim inferior
    limite_superior = Q3 + (1.5 * IQR) # lim superior
    
    return limite_inferior, limite_superior

def verifica_outliers(df, coluna):
    """verifica existência de outliers dada uma certa coluna do dataframe"""
    # calcula limite inferior e superior da coluna específica
    lim_inf, lim_sup = calcula_lim_iqr(df[coluna])
    
    # verifica se possui um dado menor que o limite inferior ou se há um dado maior que o limite superior
    if df[coluna].min() < lim_inf or df[coluna].max() > lim_sup: return True
    return False

def trata_outliers_clipping(df, colunas):
    """trata outliers "capando" (clipping) os valores nos limites IQR"""
    
    for coluna in colunas:
        # pega os limites
        lim_inf, lim_sup = calcula_lim_iqr(df[coluna])

        # conta quantos outliers existem antes
        num_outliers = df[(df[coluna] < lim_inf) | (df[coluna] > lim_sup)].shape[0]

        if num_outliers > 0:
            print(f"    tratando {num_outliers} outliers em '{coluna}' com clipping")
            # usa np.clip para "capar" os valores
            df[coluna] = np.clip(df[coluna], lim_inf, lim_sup)

    return df


"""
funções para tratamento de assimetria (indiretamente, trata outliers) ---
"""

def trata_assimetria_log(df, colunas):
    """aplica transformação log1p em colunas específicas com cauda longa (assimétricas)"""
    
    for col in colunas:
        if col in df.columns:
            print(f"    transformando coluna '{col}' com log1p")
            # substitui a coluna original pela sua versão log
            df[col] = np.log1p(df[col])
            # renomeia para clareza
            df.rename(columns={col: f'{col}_log'}, inplace=True)
            
    return df


"""
função para padronização de texto ---
"""

def padroniza_texto(df):
    """padroniza colunas de texto (object): remove espaços extras e converte para minúsculas"""
    
    print("  padronizando colunas de texto (strip, lower)...")
    df_tratado = df.copy()
    
    # seleciona apenas as colunas do tipo 'object' (texto)
    colunas_texto = df_tratado.select_dtypes(include=['object']).columns
    
    for col in colunas_texto:
        df_tratado[col] = df_tratado[col].str.strip().str.lower()
        
    return df_tratado