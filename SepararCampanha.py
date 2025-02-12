import pandas as pd
import os

def clean_phone_number(phone):
    if pd.isna(phone):
        return None
    # Remove +55 e caracteres não numéricos
    cleaned = str(phone).replace('+55', '').replace(' ', '')
    cleaned = ''.join(filter(str.isdigit, cleaned))
    return cleaned if cleaned else None

def main():
    # Criar/limpar diretório data
    if not os.path.exists('data'):
        os.makedirs('data')
    if 'data' in os.listdir():
        for file in os.listdir('data'):
            try:
                os.remove(f'data/{file}')
            except:
                pass

    # Ler o arquivo CSV
    df = pd.read_csv('campanha.csv', 
                     skiprows=[0], 
                     usecols=['Nome','Campanha','Email','Telefone'])

    # Tratar os telefones
    # Primeiro, dividir os telefones por ';'
    telefones_split = df['Telefone'].str.split(';', expand=True)
    
    # Limpar cada coluna de telefone
    for col in telefones_split.columns:
        telefones_split[col] = telefones_split[col].apply(clean_phone_number)
    
    # Garantir que a primeira coluna de telefone vá para 'Telefone'
    df['Telefone'] = telefones_split[0]
    
    # Renomear as outras colunas como Telefone1, Telefone2, etc.
    telefones_adicionais = telefones_split.iloc[:, 1:]
    telefones_adicionais.columns = [f'Telefone{i+1}' for i in range(len(telefones_adicionais.columns))]
    
    # Concatenar com o DataFrame original
    df = pd.concat([df, telefones_adicionais], axis=1)
    
    # Usar o primeiro telefone como ID
    df['ID'] = df['Telefone']
    
    # Mover a coluna ID para a primeira posição
    colunas = ['ID'] + [col for col in df.columns if col != 'ID']
    df = df[colunas]
    
    # Limpar nome da campanha
    df['Campanha'] = df['Campanha'].str.replace(r'[^\w\s]', '', regex=True)
    
    # Criar arquivos por campanha
    list_campaing = df['Campanha'].unique()
    for campaing in list_campaing:
        x = df[df['Campanha'] == campaing]
        x.to_csv(f'data/{campaing}.csv', sep='|', index=False)
    
    if 'nan.xlsx' in os.listdir('data'):
        os.remove('data/nan.xlsx')

if __name__ == '__main__':
    main()