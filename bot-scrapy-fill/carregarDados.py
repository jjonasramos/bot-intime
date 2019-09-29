import pandas as pd
from dateutil.relativedelta import *
import os
import Configs

def main():
    stop_colunas = ['Saldo', 'Pendências', 'Observações', 'Pendências resolvidas', 'Classificação Demanda', ':', 'Consultor', 'Demanda']

    link = Configs.get()['Chronos']

    servicos = pd.read_csv(link, usecols=lambda x: x not in stop_colunas and 'Unnamed' not in x)
    
    servicos['Data'] = pd.to_datetime(servicos['Data'])

    mes_atual = (pd.to_datetime('today').floor('D')).replace(day=1)
    mes_passado = ((pd.to_datetime('today').floor('D')).replace(day=1) - relativedelta(months=1))

    # Filtrar todos os serviços de mentoring do Mês anterior
    serv_filter = servicos[(servicos['Data'] >= mes_passado) & (servicos['Data'] < mes_atual) & (servicos['Tipo demanda'] == 'Mentoring')]

    # Criar coluna juntando Área com Tarefa
    serv_filter['Desc'] = serv_filter.apply(lambda row: row['Área demandante'] + ' - ' + row['Tarefa'], axis=1)

    # Dropando os campos desnecessários
    serv_filter = serv_filter.drop(['Área demandante',	'Tipo demanda', 'Tarefa'], axis=1)

    if not os.path.exists('data'):
        os.makedirs('data', 0o700)

    serv_filter.to_csv('data/servicos.csv', encoding="utf-8")

if __name__ == '__main__':
    main()