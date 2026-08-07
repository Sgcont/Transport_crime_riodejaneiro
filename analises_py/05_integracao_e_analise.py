# Arquivo gerado a partir do notebook Transporte_Crimes.ipynb
# Mantém a ordem das células de código para este tema.

# --- Célula 50 ---
# 1. Extração de bairros do nome da rota

df2_unique_neighborhoods_set = set(lista_bairros)

def find_route_neighborhoods(route_long_name, df2_nh_set):
    if not isinstance(route_long_name, str):
        return []
    route_name_lower = route_long_name.lower()
    found_nhs = []
    for nh in df2_nh_set:
# match por palavra inteira para evitar falso positivo (ex: "lapa" em "lapatã")
        if re.search(r'\b' + re.escape(nh) + r'\b', route_name_lower):
            found_nhs.append(nh)
    return list(set(found_nhs))

# Procura os bairros no nome da rota
rotas['ID_Bairro'] = rotas['route_long_name'].apply(
    lambda x: find_route_neighborhoods(x, df2_unique_neighborhoods_set)
)

# Separar origem e destino textuais
rotas[['origem', 'destino']] = rotas['route_long_name'].str.split(' - ', n=1, expand=True)
rotas['origem'] = rotas['origem'].str.strip().str.lower()
rotas['destino'] = rotas['destino'].str.strip().str.lower()

display(rotas[['route_long_name', 'origem', 'destino', 'ID_Bairro']].head(10))

# --- Célula 51 ---
#2. Merge em viagens + rotas + paradas

df_merged = pd.merge(viagens, rotas, on='route_id')
df_merged = pd.merge(df_merged, tempo_parada, on='trip_id')

# Explode: cada bairro vira uma linha
df_exploded = df_merged.explode('ID_Bairro').dropna(subset=['ID_Bairro'])
df_exploded['ID_Bairro'] = df_exploded['ID_Bairro'].str.strip().str.lower()

# Linhas ónibus ónibus por bairro
linhas_bairro = (
    df_exploded
    .groupby('ID_Bairro')['route_id']
    .nunique()
    .reset_index()
    .rename(columns={'route_id': 'qtd_linhas'})
)

print(f"Bairros encontrados nas rotas: {linhas_bairro.shape[0]}")
display(linhas_bairro.head(10))

# --- Célula 52 ---
# 3. Criar 'total crime' e normalizar

# Colunas de crime
crime_cols = [c for c in df_roubos2.columns if 'roubo' in c or 'furto' in c]

df_roubos2['total crime'] = df_roubos2[crime_cols].sum(axis=1)

# Criando um DataFrame intermediário para expandir 'cisp' em bairros individuais
exploded_cisp_crimes = []
for index, row in df_roubos2.iterrows():
    cisp_entry = str(row['cisp'])
    crime_sum = row['total crime']

    # Dividindo a string cisp, semelhante a extrair_lista, manipulando 'e' como separador
    parts = re.split(r',|\se\s', cisp_entry)

    for part in parts:
        bairro = part.strip().lower()
        if bairro:
            exploded_cisp_crimes.append({'bairro_norm': bairro, 'total crime_per_cisp_group': crime_sum})

# Convertendo para df
crimes_expanded_df = pd.DataFrame(exploded_cisp_crimes)

# Agora, agrupando por vizinhança normalizada individual e some os crimes associados,
# Esta ferramenta agrega crimes de bairros que aparecem em vários grupos 'cisp'
crimes_bairro = crimes_expanded_df.groupby('bairro_norm')['total crime_per_cisp_group'].sum().reset_index()
crimes_bairro.rename(columns={'total crime_per_cisp_group': 'total crime'}, inplace=True)

print(f"\nBairros no dataset de crimes: {crimes_bairro.shape[0]}")
print("Exemplos:", crimes_bairro['bairro_norm'].unique()[:10])

# --- Célula 53 ---
# 4. Diagnóstico do merge

bairros_rotas  = set(linhas_bairro['ID_Bairro'])
bairros_crimes = set(crimes_bairro['bairro_norm'])

intersecao = bairros_rotas & bairros_crimes
print(f"\nBairros em comum (casam no merge): {len(intersecao)}")
print(f"Só nas rotas:  {len(bairros_rotas - bairros_crimes)}")
print(f"Só nos crimes: {len(bairros_crimes - bairros_rotas)}")
print("\nExemplos que casam:", list(intersecao)[:10])

# --- Célula 54 ---
# 5. Merge final e gráficos

df_final = pd.merge(
    linhas_bairro,
    crimes_bairro,
    left_on='ID_Bairro',
    right_on='bairro_norm',
    how='inner'
)

print(f"\nLinhas no df_final: {df_final.shape[0]}")
display(df_final.head())

# Gráfico 1: Top 10 bairros com mais crimes
top_crimes = df_final.sort_values('total crime', ascending=False).head(10)

fig, axes = plt.subplots(1, 2, figsize=(16, 5))

sns.barplot(ax=axes[0], x='total crime', y='ID_Bairro', data=top_crimes, palette='Reds_r')
axes[0].set_title('Top 10 bairros com mais crimes')
axes[0].set_xlabel('total crimes')
axes[0].set_ylabel('Bairro')

# Gráfico 2: Quantidade de linhas nesses mesmos bairros
sns.barplot(ax=axes[1], x='qtd_linhas', y='ID_Bairro', data=top_crimes, palette='Blues_r')
axes[1].set_title('Linhas de ónibus nos bairros mais violentos')
axes[1].set_xlabel('Qtd. linhas de ónibus')
axes[1].set_ylabel('')

plt.tight_layout()
plt.show()

# --- Célula 56 ---
print(df_final.columns)

# --- Célula 57 ---
df_final

# --- Célula 58 ---
print(df_pop.columns)

# --- Célula 59 ---
df_area_pop['bairro_norm'] = df_area_pop['Bairro_x'].str.strip().str.lower()
df_final['bairro_norm'] = df_final['ID_Bairro'].str.strip().str.lower()

# --- Célula 60 ---
df_final = pd.merge(
    df_final,
    df_area_pop,
    on='bairro_norm',
    how='left'
)

# --- Célula 61 ---
set(df_final['bairro_norm']) - set(df_area_pop['bairro_norm'])

# --- Célula 62 ---
print(df_final.columns)
display(df_final.head())

# --- Célula 63 ---
df_final

# --- Célula 64 ---
df_final['crime_per_capita'] = df_final['total crime'] / df_area_pop['Total populacao']

# --- Célula 65 ---
corr = df_final[['qtd_linhas', 'total crime', 'Densidade', 'crime_per_capita', 'Total populacao', 'Shape__Area']].corr()
corr

# --- Célula 66 ---
fig = px.scatter(df_final,x='Densidade',y='total crime',color='Zona')
fig.update_traces(marker=dict(size=12))
fig.update_layout(width=800, height=500)
fig.show()

# Observação de Lucas : Gráfico ficou perfeito! E demonstra de forma lindissima o total de crimes para cada bairro com sua respectiva densidade

# --- Célula 67 ---
df_Densidade_Crimes = df_final[['Total populacao','total crime']]
corrDC = df_Densidade_Crimes.corr()
corrDC

# correlação igual a 0,326 quer dizer ser pequena

# --- Célula 68 ---
plt.figure(figsize=(8,6))
sns.heatmap(corrDC, annot=True)

plt.title('Matriz de Correlação')
plt.show()

# Baixa correlação entre essas duas variáveis

# --- Célula 69 ---
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True)

plt.title('Matriz de Correlação')
plt.show()

# Total de população e quantidade de linhas estão bem correlacionados

# --- Célula 70 ---
df_final.columns

# --- Célula 71 ---
# Scatter da quantidade de linhas sobre os crimes totais
plt.scatter(x='qtd_linhas', y='total crime', data = df_final)
plt.xlabel('Quantidade de Linhas')
plt.ylabel('Total de Crimes')
plt.title('Relação entre Quantidade de Linhas e Crimes')
plt.show()

# --- Célula 72 ---
# Novo df para abrigar apenas essas colunas
df_final_valores = df_final[['qtd_linhas', 'total crime']]

# --- Célula 73 ---
# Vendo ordem decrescente na qtd_linhas
df_final_valores.sort_values('qtd_linhas', ascending=False)

# --- Célula 74 ---
# Calculando a correlação :
correlacao = df_final_valores.corr()

# --- Célula 75 ---
# Histograma da quantidade de linhas de ônibus
hist = px.histogram(df_final['qtd_linhas'], nbins=20, height=800)
hist.show()

# --- Célula 76 ---
# Histograma do total de crimes
hist = px.histogram(df_final['total crime'], nbins=20, height=800)
hist.show()

# --- Célula 77 ---
# Vendo o valor da correlação (usando heatmap) :
sns.heatmap(correlacao, annot=True)
# Vemos que a correlação entre total de crimes e linhas é fraco (achamos com outros metodos entre 0,25 e 0,33)
