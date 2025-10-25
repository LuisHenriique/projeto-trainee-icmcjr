import pandas as pd
import numpy as np
import tratamentos_especificos as t_e

def carregar_arquivo(nome_csv):
    """carrega um arquivo csv para um dataframe"""
    print("--- CARREGANDO O CSV ---")
    try:
        df = pd.read_csv(nome_csv)
        print(f"arquivo {nome_csv} carregado com sucesso.")
        return df
    except FileNotFoundError:
        print(f"ERRO: o arquivo {nome_csv} não foi encontrado.")
        return None
    except Exception as e:
        print(f"ERRO ao carregar o arquivo: {e}")
        return None

def exibir_informacoes(df):
    """mostra informações resumidas do dataframe"""
    if df is not None:
        print("\n--- RESUMO DO DATAFRAME ---")
        print("  PRIMEIRAS 5 LINHAS:")
        print(df.head())
        print("\n  INFORMAÇÕES (TIPOS DE DADOS E NÚMERO DE VALORES NÃO NULOS):")
        df.info()
        print("\n  CONTAGEM DE VALORES NULOS POR COLUNA")
        print(df.isnull().sum())
        print("---------------------------------\n")

def salvar_arquivo(df, nome_csv):
    """salva o dataframe limpo em um novo arquivo csv"""
    print("--- FINALIZANDO: SALVANDO O CSV LIMPO... ---")
    if df is not None:
        try:
            df.to_csv(nome_csv, index=False, encoding='utf-8')
            print(f"\n  arquivo limpo salvo com sucesso em: {nome_csv}")
        except Exception as e:
            print(f"  ERRO ao salvar o arquivo: {e}")

def limpeza(df):
    """função para tratar e limpar os dados do dataframe"""
    print("--- LIMPANDO OS DADOS... ---")
    df_limpo = df.copy()

    print("  limpeza específica: removendo colunas irrelevantes")
    # verifica (e remove) colunas que possuem valores constantes
    for coluna in df_limpo.columns.tolist(): 
        if df_limpo[coluna].nunique() <= 1:
            print(f"    removendo coluna '{coluna}' (valor constante)")
            df_limpo.drop(columns=[coluna], inplace=True)
    # remove manualmente o employeeNumber (id do funcionário na base; como usamos o índice do dataframe, não é necessário)
    if 'EmployeeNumber' in df_limpo.columns:
        print("    removendo coluna 'EmployeeNumber' (id do funcionário)")
        df_limpo.drop(columns=['EmployeeNumber'], inplace=True)

    print("  tratamento de valores nulos específicos para cada coluna")
    colunas_com_nulos = df_limpo.columns[df_limpo.isnull().any()].tolist()
    print(f"    colunas com valores nulos: {colunas_com_nulos}")
    # para maior precisão, cada coluna com valores nulos (e a estratégia usada para preenchê-los) é tratada individualmente
    # a estratégia decidida para cada coluna foi feita à parte com base na análise dos dados. os scripts apenas aplicam as escolhas
    df_limpo = t_e.preenche_nulos_com_mediana(df_limpo, 'DistanceFromHome')
    df_limpo = t_e.preenche_nulos_com_moda(df_limpo, 'EnvironmentSatisfaction')
    df_limpo = t_e.preenche_nulos_com_moda(df_limpo, 'OverTime')
    df_limpo = t_e.preenche_nulos_com_media(df_limpo, 'HourlyRate')
    #  comentário próprio: --------------------------------------------
    # terminando de tratar sobre as demais colunas com valores nulos...
    # parei aqui por enquanto para mexer no notebook também e, só depois de aplicar as explicações dos tratamentos especfícos, colocá-los aqui

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

def main():
    nome_arquivo_bruto = "dados.csv" 
    nome_arquivo_limpo = "dados_limpos.csv" 

    df_bruto = carregar_arquivo(nome_arquivo_bruto)

    if df_bruto is not None:
        exibir_informacoes(df_bruto)
        limpeza(df_bruto)
        # a partir daqui adicionar o resto do processamento... trabalhando nisso

if __name__ == "__main__":
    main()