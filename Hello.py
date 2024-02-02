import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def calcular_tempo_reserva(data_ingresso):
    # Data de referência para a lei (17/12/2019)
    data_referencia = datetime(2019, 12, 17)

    # Calcular anos, meses e dias até a data de referência
    diferenca_referencia = relativedelta(data_referencia, data_ingresso)

    # Inicializar variáveis para o acompanhamento passo a passo
    passo_a_passo = []

    # Se entrou após 17/12/2019, precisa cumprir 35 anos de serviço
    tempo_faltante = relativedelta(years=35) - diferenca_referencia
    data_aposentadoria = data_referencia + tempo_faltante

    # Registrar o passo a passo
    passo_a_passo.append("Passo 1: Entrou após 17/12/2019.")
    passo_a_passo.append(f"Passo 2: Tempo que falta considerando 35 anos: {tempo_faltante}")
    passo_a_passo.append(f"Passo 3: Data de aposentadoria: {data_aposentadoria.strftime('%d-%m-%Y')}")
    return tempo_faltante.years, tempo_faltante.months, tempo_faltante.days, 0, tempo_faltante, data_aposentadoria, passo_a_passo

# Configurações da página
st.title('Calculadora de Reserva Remunerada para Militares')

# Solicitar a data de ingresso do usuário
data_ingresso_str = st.text_input('Digite a data de ingresso (DD-MM-YYYY):')

# Validar a entrada do usuário
if is_valid_date(data_ingresso_str):
    data_ingresso = datetime.strptime(data_ingresso_str, "%d-%m-%Y")
    
    # Calcular o tempo de serviço restante e a data de aposentadoria
    anos, meses, dias, tempo_servico_ate_referencia, tempo_faltante, data_aposentadoria, passo_a_passo = calcular_tempo_reserva(data_ingresso)
    
    # Exibir os resultados e o passo a passo
    if data_ingresso >= data_referencia:
        st.write(f"Tempo total de serviço: {tempo_servico_ate_referencia.years} anos, {tempo_servico_ate_referencia.months} meses e {tempo_servico_ate_referencia.days} dias")
        st.write(f"Data provável de aposentadoria: {data_aposentadoria.strftime('%d-%m-%Y')}")
    else:
        st.write(f"Tempo de serviço até 17/12/2019: {tempo_servico_ate_referencia.years} anos, {tempo_servico_ate_referencia.months} meses e {tempo_servico_ate_referencia.days} dias")
        st.write(f"Tempo faltante após 17/12/2019: {tempo_faltante.years} anos, {tempo_faltante.months} meses e {tempo_faltante.days} dias")
        st.write(f"Data provável de aposentadoria: {data_aposentadoria.strftime('%d-%m-%Y')}")
    
    st.subheader("Passo a Passo:")
    for passo in passo_a_passo:
        st.write(passo)
else:
    st.write("Por favor, insira uma data válida no formato DD-MM-YYYY.")
