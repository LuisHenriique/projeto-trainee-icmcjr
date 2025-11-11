# Projeto Trainee ICMC Júnior - HR Analytics (Attrition)

Este repositório contém o desenvolvimento do projeto trainee de Estatística do ICMC Júnior, focado em Análise de Dados e Machine Learning.

## Objetivo

O objetivo principal deste projeto é utilizar uma base de dados de RH (HR Analytics) para construir um modelo de Machine Learning capaz de **prever se um funcionário vai sair da empresa (attrition)**.

## Dataset

O dataset original (`dados.csv`) é uma base de dados de RH contendo diversas informações sobre os funcionários, como:
* Idade (Age)
* Taxa de saída (Attrition)
* Frequência de viagens (BusinessTravel)
* Departamento (Department)
* Renda Mensal (MonthlyIncome)
* Horas Extras (OverTime)
* Anos na Companhia (YearsAtCompany)
* E outras 30+ variáveis.

## Estrutura do Projeto

O projeto foi dividido em três etapas principais, cada uma documentada em seu respectivo notebook:

1.  **`main.ipynb`**: Limpeza e Pré-processamento dos Dados.
2.  **`eda.ipynb`**: Análise Exploratória dos Dados (EDA).
3.  **`modelagem.ipynb`**: Modelagem, Treinamento e Avaliação dos Modelos de Machine Learning.

## Metodologia

### 1. Limpeza e Pré-processamento (`main.ipynb`)

Nesta etapa, o dataset `dados.csv` foi preparado para a análise. As principais ações incluíram:

* **Remoção de Colunas Constantes/Irrelevantes:** Foram removidas colunas que não agregam valor preditivo, como `EmployeeCount`, `Over18`, `StandardHours` (valores constantes) e `EmployeeNumber` (ID).
* **Tratamento de Valores Ausentes (NaN):**
    * Colunas categóricas (ex: `BusinessTravel`) tiveram os valores nulos preenchidos com a **moda** (valor mais frequente).
    * Colunas quantitativas (ex: `DistanceFromHome`) tiveram os valores nulos preenchidos com a **mediana**, por ser mais robusta a outliers.
* **Tratamento de Outliers:** Foi utilizada a técnica de **Clipping (IQR)** para limitar valores extremos em colunas numéricas, substituindo-os pelos limites inferior ou superior calculados.
* **Transformação de Dados:** Colunas com forte assimetria (como `MonthlyIncome`) passaram por uma transformação logarítmica (`log1p`) para normalizar sua distribuição.
* **Padronização Textual:** Colunas de texto foram convertidas para minúsculas e tiveram espaços extras removidos.


### 2. Análise Exploratória (EDA) (`eda.ipynb`)

Com os dados limpos, foi realizada uma análise exploratória para extrair insights e entender a relação das variáveis com a variável alvo (`Attrition`). Principais descobertas:

* **Relação com Horas Extras (Overtime):** Funcionários que fazem horas extras têm uma probabilidade quase **3 vezes maior** de deixar a empresa (taxa de attrition de 30.5%) em comparação com os que não fazem (10.7%).
* **Relação com Renda Mensal (MonthlyIncome):** Utilizando um boxplot, observou-se que os funcionários que saíram (`Attrition=yes`) possuíam, em geral, uma **renda mensal menor** do que os que permaneceram.
* **Relação com Departamento (Department):** A análise mostrou que o departamento de **Vendas (Sales)** possui a maior taxa de attrition (cerca de 21%), enquanto **Pesquisa e Desenvolvimento (R&D)** possui a menor (13.8%).
* **Matriz de Correlação:** Foi gerado um heatmap e um gráfico de barras utilizando o Coeficiente de Correlação de Pearson para visualizar a relação linear de todas as variáveis com o `Attrition`.

### 3. Modelagem e Avaliação (`modelagem.ipynb`)

Na etapa final, os dados foram preparados para a modelagem e dois algoritmos foram treinados e avaliados:

* **Preparação dos Dados:**
    * **Label Encoding:** Colunas categóricas binárias (`Attrition`, `OverTime`, `Gender`) foram convertidas para 0 e 1.
    * **One-Hot Encoding:** Colunas nominais com múltiplas categorias (`BusinessTravel`, `Department`, `JobRole`, etc.) foram transformadas em colunas dummies.
    * **Padronização (Scaling):** Os dados foram padronizados usando `StandardScaler` (média 0, desvio padrão 1).
    * **Divisão Treino/Teste:** Os dados foram divididos em 75% para treino e 25% para teste, de forma estratificada para manter a proporção da variável alvo.

* **Modelos de Classificação:**
    * **Regressão Logística:**
        * Hiperparâmetros otimizados com Grid Search (Melhores: `C=10`, `solver='liblinear'`).
        * Limiar de decisão ajustado para 0.3 para priorizar a identificação de possíveis saídas (aumentando o recall).
        * **Resultado (Teste):** Acurácia de 69.02%, com um **Recall de 80%** para a classe ("Yes" - 1) previsão de saída.
    * **Random Forest Classifier:**
        * Hiperparâmetros otimizados com Grid Search (Melhores: `max_depth=5`, `min_samples_leaf=4`, `n_estimators=100`).
        * Limiar de decisão ajustado para 0.35.
        * **Resultado (Teste):** Acurácia de 64.13%, com um **Recall de 85%** para a classe ("Yes" - 1).

## Bibliotecas Utilizadas

* **pandas**: Para manipulação e limpeza dos dados.
* **numpy**: Para operações numéricas.
* **matplotlib**: Para a geração de gráficos.
* **seaborn**: Para visualização de dados estatísticos (Heatmaps, Boxplots, etc.).
* **scikit-learn** (sklearn): Para pré-processamento (StandardScaler, Encoders), divisão treino/teste, e implementação dos modelos (LogisticRegression, RandomForestClassifier) e avaliação (GridSearch, classification_report).

## Contribuidores

* Daniel Jorge Manzano
* Lucas Alves da Silva
* Luis Henrique Ponciano dos Santos
* Pablo Henrique Almeida Vieira
