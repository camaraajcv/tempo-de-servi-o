import streamlit as st
from datetime import datetime, timedelta
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

    # Passo 1: Verificar se está na regra de transição
    if data_ingresso <= data_referencia:
        # Calcular o tempo de serviço até 17/12/2019
        tempo_servico_ate_referencia = diferenca_referencia

        # Passo 2: Se já tinha 30 anos de serviço até 17/12/2019, pode pedir a reserva a qualquer momento
        if diferenca_referencia.years >= 30:
            passo_a_passo.append(f"Passo 2: Já tinha 30 anos de serviço até 17/12/2019.")
            return 0, 0, 0, tempo_servico_ate_referencia, 0, data_referencia, passo_a_passo
        else:
            # Calcular o tempo que falta considerando 30 anos
            tempo_faltante = relativedelta(
                years=(30 - diferenca_referencia.years),
                months=-diferenca_referencia.months,
                days=-diferenca_referencia.days
            )

            # Calcular os 17% do tempo total que falta até atingir 30 anos
            percentual_17 = int((tempo_faltante.years * 365 + tempo_faltante.months * 30 + tempo_faltante.days) * 0.17)

            # Adicionar os 17% ao tempo total que falta
            tempo_faltante_ajustado = relativedelta(
                years=tempo_faltante.years + int(percentual_17 / 365),
                months=0,  # Manter os meses zerados para evitar contagem duplicada
                days=(percentual_17 % 365)
            )

            # Calcular a data de aposentadoria
            data_aposentadoria = data_referencia + tempo_faltante_ajustado

            # Registrar o passo a passo
            passo_a_passo.append(f"Passo 2: Tempo que falta considerando 30 anos: {tempo_faltante}")
            passo_a_passo.append(f"Passo 3: Acréscimo de 17% em anos e dias: {percentual_17} dias")
            passo_a_passo.append(f"Passo 4: Ajuste com acréscimo de 17%: {tempo_faltante_ajustado}")
            passo_a_passo.append(f"Passo 5: Data de aposentadoria: {data_aposentadoria.strftime('%d-%m-%Y')}")
            return tempo_faltante_ajustado.years, tempo_faltante_ajustado.months, tempo_faltante_ajustado.days, tempo_servico_ate_referencia, tempo_faltante, data_aposentadoria, passo_a_passo
    else:
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
    st.write(f"Tempo de serviço até 17/12/2019: {tempo_servico_ate_referencia.years} anos, {tempo_servico_ate_referencia.months} meses e {tempo_servico_ate_referencia.days} dias")
    st.write(f"Tempo faltante após 17/12/2019: {tempo_faltante.years} anos, {tempo_faltante.months} meses e {tempo_faltante.days} dias")
    st.write(f"Data provável de aposentadoria: {data_aposentadoria.strftime('%d-%m-%Y')}")
    
    st.subheader("Passo a Passo:")
    for passo in passo_a_passo:
        st.write(passo)
else:
    st.write("Por favor, insira uma data válida no formato DD-MM-YYYY.")
