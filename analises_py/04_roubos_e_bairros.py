# Arquivo gerado a partir do notebook Transporte_Crimes.ipynb
# Mantém a ordem das células de código para este tema.

# --- Célula 25 ---
#carregamento e limpeza inicial
df_roubos1 = pd.read_excel('evolucaomensalcapitalnomes.xlsx')
df_roubos1.head()

# --- Célula 26 ---
df_roubos1.shape

# --- Célula 27 ---
df_roubos1.describe()

# --- Célula 28 ---
df_roubos1.info()

# --- Célula 29 ---
# roubo_columns = [col for col in df_roubos1.columns if 'roubo' in col] # estou pegando todas as colunas que tem "roubo" no nome para selecionar no df_roubos2
# roubo_columns_filtered = [col for col in roubo_columns if 'total' not in col] # tirando a coluna que é total_roubo

# furto_columns = [col for col in df_roubos1.columns if 'furto' in col] # estou pegando todas as colunas que tem "furto" no nome para selecionar no df_roubos2
# furto_columns_filtered = [col for col in furto_columns if 'total' not in col] # tirando a coluna que é total_furto

# inicial_columns = df_roubos1.iloc[:,0:9].columns.tolist() # pegando as colunas iniciais para colocar no df_roubos2

# todas_colunas = inicial_columns + roubo_columns_filtered + furto_columns_filtered # todas as colunas juntas

# df_roubos2 = df_roubos1.loc[:, todas_colunas]
# nova tabela somente com as variaveis que vamos utilizar

# --- Célula 30 ---
df_roubos2 = df_roubos1.copy()

# --- Célula 31 ---
df_roubos2.info()

# --- Célula 32 ---
# df_roubos2 = df_roubos2.drop(['roubo_bicicleta','furto_bicicleta'], axis = 1) # dropamos a coluna de roubo e furto de bicicleta porque haviam muitos valores não nulos e não teria um impaccto muito grande

# --- Célula 33 ---
df_roubos2['cisp'].unique()

# --- Célula 34 ---
len(df_roubos2['cisp'].unique().tolist())

# --- Célula 35 ---
# Identifica as colunas a serem excluídas com base na solicitação do usuário (índices 0-8 e 64)
excluded_columns_by_position = df_roubos2.columns[0:9].tolist() + [df_roubos2.columns[63]] + [df_roubos2.columns[64]]

# Filtra as colunas numéricas relacionadas a crimes, excluindo explicitamente as colunas especificadas
crime_columns_for_sum = [
    col for col in df_roubos2.columns
    if col not in excluded_columns_by_position
]

df_roubos2['total crime'] = df_roubos2[crime_columns_for_sum].sum(axis=1) # Cria uma coluna com o número total de crimes relevantes

# --- Célula 36 ---
# total_columns_updated = [col for col in furto_columns_filtered if col in df_roubos2.columns] + [col for col in roubo_columns_filtered if col in df_roubos2.columns] # junta roubos e furtos em uma única coisa
# df_roubos2['total crime'] = df_roubos2[total_columns_updated].sum(axis=1) # cria uma coluna com o total de crimes relevantes

# --- Célula 37 ---
df_roubos2

# --- Célula 38 ---
total_bairro = df_roubos2.groupby('ano')['total crime'].sum().reset_index()
total_bairro = total_bairro.iloc[0:23,:]

# --- Célula 39 ---
fig = px.bar(total_bairro, x='ano',y='total crime')
fig.show()

# --- Célula 40 ---
fig = px.box(total_bairro, y='total crime')
fig.update_layout(width=800, height=500)
fig.show()

# --- Célula 43 ---
lista_bruta = df_roubos2['cisp'].dropna().unique().astype(str).tolist() # Lucas : Tava df2 mudei para o df_roubos2 pois estava dando erro

lista_final = []

for item in lista_bruta:
    # Transforma em minúsculo e remove aspas para evitar duplicatas sutis
    item = item.lower()

    # Remove "(parte)"
    item = re.sub(r'\(parte\)', '', item)

    # Separa o texto por vírgulas ou " e "
    partes = re.split(r'\s*,\s*|\s+e\s+', item)

    for p in partes:
        # Limpeza final de espaços
        bairro_limpo = p.strip()
        if bairro_limpo:
            lista_final.append(bairro_limpo)

# Contagem consolidada
contagem = dict(Counter(lista_final))

# Lista de nomes únicos
lista_bairros = list(contagem.keys())

print(f"Bairros: {lista_bairros}")
print(len(lista_bairros))
print(f"Contagem: {contagem}")

# --- Célula 45 ---
#agrupar o total de crimes por bairro
crimes_bairro = df_roubos2.groupby('cisp')['total crime'].sum().reset_index()
crimes_bairro.head()

# --- Célula 46 ---
#padronização
crimes_bairro['cisp'] = crimes_bairro['cisp'].str.lower()

# --- Célula 47 ---
crimes_bairro

# --- Célula 48 ---
df_roubos2
