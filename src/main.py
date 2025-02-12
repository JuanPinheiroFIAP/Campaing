import pandas as pd
import os

def main():
    df = pd.re('relatorio_deals_Comparecimento.xlsx', usecols=['name_negociação','campaing_name','contact_email','contact_phone'])
    df.rename(columns={
        'name_negociação': 'Nome',
        'campaing_name': 'Campanha',
        'contact_email': 'Email',
        'contact_phone': 'Telefone'
    }, inplace=True)
    #Fazendo a tratativa dos telefones
    df['Telefone'] = df['Telefone'].str.replace(r'\+55', '', regex=True)
    df['Telefone'] = df['Telefone'].str.replace(r'[^\d]', '', regex=True)
    df['ID'] = df['Telefone']

    df['Campanha'] = df['Campanha'].str.replace(r'[^\w\s]', '', regex=True)
    list_campaing = df['Campanha'].unique()

    if not os.path.exists('data'):
        os.makedirs('data')
    for campaing in list_campaing:
        x = df[df['Campanha'] == campaing]
        x.to_excel(f'data/{campaing}.xlsx', sep='|')
    
if __name__ == '__main__':
    main()
