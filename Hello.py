# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from datetime import datetime, timedelta
from inputmask import inputmask

def calcular_tempo_reserva(data_ingresso):
    # Data de referência para a lei (17/12/2019)
    data_referencia = datetime(2019, 12, 17)

    # Calcular anos, meses e dias até a data de referência
    diferenca = data_referencia - data_ingresso
    anos_servico_atual = diferenca.days // 365
    meses_servico_atual = (diferenca.days % 365) // 30

    # Tempo de serviço atual
    tempo_atual = timedelta(days=(anos_servico_atual * 365) + (meses_servico_atual * 30))

    # Verificar se está na regra de transição
    if data_ingresso <= data_referencia:
        # Se já tinha 30 anos de serviço até 17/12/2019, pode pedir a reserva a qualquer momento
        if anos_servico_atual >= 30:
            return timedelta(days=0)
        else:
            # Calcular o tempo que falta considerando o acréscimo de 17%
            tempo_faltante = timedelta(days=((30 - anos_servico_atual) * 365 * 1.17))
            return tempo_faltante - tempo_atual
    else:
        # Se entrou após 17/12/2019, precisa cumprir 35 anos de serviço
        tempo_faltante = timedelta(days=(35 * 365))
        return tempo_faltante - tempo_atual

# Configurações da página
st.title('Calculadora de Reserva Remunerada para Militares')

# Solicitar a data de ingresso do usuário com máscara
data_ingresso_str = st.text_input('Digite a data de ingresso (DD-MM-YYYY):')
data_ingresso = datetime.strptime(data_ingresso_str, "%d-%m-%Y") if data_ingresso_str else None

# Calcular o tempo de serviço restante
if data_ingresso:
    tempo_faltante = calcular_tempo_reserva(data_ingresso)
    st.write(f"Tempo faltante para a reserva remunerada: {tempo_faltante.days} dias")
