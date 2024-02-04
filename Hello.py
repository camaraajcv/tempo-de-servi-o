import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

def calcular_tempo_servico(data_ingresso, data_lei, anos_extras, anos_localidade_especial):
    if data_ingresso >= datetime.combine(data_lei, datetime.min.time()).date():
        # Tempo de serviço após a lei
        delta_tempo_servico = datetime.now() - datetime.combine(data_ingresso, datetime.min.time())
        anos = delta_tempo_servico.days / 365.25  # Usar 365.25 para considerar anos bissextos
        meses = (delta_tempo_servico.days % 365.25) / 30.44  # Usar 30.44 para considerar a média de dias por mês
        dias = (delta_tempo_servico.days % 365.25) % 30.44  # Usar 30.44 para considerar a média de dias por mês

        #Calcular a data futura de reserva remunerada considerando anos extras e anos de localidade especial
        anos_extras_total = anos_extras + (anos_localidade_especial // 2) * (2/3)
        data_reserva_remunerada = calcular_data_futura_reserva(data_ingresso, 35) - timedelta(days=365.25 * anos_extras_total)

      

        # Criar uma contagem regressiva para a futura reserva considerando anos extras
        hoje = datetime.now()
        tempo_restante = (data_reserva_remunerada - hoje)
        anos_restantes = int(tempo_restante.days / 365.25)
        meses_restantes = int((tempo_restante.days % 365.25) / 30.44)
        dias_restantes = int((tempo_restante.days % 365.25) % 30.44)
        horas_restantes, resto_horas = divmod(tempo_restante.seconds, 3600)
        minutos_restantes, _ = divmod(resto_horas, 60)

        # Normalizar a porcentagem para um valor entre 0.0 e 1.0
        percent_tempo_restante = min(100, max(0, (tempo_restante.total_seconds() / (35 * 365 * 24 * 3600)) * 100))

        # Exibir barra de progresso invertida
        st.markdown("Contagem regressiva para a reserva:")
        st.progress(1.0 - percent_tempo_restante / 100.0)

        # Exibir texto de sucesso
        st.success(
            f"**Data futura de reserva remunerada:** {data_reserva_remunerada.strftime('%d/%m/%Y')}. "
            f"**Contagem regressiva para a reserva:** {anos_restantes} anos, {meses_restantes} meses, {dias_restantes} dias, {horas_restantes} horas, {minutos_restantes} minutos."
        )

        return (
                f"<p><strong>Regra de Transição para Reserva Remunerada</strong></p>"
                f"<p>Se você ingressou no serviço militar até 17/12/2019, uma nova regra de transição foi estabelecida:</p>"
                f"<p>1. Se já tinha 30 anos de serviço até essa data, você pode solicitar a reserva remunerada a qualquer momento devido ao direito adquirido.</p>"
                f"<p>2. Caso não tenha completado 30 anos até 17/12/2019, será necessário cumprir o tempo restante para atingir os 30 anos, acrescido de 17%. Desse acréscimo, 25 anos devem ser de atividade militar nas Forças Armadas.</p>"
                f"<p>Por exemplo, um militar com 20 anos de serviço em 17/12/2019 precisará cumprir mais 10 anos, com acréscimo de 1,7 anos, totalizando 31 anos, 8 meses e 12 dias de serviço para ter direito à reserva remunerada.</p>"
                f"<p>Assim, se você entrou no serviço militar até 17/12/2019, verifique quanto tempo faltava para completar 30 anos de serviço naquela data. Calcule 17% desse tempo para acrescentá-lo ao período necessário para a reserva remunerada.</p>"
                f"<p>Para os que ingressarem no serviço militar após 17/12/2019, será obrigatório cumprir 35 anos de serviço para ter direito à reserva remunerada.</p>"
                f"<p>Quanto aos oficiais formados em instituições específicas e praças, os 25 anos nas Forças Armadas terão um acréscimo de 4 meses a cada ano, a partir de 2021, até atingir 30 anos.</p>"
            
        )

    else:
        # Tempo de serviço antes da lei
        delta_tempo_servico = datetime.combine(data_lei, datetime.min.time()) - datetime.combine(data_ingresso, datetime.min.time())
        anos_antes_lei = delta_tempo_servico.days / 365.25  # Usar 365.25 para considerar anos bissextos

        # Verificar se o militar está sujeito à regra de transição
        if anos_antes_lei < 30:
            tempo_faltante = 30 - anos_antes_lei
            tempo_transicao = tempo_faltante * 0.17
            # Calcular a data futura de reserva remunerada
            anos_extras_total = anos_extras + (anos_localidade_especial // 2) * (2/3)

            data_reserva_remunerada = calcular_data_futura_reserva(data_ingresso, 30 + tempo_transicao)- timedelta(days=365.25 * anos_extras_total)

            # Criar uma contagem regressiva para a futura reserva
            hoje = datetime.now()
            tempo_restante = (data_reserva_remunerada - hoje)
            percent_tempo_restante = min(100, max(0, (tempo_restante.total_seconds() / (30 * 365 * 24 * 3600)) * 100))  # Limitar a 100%
            anos_restantes = int(tempo_restante.days / 365.25)
            meses_restantes = int((tempo_restante.days % 365.25) / 30.44)
            dias_restantes = int((tempo_restante.days % 365.25) % 30.44)
            horas_restantes, resto_horas = divmod(tempo_restante.seconds, 3600)
            minutos_restantes, _ = divmod(resto_horas, 60)

            # Normalizar a porcentagem para um valor entre 0.0 e 1.0
            normalized_percent_tempo_restante = percent_tempo_restante / 100.0

            # Exibir barra de progresso invertida
            st.markdown("Contagem regressiva para a reserva:")
            st.progress(1.0 - normalized_percent_tempo_restante)

            # Exibir texto de sucesso
            st.success(
                f"**Data futura de reserva remunerada:** {data_reserva_remunerada.strftime('%d/%m/%Y')}. "
                f"**Contagem regressiva para a reserva:** {anos_restantes} anos, {meses_restantes} meses, {dias_restantes} dias, {horas_restantes} horas, {minutos_restantes} minutos."
            )

            return (
                f"<p><strong>Regra de Transição para Reserva Remunerada</strong></p>"
                f"<p>Se você ingressou no serviço militar até 17/12/2019, uma nova regra de transição foi estabelecida:</p>"
                f"<p>1. Se já tinha 30 anos de serviço até essa data, você pode solicitar a reserva remunerada a qualquer momento devido ao direito adquirido.</p>"
                f"<p>2. Caso não tenha completado 30 anos até 17/12/2019, será necessário cumprir o tempo restante para atingir os 30 anos, acrescido de 17%. Desse acréscimo, 25 anos devem ser de atividade militar nas Forças Armadas.</p>"
                f"<p>Por exemplo, um militar com 20 anos de serviço em 17/12/2019 precisará cumprir mais 10 anos, com acréscimo de 1,7 anos, totalizando 31 anos, 8 meses e 12 dias de serviço para ter direito à reserva remunerada.</p>"
                f"<p>Assim, se você entrou no serviço militar até 17/12/2019, verifique quanto tempo faltava para completar 30 anos de serviço naquela data. Calcule 17% desse tempo para acrescentá-lo ao período necessário para a reserva remunerada.</p>"
                f"<p>Para os que ingressarem no serviço militar após 17/12/2019, será obrigatório cumprir 35 anos de serviço para ter direito à reserva remunerada.</p>"
                f"<p>Quanto aos oficiais formados em instituições específicas e praças, os 25 anos nas Forças Armadas terão um acréscimo de 4 meses a cada ano, a partir de 2021, até atingir 30 anos.</p>"
                
            )
        else:
            # Tempo de serviço após a lei
            delta_tempo_servico = datetime.now() - datetime.combine(data_ingresso, datetime.min.time())
            anos = delta_tempo_servico.days / 365.25  # Usar 365.25 para considerar anos bissextos
            meses = (delta_tempo_servico.days % 365.25) / 30.44  # Usar 30.44 para considerar a média de dias por mês
            dias = (delta_tempo_servico.days % 365.25) % 30.44  # Usar 30.44 para considerar a média de dias por mês

            # Calcular a data futura de reserva remunerada
            data_reserva_remunerada = calcular_data_futura_reserva(data_ingresso, 35 - anos_extras)

            # Criar uma contagem regressiva para a futura reserva
            hoje = datetime.now()
            tempo_restante = (data_reserva_remunerada - hoje)
            percent_tempo_restante = min(100, max(0, (tempo_restante.total_seconds() / (35 * 365 * 24 * 3600)) * 100))  # Limitar a 100%
            anos_restantes = int(tempo_restante.days / 365.25)
            meses_restantes = int((tempo_restante.days % 365.25) / 30.44)
            dias_restantes = int((tempo_restante.days % 365.25) % 30.44)
            horas_restantes, resto_horas = divmod(tempo_restante.seconds, 3600)
            minutos_restantes, _ = divmod(resto_horas, 60)

            # Normalizar a porcentagem para um valor entre 0.0 e 1.0
            normalized_percent_tempo_restante = percent_tempo_restante / 100.0

            # Exibir barra de progresso invertida
            st.markdown("Contagem regressiva para a reserva:")
            st.progress(1.0 - normalized_percent_tempo_restante)

            # Exibir texto de sucesso
            st.success(
                f"**Data futura de reserva remunerada:** {data_reserva_remunerada.strftime('%d/%m/%Y')}. "
                f"**Contagem regressiva para a reserva:** {anos_restantes} anos, {meses_restantes} meses, {dias_restantes} dias, {horas_restantes} horas, {minutos_restantes} minutos."
            )

            return (
                f"<p><strong>Regra de Transição para Reserva Remunerada</strong></p>"
                f"<p>Se você ingressou no serviço militar até 17/12/2019, uma nova regra de transição foi estabelecida:</p>"
                f"<p>1. Se já tinha 30 anos de serviço até essa data, você pode solicitar a reserva remunerada a qualquer momento devido ao direito adquirido.</p>"
                f"<p>2. Caso não tenha completado 30 anos até 17/12/2019, será necessário cumprir o tempo restante para atingir os 30 anos, acrescido de 17%. Desse acréscimo, 25 anos devem ser de atividade militar nas Forças Armadas.</p>"
                f"<p>Por exemplo, um militar com 20 anos de serviço em 17/12/2019 precisará cumprir mais 10 anos, com acréscimo de 1,7 anos, totalizando 31 anos, 8 meses e 12 dias de serviço para ter direito à reserva remunerada.</p>"
                f"<p>Assim, se você entrou no serviço militar até 17/12/2019, verifique quanto tempo faltava para completar 30 anos de serviço naquela data. Calcule 17% desse tempo para acrescentá-lo ao período necessário para a reserva remunerada.</p>"
                f"<p>Para os que ingressarem no serviço militar após 17/12/2019, será obrigatório cumprir 35 anos de serviço para ter direito à reserva remunerada.</p>"
                f"<p>Quanto aos oficiais formados em instituições específicas e praças, os 25 anos nas Forças Armadas terão um acréscimo de 4 meses a cada ano, a partir de 2021, até atingir 30 anos.</p>"
                                
            )

def calcular_data_futura_reserva(data_ingresso, anos_futura_reserva):
    anos = int(anos_futura_reserva)
    meses_faltantes = (anos_futura_reserva - anos) * 12
    meses = int(meses_faltantes)
    dias_faltantes = (meses_faltantes - meses) * 30.44  # Usar 30.44 para considerar a média de dias por mês
    dias = int(dias_faltantes)

    data_reserva_remunerada = datetime.combine(data_ingresso, datetime.min.time()) + timedelta(days=anos * 365 + meses * 30.44 + dias)
    return data_reserva_remunerada

def main():
    st.set_page_config(
    page_title="Tempo de Serviço",
    page_icon="🧊",
    initial_sidebar_state="collapsed",
    
)
    st.title("Calculadora de Tempo para a reserva nas FFAA")

    # Adicionar explicação sobre as regras
    st.markdown(
    "Este aplicativo calcula o tempo para reserva nas Forças Armadas conforme as regras estabelecidas pela Lei 13.954/2019. "
    "Selecione a data de ingresso, informe os anos extras desejados e os anos completos em localidade especial, e clique no botão 'Calcular' para obter o resultado."
)
    #Selecionar a data de ingresso
    data_ingresso = st.date_input("Selecione a data de ingresso nas FFAA:", min_value=date(1970, 1, 1),format="DD/MM/YYYY")

    # Adicionar checkboxes para indicar se possui tempo extra para averbar e se serviu em localidade especial
    possui_tempo_extra = st.checkbox("Possuo tempo extra para averbar")
    serviu_localidade_especial = st.checkbox("Servi em localidade especial")

    # Se o usuário marcar a checkbox de "Possuo tempo extra para averbar", permitir entrada para anos extras
    anos_extras = 0
    if possui_tempo_extra:
        anos_extras = st.number_input("Informe os anos extras a serem averbados:", min_value=0, max_value=35, step=1, value=0)

    # Se o usuário marcar a checkbox de "Servi em localidade especial", permitir entrada para anos de localidade especial
    anos_localidade_especial = 0
    if serviu_localidade_especial:
        anos_localidade_especial = st.number_input("Informe os anos completos em localidade especial. Lembrando que o tempo a ser considerado equivale a 1/3 (um terço) para cada período consecutivo ou não de 2 (dois) anos de efetivo serviço passados pelo militar nas guarnições especiais da Categoria A, a partir da vigência da Lei nº 5.774, de 23 de dezembro de 1971.                       (Redação dada pela Lei nº 7.698, de 1988):", min_value=0, max_value=10, step=1, value=0)
        st.markdown(
        f"**PORTARIA GM-MD Nº 379, DE 25 DE JANEIRO DE 2022:**" 
        "\n\n"
        f"**Art. 3º** Para efeito desta Portaria, são consideradas localidades especiais de Categoria A as localidades e as vias fluviais e lacustres situadas no território nacional, na região a oeste da linha denominada Alfa que, partindo do litoral, acompanha sucessivamente os limites interestaduais entre Maranhão – Pará, Maranhão – Tocantins, Piauí – Tocantins, Bahia – Tocantins, Goiás – Tocantins, Goiás – Mato Grosso, Goiás – Mato Grosso do Sul, Minas Gerais – Mato Grosso do Sul, São Paulo – Mato Grosso do Sul e Paraná – Mato Grosso do Sul, conforme o mapa constante do Anexo I."
        "Parágrafo único. Consideram-se também como localidades especiais de Categoria A as regiões do Oceano Atlântico situadas ao norte da latitude 01 00 S, durante todo o ano, ao sul da latitude 24 00 S, no período compreendido entre 1º de julho e 30 de setembro, e as relacionadas na Tabela I do Anexo II desta Portaria **(após o mapa)**."
        
                    )
    
        st.image("https://www.in.gov.br/documents/68942/376580666/515%2B2022-01-28%2B14220115-1_MD_14220115_001.jpg/88b9f3fb-f840-0fef-149b-433145152843", use_column_width=True)
        # Criar um DataFrame com os dados da tabela
        data = {
            'UF': ['BA', 'ES', 'GO', 'MA', 'MS', 'PE', 'PR', 'RJ', 'RN', 'RS', 'SC', 'SP'],
            'LOCALIDADES E/OU GUARNIÇÕES NÃO ENQUADRADAS NO ART. 3º': [
                'Arquipélago de Abrolhos e Caravelas',
                'Ilha de Trindade',
                'Aragarças e Porangatu',
                'Farol Preguiças, Farol Araçagy, Farol Santana, Farol São João e Alcântara',
                'Aquidauana',
                'Arquipélago de Fernando de Noronha',
                'Guaíra e Radiofarol Paranaguá',
                'Ilha Rasa, Farol de Macaé, Farol de Cabo Frio, Farol de Castelhanos e Radiofarol de São Tomé',
                'Radiofarol de Calcanhar em Touros e Farol da Ponta do Mel em Areia Branca',
                'Rio Grande, Tramandaí, Farol de Tramandaí, Radiofarol de Tramandaí, Farol de Cidreira, Radiofarol Chuí, Farol Mostardas, Farol Albardão, Radiofarol Rio Grande e Farol da Barra do Rio Grande em São José do Norte',
                'Farol de Santa Marta, Radiofarol da Ilha da Paz, Farol da Ilha do Arvoredo e Urubici',
                'Radiofarol da Ilha da Moela e Farol da Ponta do Boi'
            ]
        }

        df = pd.DataFrame(data)

        # Exibir a tabela no Streamlit
        df
    
    # Definir a data da Lei
    data_lei = date(2019, 12, 17)

    if st.button("Calcular"):
        # Calcular o tempo de serviço
        resultado = calcular_tempo_servico(data_ingresso, data_lei, anos_extras, anos_localidade_especial)

        # Exibir o resultado
        st.markdown(resultado, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("Desenvolvido por Alex Jorge da Camara Vieira")
if __name__ == "__main__":
    main()
