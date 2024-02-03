import streamlit as st
from datetime import datetime, date, timedelta

def calcular_tempo_servico(data_ingresso, data_lei):
    # Tempo de serviço antes da lei
    if data_ingresso < datetime.combine(data_lei, datetime.min.time()).date():
        delta_tempo_servico = data_lei - data_ingresso
        anos_antes_lei = delta_tempo_servico.days / 365.25  # Usar 365.25 para considerar anos bissextos

        # Verificar se o militar está sujeito à regra de transição
        if anos_antes_lei < 30:
            tempo_faltante = 30 - anos_antes_lei
            tempo_transicao = tempo_faltante * 0.17
            # Calcular a data futura de reserva remunerada
            data_reserva_remunerada = calcular_data_futura_reserva(data_ingresso, 30 + tempo_transicao)

            # Criar uma contagem regressiva para a futura reserva
            hoje = datetime.now()
            tempo_restante = (data_reserva_remunerada - hoje)
            percent_tempo_restante = min(100, (tempo_restante.total_seconds() / (30 * 365 * 24 * 3600)) * 100)  # Limitar a 100%
            dias_restantes = int(tempo_restante.days)
            horas_restantes, resto_horas = divmod(tempo_restante.seconds, 3600)
            minutos_restantes, _ = divmod(resto_horas, 60)

            # Normalizar a porcentagem para um valor entre 0.0 e 1.0
            normalized_percent_tempo_restante = percent_tempo_restante / 100.0

            # Exibir contagem regressiva para a futura reserva
            st.markdown("Contagem regressiva para a reserva:")
            st.progress(normalized_percent_tempo_restante)
            st.success(f"**{dias_restantes} dias, {horas_restantes} horas, {minutos_restantes} minutos.**")
            st.success(f"**Data futura de reserva remunerada:** {data_reserva_remunerada.strftime('%d/%m/%Y')}. ")
            return (
                "<p><strong>Nova regra da reserva remunerada</strong></p>"
                "<p>Os militares que ingressarem nas Forças Armadas a partir de 17/12/2019 (vigência da reforma) devem cumprir, "
                "no mínimo, 35 anos de tempo de serviço para entrar na reserva remunerada.</p>"
                "<p>No entanto, para que os 35 anos sejam válidos, é preciso cumprir um dos dois requisitos abaixo:</p>"
                "<ol>"
                "<li>30 anos de exercício de atividade de natureza militar nas Forças Armadas, para os oficiais formados nas "
                "seguintes instituições:"
                "   <ul>"
                "       <li>Academia Militar das Agulhas Negras</li>"
                "       <li>Academia da Força Aérea</li>"
                "       <li>Escola Naval</li>"
                "       <li>Instituto Militar de Engenharia</li>"
                "       <li>Instituto Tecnológico de Aeronáutica</li>"
                "       <li>Em escola ou centro de formação de oficiais.</li>"
                "   </ul>"
                "</li>"
                "<li>25 anos de atividade de natureza militar nas Forças Armadas, para militares que não se enquadram nas hipóteses acima.</li>"
                "</ol>"
                "<p>Ao contrário da nova regra de aposentadorias do trabalhador privado, não é preciso ter uma idade mínima para entrar na reserva remunerada.</p>"
                "<p>Para os militares ativos que pretendem entrar na reserva remunerada, há uma regra de transição: é preciso cumprir um pedágio de 17% do tempo que faltava para a aposentadoria até a vigência da reforma. "
                "Como a regra anterior estipulava o tempo mínimo de 30 anos de serviço para entrar na reserva, o militar ativo deverá cumprir 17% a mais sobre o período que falta para dar entrada na aposentadoria."
                "Por exemplo, se faltam 5 anos para um militar completar os 30 anos de serviço quando a reforma entrou em vigor, ele terá que cumprir 5 anos + 17% de pedágio (0,85), totalizando 5,85 anos (cerca de 5 anos e 10 meses) para entrar na reforma remunerada.</p>"
                f"<p><strong>Data futura de reserva remunerada:</strong> {data_reserva_remunerada.strftime('%d/%m/%Y')}. "
                f"<strong>Contagem regressiva para a reserva:</strong> {dias_restantes} dias, {horas_restantes} horas, {minutos_restantes} minutos.</p>"
            )

    # Tempo de serviço após a lei
    delta_tempo_servico = datetime.now() - datetime.combine(data_ingresso, datetime.min.time())
    anos = delta_tempo_servico.days / 365.25  # Usar 365.25 para considerar anos bissextos
    meses = (delta_tempo_servico.days % 365.25) / 30.44  # Usar 30.44 para considerar a média de dias por mês
    dias = (delta_tempo_servico.days % 365.25) % 30.44  # Usar 30.44 para considerar a média de dias por mês

    # Calcular a data futura de reserva remunerada
    data_reserva_remunerada = calcular_data_futura_reserva(data_ingresso, 30)

    # Criar uma contagem regressiva para a futura reserva
    hoje = datetime.now()
    tempo_restante = (data_reserva_remunerada - hoje)
    percent_tempo_restante = min(100, (tempo_restante.total_seconds() / (30 * 365 * 24 * 3600)) * 100)  # Limitar a 100%
    dias_restantes = int(tempo_restante.days)
    horas_restantes, resto_horas = divmod(tempo_restante.seconds, 3600)
    minutos_restantes, _ = divmod(resto_horas, 60)

    # Normalizar a porcentagem para um valor entre 0.0 e 1.0
    normalized_percent_tempo_restante = percent_tempo_restante / 100.0

    # Exibir contagem regressiva para a futura reserva
    st.markdown("Contagem regressiva para a reserva:")
    st.progress(normalized_percent_tempo_restante)
    st.text(f"**{dias_restantes} dias, {horas_restantes} horas, {minutos_restantes} minutos.**")

    return (
        "<p><strong>Nova regra da reserva remunerada</strong></p>"
        "<p>Os militares que ingressarem nas Forças Armadas a partir de 17/12/2019 (vigência da reforma) devem cumprir, "
        "no mínimo, 35 anos de tempo de serviço para entrar na reserva remunerada.</p>"
        "<p>No entanto, para que os 35 anos sejam válidos, é preciso cumprir um dos dois requisitos abaixo:</p>"
        "<ol>"
        "<li>30 anos de exercício de atividade de natureza militar nas Forças Armadas, para os oficiais formados nas "
        "seguintes instituições:"
        "   <ul>"
        "       <li>Academia Militar das Agulhas Negras</li>"
        "       <li>Academia da Força Aérea</li>"
        "       <li>Escola Naval</li>"
        "       <li>Instituto Militar de Engenharia</li>"
        "       <li>Instituto Tecnológico de Aeronáutica</li>"
        "       <li>Em escola ou centro de formação de oficiais.</li>"
        "   </ul>"
        "</li>"
        "<li>25 anos de atividade de natureza militar nas Forças Armadas, para militares que não se enquadram nas hipóteses acima.</li>"
        "</ol>"
        "<p>Ao contrário da nova regra de aposentadorias do trabalhador privado, não é preciso ter uma idade mínima para entrar na reserva remunerada.</p>"
        f"<p><strong>Tempo de serviço após a Lei:</strong> {anos:.2f} anos, {meses:.2f} meses, {dias:.2f} dias. "
        f"<strong>Data futura de reserva remunerada:</strong> {data_reserva_remunerada.strftime('%d/%m/%Y')}. "
        f"<strong>Contagem regressiva para a reserva:</strong> {dias_restantes} dias, {horas_restantes} horas, {minutos_restantes} minutos.</p>"
    )

def calcular_data_futura_reserva(data_ingresso, anos_futura_reserva):
    # Calcular anos, meses e dias
    anos = int(anos_futura_reserva)
    meses_faltantes = (anos_futura_reserva - anos) * 12
    meses = int(meses_faltantes)
    dias_faltantes = (meses_faltantes - meses) * 30.44  # Usar 30.44 para considerar a média de dias por mês
    dias = int(dias_faltantes)

    # Somar à data de ingresso
    data_reserva_remunerada = datetime.combine(data_ingresso, datetime.min.time()) + timedelta(days=anos * 365 + meses * 30.44 + dias)
    return data_reserva_remunerada

def main():
    st.title("Calculadora de Tempo de Serviço nas FFAA")

    # Adicionar explicação sobre as regras
    st.markdown(
        "Este aplicativo calcula o tempo de serviço nas Forças Armadas conforme as regras estabelecidas pela Lei 13.954/2019. "
        "Selecione a data de ingresso e clique no botão 'Calcular' para obter o resultado."
    )

    # Selecionar a data de ingresso
    data_ingresso = st.date_input("Selecione a data de ingresso nas FFAA:", min_value=date(1990, 1, 1))

    # Definir a data da Lei
    data_lei = date(2019, 12, 17)

    if st.button("Calcular"):
        # Calcular o tempo de serviço
        resultado = calcular_tempo_servico(data_ingresso, data_lei)

        # Exibir o resultado
        st.markdown(resultado, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
