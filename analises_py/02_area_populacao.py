# Arquivo gerado a partir do notebook Transporte_Crimes.ipynb
# Mantém a ordem das células de código para este tema.

# --- Célula 3 ---
# Requisição à API do ArcGIS
import requests

url = "https://services1.arcgis.com/OlP4dGNtIcnD3RYf/arcgis/rest/services/Atlas_Densidade_Demografica/FeatureServer/0/query"

params = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "false",
    "f": "json"
}

r = requests.get(url, params=params)
data = r.json()

df_area = pd.DataFrame([f["attributes"] for f in data["features"]])

# --- Célula 4 ---
df_area

# --- Célula 5 ---
# le = LabelEncoder()

# df_area["REGIAO_ADM"] = le.fit_transform(df_area["REGIAO_ADM"])

# --- Célula 6 ---
df_area['Shape__Area'] = df_area['Shape__Area'] / 1000000 # precisamos dividir essa coluna por 1.000.000 para acharmos o valor em km²

# --- Célula 7 ---
df_area.sort_values(by='Shape__Area', ascending=False) # Organiza df_area em ordem decrescente

# --- Célula 8 ---
# padronização
df_area['NOME'] = df_area['NOME'].str.lower()
df_area['NOME'] = df_area['NOME'].str.strip()
df_area

# --- Célula 9 ---
zonas = pd.read_csv('zonas_bairro.txt', sep=',')

# --- Célula 10 ---
# padronização
zonas['Bairro'] = zonas['Bairro'].str.lower()
zonas['Bairro'] = zonas['Bairro'].str.strip()
zonas

# --- Célula 12 ---
df_pop = pd.read_excel('PopulacaoBairros2010.xlsx')

# --- Célula 13 ---
df_pop

# --- Célula 14 ---
df_pop = df_pop[df_pop['Unnamed: 1'] == 'Total']

# --- Célula 15 ---
df_pop.drop('Unnamed: 1', axis=1, inplace=True)

# --- Célula 16 ---
df_pop

# --- Célula 17 ---
df_pop.rename(
    columns={
        'Unnamed: 2': 'Total populacao',
        'Unnamed: 3': 'Homens',
        'Unnamed: 4': 'Mulheres',
        'Tabela 202 - População residente, por sexo e situação do domicílio': 'Bairro'}, inplace=True)

# --- Célula 18 ---
df_pop['Bairro'] = df_pop['Bairro'].str.extract(r'([^-]*)')[0].str.lower()
df_pop['Bairro'] = df_pop['Bairro'].str.strip()
df_pop

# --- Célula 20 ---
df_area_pop = pd.merge(left=df_area, right=df_pop, left_on='NOME', right_on='Bairro')
df_area_pop = pd.merge(left=df_area_pop, right=zonas, left_on='NOME', right_on='Bairro')
df_area_pop['Densidade'] = df_area_pop['Total populacao'] / df_area_pop['Shape__Area']
df_area_pop
