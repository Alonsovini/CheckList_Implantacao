# CheckList de Implantação

import streamlit as st
import pandas as pd
import os

# Nome do arquivo Excel
FILE_PATH = "checklist.xlsx"


# Função para carregar os dados iniciais
def load_initial_data():
    # Lista de tarefas
    tarefas = [
        "Coletar no mínimo 3 lacres de cada bomba", "Validar a estrutura de Tanques",
        "Deixar todos os caixas importados no LBC",
        "Deixar todas as NFs lançadas no LBC", "Conferir Nome dos colaboradores no Cofre",
        "Validar preço de Venda Dos Combustíveis", "Sangria e Coleta Antes do Fechamento",
        "Realizar corte do carro forte no LBC", "Conferir saldo LBC VS Cofre", "Coletar Medição dos tanques",
        "Coletar Encerrantes digital de todos os bicos", "Importar último caixa no LBC",
        "Validar Medição de Tanques (LMC)", "Validar Preço de Custo dos Combustíveis no LBC",
        "Abrir o primeiro caixa com o usuário do gerente", "Validar (hexa), fazer aferição em todos os bicos",
        "Conferir CNPJ nas POS", "Testar meios de pagamento (Pix,Credito, Debito, Dinheiro e B2B)",
        "Validar se está pedindo codigo de vendedor somente em produtos comissionados", "Em Loja, Fazer teste com produtos que mais vendem",
        "Em Automotivo, Fazer teste com Oleo mais vendido", "Conferir saldo de estoque no PDV (Após ok da Auditoria)",
        "Fazer corte de caixa após 30 minutos de testes (Conferir Encerrantes)", "Postos de Rodovia, Emitir danfe no PDV",
        "Baixa de aferição em todos os tipos de combustíveis", "Testar baixa na POS",
        "Baixar o restante das Aferições"
    ]

    # Lista de tópicos (mesmo número de itens que a lista de tarefas)
    topicos = ["Pré-Instalação"] * 7 + ["Instalação"] * 7 + ["Pós-Instalação"] * 13

    # Lista de status (mesmo número de itens que a lista de tarefas)
    concluido = ["FALSE"] * len(tarefas)

    # Criar DataFrame
    df = pd.DataFrame({
        "Tópico": topicos,
        "Tarefas": tarefas,
        "Concluído": concluido
    })
    return df


# Função para carregar os dados da empresa selecionada
def load_data(empresa):
    if empresa not in st.session_state:
        st.session_state[empresa] = load_initial_data()  # Carrega dados iniciais se a empresa não existir
    return st.session_state[empresa]


# Função para salvar os dados da empresa selecionada
def save_data(df, empresa):
    st.session_state[empresa] = df


# Função para resetar o checklist da empresa selecionada
def reset_data(df, empresa):
    df["Concluído"] = "FALSE"
    save_data(df, empresa)
    st.success("Checklist zerado com sucesso!")


# Função para obter o índice do status
def get_status_index(status):
    options = ["TRUE", "FALSE", "NÃO SE APLICA"]
    status = str(status).strip() if pd.notna(status) else "FALSE"
    return options.index(status) if status in options else 1


# Customização com HTML e CSS
st.markdown(
    """
    <style>
    /* Aplicar gradiente ao fundo da página */
    .stApp {
        background: linear-gradient(135deg, #22e6b9, #7525b9);
        background-attachment: fixed;
        background-size: cover;
    }

    /* Centralizar o título */
    .centered-title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: black;
        margin-bottom: 30px;
    }

    /* Estilo das tarefas */
    .task-font {
        font-size: 40px;
        font-weight: bold;
        margin-top: 20px;
        color: black;
    }

    /* Reduzir espaçamento entre a tarefa e o selectbox */
    .stSelectbox {
        margin-top: -40px !important;
    }

    /* Estilo dos botões */
    .stButton button {
        background-color: #4F8BF9;
        color: black;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }

    /* Estilo dos selectboxes */
    .stSelectbox select {
        background-color: black;
        color: black;
        border-radius: 5px;
        padding: 5px;
    }

    /* Corrigir cor de fundo dos containers */
    .stContainer {
        background-color: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título centralizado
st.markdown('<p class="centered-title">Checklist de Implantação</p>', unsafe_allow_html=True)

# Inicializar a lista de empresas no session_state
if "empresas" not in st.session_state:
    st.session_state.empresas = []

# Seletor de empresa
empresa_selecionada = st.selectbox(
    "Selecione ou adicione uma empresa:",
    options=st.session_state.empresas,
    index=0 if st.session_state.empresas else None,
    key="empresa_selecionada"
)

# Campo para adicionar nova empresa
nova_empresa = st.text_input("Adicione uma nova empresa:", key="nova_empresa")

# Adicionar nova empresa à lista
if nova_empresa and nova_empresa not in st.session_state.empresas:
    st.session_state.empresas.append(nova_empresa)
    st.success(f"Empresa '{nova_empresa}' adicionada com sucesso!")
    st.rerun()  # Atualiza a interface para mostrar a nova empresa

# Verificar se uma empresa foi selecionada
if empresa_selecionada:
    # Carregar dados da empresa selecionada
    df = load_data(empresa_selecionada)

    # Garantir que a "Pré-Instalação" apareça primeiro
    topicos_ordenados = ["Pré-Instalação"] + [str(t) for t in df["Tópico"].dropna().astype(str).unique() if
                                              str(t) != "Pré-Instalação"]

    for topico in topicos_ordenados:
        if topico in df["Tópico"].dropna().astype(str).unique():
            st.subheader(topico)
            topico_df = df[df["Tópico"].astype(str).fillna("") == topico]
            for index, row in topico_df.iterrows():
                status_options = ["TRUE", "FALSE", "NÃO SE APLICA"]
                status_index = get_status_index(row["Concluído"])

                # Exibe a tarefa com fonte maior
                st.write(f"<p class='task-font'>{row['Tarefas']}</p>", unsafe_allow_html=True)

                # Selectbox para escolher TRUE, FALSE ou NÃO SE APLICA
                new_status = st.selectbox(
                    " ",
                    status_options,
                    index=status_index,
                    key=f"{empresa_selecionada}_{row['Tópico']}_{index}",
                    format_func=lambda x: f"✅ {x}" if x == "TRUE" else f"❌ {x}" if x == "FALSE" else f"➖ {x}",
                )
                df.at[index, "Concluído"] = new_status

    # Botões de salvar e zerar
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Salvar Progresso"):
            save_data(df, empresa_selecionada)
            st.success("Progresso salvo!")
    with col2:
        if st.button("Zerar Checklist"):
            reset_data(df, empresa_selecionada)
else:
    st.warning("Por favor, selecione ou adicione uma empresa para começar.")

