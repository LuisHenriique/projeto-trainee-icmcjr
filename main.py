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
        print("  PRIMEIRAS 5 LINHAS:")
        print(df.head())
        print("\n  INFORMAÇÕES (TIPOS DE DADOS E NÚMERO DE VALORES NÃO NULOS):")
        df.info()
        print("\n  CONTAGEM DE VALORES NULOS POR COLUNA")
        print(df.isnull().sum())
        print("---------------------------------\n")

def salvar_arquivo(df, nome_csv):
    """salva o dataframe em um arquivo csv"""
    print("--- SALVANDO ARQUIVO... ---")
    if df is not None:
        try:
            df.to_csv(nome_csv, index=False, encoding='utf-8')
            print(f"  arquivo salvo com sucesso em: {nome_csv}")
        except Exception as e:
            print(f"  ERRO ao salvar o arquivo: {e}")

def limpeza(df):
    """função para tratar e limpar os dados do dataframe"""
    print("--- LIMPANDO OS DADOS ---")
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

    # operações para tratamento de valores nulos
    print("  tratamento de valores nulos para colunas específicas:")
    colunas_com_nulos = df_limpo.columns[df_limpo.isnull().any()].tolist()
    print(f"    colunas com valores nulos: {colunas_com_nulos}")
    df_limpo = t_e.preenche_nulos(df_limpo)
    
    # operações para tratamento de assimetria (indiretamente, trata outliers)
    # as colunas não são todas necessariamente assimétricas (podem ser), mas a transformação não prejudica colunas simétricas
    print("  tratamento de assimetria para colunas específicas:")
    colunas_assimetricas = ['MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion']
    print(f"    colunas tratadas com log1p: {colunas_assimetricas}")
    df_limpo = t_e.trata_assimetria_log(df_limpo, colunas_assimetricas)

    # operações para tratamento de outliers
    print("  tratamento de outliers para colunas específicas:")
    colunas_para_clipping = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike']
    print(f"    colunas tratadas com clipping: {colunas_para_clipping}")
    df_limpo = t_e.trata_outliers_clipping(df_limpo, colunas_para_clipping)

    # operação de padronização de texto
    df_limpo = t_e.padroniza_texto(df_limpo)

    print()
    return df_limpo


def main():
    nome_arquivo_bruto = "dados.csv" 
    nome_arquivo_limpo = "dados_limpos.csv" 

    df_bruto = carregar_arquivo(nome_arquivo_bruto)

    if df_bruto is not None:
        print("\n--- INFORMAÇÕES DO DATAFRAME BRUTO ---")
        exibir_informacoes(df_bruto)
        df_limpo = limpeza(df_bruto)
        salvar_arquivo(df_limpo, nome_arquivo_limpo)
        print("\n--- INFORMAÇÕES DO DATAFRAME LIMPO ---")
        exibir_informacoes(df_limpo)

if __name__ == "__main__":
    main()