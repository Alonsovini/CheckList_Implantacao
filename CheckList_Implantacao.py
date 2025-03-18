# CheckList de Implantação

import streamlit as st
import pandas as pd
import os

# Nome do arquivo Excel
FILE_PATH = "checklist.xlsx"

# Função para carregar os dados
def load_data():
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
        expected_columns = {"Tópico", "Tarefas", "Concluído"}
        if not expected_columns.issubset(df.columns):
            st.error(f"O arquivo Excel não contém as colunas esperadas. Colunas encontradas: {df.columns.tolist()}")
            st.stop()
        df["Concluído"].fillna("FALSE", inplace=True)
        return df
    else:
        df = pd.DataFrame({
            "Tópico": [
                "Pré-Instalação", "Pré-Instalação", "Pré-Instalação", "Pré-Instalação", "Pré-Instalação", "Pré-Instalação", "Pré-Instalação",
                "Instalação", "Instalação", "Instalação", "Instalação", "Instalação", "Instalação", "Instalação", "Instalação",
                "Pós-Instalação", "Pós-Instalação", "Pós-Instalação", "Pós-Instalação", "Pós-Instalação"
            ],
            "Tarefas": [
                "Coletar no mínimo 3 lacres de cada bomba", "Validar a estrutura de Tanques", "Deixar todos os caixas importados no LBC",
                "Deixar todas as NFs lançadas no LBC", "Conferir Nome dos colaboradores no Cofre", "Validar preço de Venda Dos Combustíveis", "Sangria e Coleta Antes do Fechamento",

                "Realizar corte do carro forte no LBC", "Conferir saldo LBC VS Cofre", "Coletar Medição dos tanques",
                "Coletar Encerrantes digital de todos os bicos", "Importar último caixa no LBC", "Validar Medição de Tanques (LMC)", "Validar Preço de Custo dos Combustíveis no LBC",

                "Abrir o primeiro caixa com o usuário do gerente", "Conferir CNPJ nas POS",
                "Baixa de aferição em todos os tipos de combustíveis", "Testar baixa na POS",
                "Baixar o restante das Aferições",
            ],
            "Concluído": ["FALSE"] * 19
        })
        df.to_excel(FILE_PATH, index=False)
        return df

# Função para salvar os dados
def save_data(df):
    df.to_excel(FILE_PATH, index=False)

# Função para resetar o checklist
def reset_data(df):
    df["Concluído"] = "FALSE"
    save_data(df)
    st.success("Checklist zerado com sucesso!")

# Função para obter o índice do status
def get_status_index(status):
    options = ["TRUE", "FALSE"]
    status = str(status).strip() if pd.notna(status) else "FALSE"
    return options.index(status) if status in options else 1

# Carregar dados
df = load_data()

if df is not None:
    st.write(df)  # Exibe o DataFrame no Streamlit

# Customização com HTML e CSS
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 48px; !important;  /* Aumentei o tamanho da fonte */
        font-weight: bold;
        color: #86d569;
        margin-bottom: 30px;
    }
    .task-font {
        font-size: 29px;
        font-weight: bold;
        margin-top: 20px;
    }
    .true-status {
        color: green;
    }
    .false-status {
        color: red;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título centralizado
st.markdown('<p class=centered-title>Checklist de Implantação</p>', unsafe_allow_html=True)

# Garantir que a "Pré-Instalação" apareça primeiro
topicos_ordenados = ["Pré-Instalação"] + [str(t) for t in df["Tópico"].dropna().astype(str).unique() if
                                          str(t) != "Pré-Instalação"]

for topico in topicos_ordenados:
    if topico in df["Tópico"].dropna().astype(str).unique():
        st.subheader(topico)
        topico_df = df[df["Tópico"].astype(str).fillna("") == topico]
        for index, row in topico_df.iterrows():
            status_options = ["TRUE", "FALSE"]
            status_index = get_status_index(row["Concluído"])

            # Exibe a tarefa com fonte maior
            st.write(f"<p class='task-font'>{row['Tarefas']}</p>", unsafe_allow_html=True)

            # Selectbox para escolher TRUE ou FALSE
            new_status = st.selectbox(
                "Status",
                status_options,
                index=status_index,
                key=f"{row['Tópico']}_{index}",
                format_func=lambda x: f"✅ {x}" if x == "TRUE" else f"❌ {x}",
            )
            df.at[index, "Concluído"] = new_status

# Botões de salvar e zerar
col1, col2 = st.columns(2)
with col1:
    if st.button("Salvar Progresso"):
        save_data(df)
        st.success("Progresso salvo!")
with col2:
    if st.button("Zerar Checklist"):
        reset_data(df)

