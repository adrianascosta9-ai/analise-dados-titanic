import sqlite3
import pandas as pd
from scipy.stats import chi2_contingency

try:
    # ==========================================
    # 1. CONEXÃO COM O BANCO
    # ==========================================

    conexao = sqlite3.connect("titanic.db")

    # Executa o DDL
    with open("modelo_titanic.sql", "r", encoding="utf-8") as arquivo:
        script_sql = arquivo.read()

    conexao.executescript(script_sql)

    print("DDL executado com sucesso!")

    # ==========================================
    # 2. LEITURA DOS DADOS
    # ==========================================

    df = pd.read_csv("titanic.txt")

    print("\nQuantidade de linhas e colunas:")
    print(df.shape)

    print("\nNome das colunas:")
    print(df.columns)

    print("\nInformações do DataFrame:")
    df.info()

    # ==========================================
    # 3. ANÁLISE DOS DADOS
    # ==========================================

    print("\nValores nulos:")
    print(df.isnull().sum())

    print("\nQuantidade de linhas duplicadas:")
    print(df.duplicated().sum())

    print("\nEstatísticas:")
    print(df.describe())

    print("\nPrimeiros registros:")
    print(df.head())

    print("\nMediana da idade:")
    print(df["Age"].median())

    print("\nDistribuição de embarque:")
    print(df["Embarked"].value_counts())

    # ==========================================
    # 4. TRATAMENTO DOS DADOS
    # ==========================================

    # Tratamento da coluna Age
    mediana_idade = df["Age"].median()
    df["Age"] = df["Age"].fillna(mediana_idade)

    # Tratamento da coluna Embarked
    moda_embarked = df["Embarked"].mode()[0]
    df["Embarked"] = df["Embarked"].fillna(moda_embarked)

    # Remoção da coluna Cabin
    df = df.drop(columns=["Cabin"])

    print("\nValores nulos após o tratamento:")
    print(df.isnull().sum())

    print("\nColunas após o tratamento:")
    print(df.columns)

    # ==========================================
    # 5. ANÁLISES DE SOBREVIVÊNCIA
    # ==========================================

    print("\nQuantidade de passageiros por sobrevivência:")
    print(df["Survived"].value_counts())

    print("\nPercentual de sobrevivência:")
    print(df["Survived"].value_counts(normalize=True) * 100)

    print("\nSobrevivência por sexo:")
    print(df.groupby("Sex")["Survived"].mean() * 100)

    print("\nSobrevivência por classe:")
    print(df.groupby("Pclass")["Survived"].mean() * 100)

    print("\nSobrevivência por sexo e classe:")
    print(df.groupby(["Sex", "Pclass"])["Survived"].mean() * 100)

    # ==========================================
    # 6. CARGA DOS PASSAGEIROS - DML
    # ==========================================

    for _, linha in df.iterrows():

        conexao.execute("""
            INSERT OR IGNORE INTO passageiro
            (
                passenger_id,
                nome,
                sexo,
                idade,
                sobrevivente,
                classe_id,
                sib_sp,
                parch,
                ticket,
                fare,
                embarked
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(linha["PassengerId"]),
            linha["Name"],
            linha["Sex"],
            float(linha["Age"]),
            int(linha["Survived"]),
            int(linha["Pclass"]),
            int(linha["SibSp"]),
            int(linha["Parch"]),
            linha["Ticket"],
            float(linha["Fare"]),
            linha["Embarked"]
        ))

    conexao.commit()

    print("\nDML executado com sucesso!")

    quantidade = conexao.execute(
        "SELECT COUNT(*) FROM passageiro"
    ).fetchone()[0]

    print("Passageiros carregados:", quantidade)

    # ==========================================
    # 7. DIAGNÓSTICO ESTATÍSTICO
    # ==========================================

    idade = df["Age"]

    print("\n==========================================")
    print("DIAGNÓSTICO ESTATÍSTICO")
    print("==========================================")

    # Medidas de posição
    print("\n--- Medidas de posição ---")

    print("Média da idade:", round(idade.mean(), 2))
    print("Mediana da idade:", round(idade.median(), 2))
    print("Moda da idade:", round(idade.mode()[0], 2))

    # Medidas de variabilidade
    print("\n--- Medidas de variabilidade ---")

    print("Idade mínima:", round(idade.min(), 2))
    print("Idade máxima:", round(idade.max(), 2))
    print("Amplitude:", round(idade.max() - idade.min(), 2))
    print("Variância:", round(idade.var(), 2))
    print("Desvio padrão:", round(idade.std(), 2))

    # ==========================================
    # 8. TESTE DE HIPÓTESE
    # ==========================================

    print("\n==========================================")
    print("TESTE DE HIPÓTESE")
    print("==========================================")

    # H0: não existe associação entre sexo e sobrevivência
    # H1: existe associação entre sexo e sobrevivência

    tabela = pd.crosstab(
        df["Sex"],
        df["Survived"]
    )

    print("\nTabela de contingência:")
    print(tabela)

    # Teste Qui-Quadrado
    qui2, p_valor, graus_liberdade, esperados = chi2_contingency(tabela)

    print("\nResultado do teste Qui-Quadrado:")
    print("Qui-quadrado:", round(qui2, 4))
    print("Graus de liberdade:", graus_liberdade)
    print("P-valor:", p_valor)

    # Nível de significância
    alpha = 0.05

    print("\nNível de significância:", alpha)

    if p_valor < alpha:
        print("\nConclusão:")
        print("Rejeitamos H0.")
        print(
            "Existe associação estatisticamente significativa "
            "entre sexo e sobrevivência."
        )
    else:
        print("\nConclusão:")
        print("Não rejeitamos H0.")
        print(
            "Não existem evidências suficientes de associação "
            "entre sexo e sobrevivência."
        )

except FileNotFoundError as erro:
    print("Arquivo não encontrado:", erro)

except pd.errors.EmptyDataError:
    print("O arquivo de dados está vazio.")

except pd.errors.ParserError as erro:
    print("Erro ao ler o arquivo:", erro)

except sqlite3.Error as erro:
    print("Erro no banco de dados:", erro)

except Exception as erro:
    print("Erro inesperado:", erro)

finally:
    try:
        conexao.close()
    except:
        pass