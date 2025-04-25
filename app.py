import streamlit as st
import requests

key = '9e2e7bc81035194bd942ac63'
url = 'https://v6.exchangerate-api.com/v6/{key}/latest/USD'
history = []

def calculate_value(amount, firstCoin, secondCoin, rates):
    try:
        taxa_origem = rates[firstCoin]
        taxa_destino = rates[secondCoin]
        
        converted_value = amount * (taxa_destino / taxa_origem)
        
        history.append((amount, firstCoin, round(converted_value, 2), secondCoin))
        return round(converted_value, 2)

    except KeyError:
        print('Moeda não encontrada. Verifique se digitou corretamente.')
        return None

st.set_page_config(page_title='Conversor de Moedas', page_icon='💰', layout='wide')

st.title('Conversor de Moedas')

resp = requests.get(url.format(key=key))
if resp.status_code == 200:
    dados = resp.json()
    dicionavrio = dados['conversion_rates']
    moedas_mundo = list(dicionario.keys())

    moeda_original = st.selectbox('Digite uma moeda para conversão (ex: BRL): ', moedas_mundo, index=0)
    moeda_objetivo = st.selectbox('Digite uma segunda moeda para conversão (ex: USD): ', moedas_mundo, index=1)

    valor = st.number_input(f'Digite o valor em {moeda_original} que deseja converter: ', min_value=0.0, format="%.2f")

    if st.button('Converter'):
        if moeda_original == moeda_objetivo:
            st.warning('As moedas são iguais. Escolha moedas diferentes para uma conversão bem sucedida.')
        elif valor == 0:
            st.warning('O valor deve ser maior que zero.')
        else:
            valor_convertido = calculate_value(valor, moeda_original, moeda_objetivo, dicionario)
            
            if valor_convertido is not None:
                st.success(f'{valor:.2f} {moeda_original} é igual a {valor_convertido:.2f} {moeda_objetivo}')
            else:
                st.error('Erro ao converter o valor. Verifique se digitou corretamente.')

    if st.button('Histórico de conversões'):
        if history:
            for registro in history:
                st.write(f'{registro[0]:.2f} {registro[1]} → {registro[2]:.2f} {registro[3]}')
        else:
            st.info('Nenhuma conversão realizada ainda.')


else:
    st.error(f'Error - Code: {resp.status_code}')