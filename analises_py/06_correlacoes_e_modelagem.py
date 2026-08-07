# Arquivo gerado a partir do notebook Transporte_Crimes.ipynb
# Mantém a ordem das células de código para este tema.

# --- Célula 79 ---
# 1. Preparação dos dados de População (df_area)
df_area_clean = df_area[['NOME', 'Shape__Area']].copy()
df_area_clean['NOME'] = df_area_clean['NOME'].str.strip().str.lower()

# 2. Preparação de Paradas por Bairro
paradas_bairro = df_merged.explode('ID_Bairro').groupby('ID_Bairro')['stop_id'].nunique().reset_index()
paradas_bairro.columns = ['ID_Bairro', 'qtd_paradas']

# 3. Consolidação Final
# Removemos colunas duplicadas de df_final antes do merge para evitar sufixos _x e _y
if 'Shape__Area' in df_final.columns:
    df_final_clean = df_final.drop(columns=['Shape__Area'])
else:
    df_final_clean = df_final.copy()

df_master = pd.merge(df_final_clean, df_area_clean, left_on='ID_Bairro', right_on='NOME', how='inner')
df_master = pd.merge(df_master, paradas_bairro, on='ID_Bairro', how='left').fillna(0)

# Exibir correlações numéricas
display(df_master[['total crime', 'Shape__Area', 'qtd_linhas', 'qtd_paradas']].corr())

# Quantidade de linhas de onibus e quantidade de paradas são MUITO correlacionados!

# --- Célula 80 ---
# Visualizações de Correlação
fig, axes = plt.subplots(1, 3, figsize=(20, 5))

# Densidade da População X Crimes
sns.regplot(ax=axes[0], x='Shape__Area', y='total crime', data=df_master, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
axes[0].set_title('Área vs Crimes')

# Número de Paradas X Crimes
sns.regplot(ax=axes[1], x='qtd_paradas', y='total crime', data=df_master, scatter_kws={'alpha':0.5}, line_kws={'color':'green'})
axes[1].set_title('Qtd. Paradas vs Crimes')

# Quantidade de Linhas X Densidade Populacional
sns.regplot(ax=axes[2], x='Shape__Area', y='qtd_linhas', data=df_master, scatter_kws={'alpha':0.5}, line_kws={'color':'blue'})
axes[2].set_title('Área vs Qtd. Linhas')

plt.tight_layout()
plt.show()

# --- Célula 82 ---
# 1. Matriz de Correlação: Total Crime, Homens e Mulheres
corr_genero = df_final[['total crime', 'Homens', 'Mulheres']].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(corr_genero, annot=True, cmap='coolwarm', fmt='.3f')
plt.title('Correlação entre Crimes e População por Gênero')
plt.show()

# Achei que haveria uma melhor correlação entre os crimes e a quantidade de pessoas, todavia, foi baixa a correlação

# --- Célula 83 ---
# 2. Gráficos de Regressão: Relação entre Gênero e Crescimento de Crimes
# Garantindo que os dados sejam numéricos e removendo NaNs para evitar erros no regplot
df_plot = df_final[['Homens', 'Mulheres', 'total crime']].apply(pd.to_numeric, errors='coerce').dropna()

fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Homens vs Total Crime
sns.regplot(ax=axes[0], x='Homens', y='total crime', data=df_plot,
            scatter_kws={'alpha':0.5}, line_kws={'color':'blue'})
axes[0].set_title('População Masculina vs Total de Crimes')
axes[0].set_xlabel('Quantidade de Homens')
axes[0].set_ylabel('Total de Crimes')

# Mulheres vs Total Crime
sns.regplot(ax=axes[1], x='Mulheres', y='total crime', data=df_plot,
            scatter_kws={'alpha':0.5}, line_kws={'color':'pink'})
axes[1].set_title('População Feminina vs Total de Crimes')
axes[1].set_xlabel('Quantidade de Mulheres')
axes[1].set_ylabel('Total de Crimes')

plt.tight_layout()
plt.show()

# --- Célula 85 ---
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import poisson, norm

# Nova Correlação: Normalizando por Área
# Vamos ver se bairros menores mas com muitos crimes/paradas mostram padrões diferentes
df_master['crime_por_km2'] = df_master['total crime'] / df_master['Shape__Area']
df_master['paradas_por_km2'] = df_master['qtd_paradas'] / df_master['Shape__Area']

corr_geo = df_master[['crime_por_km2', 'paradas_por_km2', 'Densidade', 'qtd_linhas']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_geo, annot=True, cmap='YlGnBu')
plt.title('Correlação: Densidade de Infraestrutura vs Crimes')
plt.show()

# --- Célula 87 ---
# Cálculo do Lambda para Poisson
lam = df_master['qtd_linhas'].mean()
print(f"Lambda (média) das linhas de ônibus: {lam:.2f}")

# Visualização da Distribuição Teórica vs Real
x_plot = np.arange(0, df_master['qtd_linhas'].max() + 5)
plt.figure(figsize=(10, 5))
plt.hist(df_master['qtd_linhas'], bins=20, density=True, alpha=0.6, color='blue', label='Dados Reais')
plt.plot(x_plot, poisson.pmf(x_plot, lam), 'ro-', lw=2, label=f'Poisson (λ={lam:.2f})')
plt.title('Distribuição de Linhas de Ônibus (Real vs Poisson)')
plt.xlabel('Qtd Linhas')
plt.legend()
plt.show()

# também vi a parte de a quantidade de assaltos parecer uma variável aleatória contínua Normal

# --- Célula 89 ---
# Gráficos de Dispersão com Linha de Tendência (Regressão Linear)
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# População Total vs Total de Crimes
sns.regplot(ax=axes[0], x='Total populacao', y='total crime', data=df_master,
            scatter_kws={'alpha':0.4, 'color':'gray'}, line_kws={'color':'darkred', 'label':'Tendência'})
axes[0].set_title('Relação: População vs Crime Total')
axes[0].legend()

# Qtd de Paradas vs Total de Crimes
sns.regplot(ax=axes[1], x='qtd_paradas', y='total crime', data=df_master,
            scatter_kws={'alpha':0.4, 'color':'gray'}, line_kws={'color':'darkgreen', 'label':'Tendência'})
axes[1].set_title('Relação: Infraestrutura (Paradas) vs Crime Total')
axes[1].legend()

plt.tight_layout()
plt.show()

# --- Célula 90 ---
# Heatmap de Correlação Consolidado
# Selecionando apenas as colunas métricas para o heatmap final
metrias_final = df_master[['total crime', 'Total populacao', 'Shape__Area', 'Densidade', 'qtd_linhas', 'qtd_paradas', 'crime_por_km2', 'paradas_por_km2']]
corr_final = metrias_final.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_final, annot=True, cmap='RdYlGn', center=0, fmt='.2f')
plt.title('Mapa de Calor: Correlações Cruzadas de Segurança e Infraestrutura')
plt.show()

# --- Célula 91 ---
metrias_final = df_master[['crime_por_km2', 'paradas_por_km2']]
corr_final = metrias_final.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_final, annot=True, cmap='RdYlGn', center=0, fmt='.2f')
plt.title('Mapa de Calor: Correlações Cruzadas de Segurança e Infraestrutura')
plt.show()

# --- Célula 92 ---
# Modelo XGBoost Regressor para Previsão de Roubos

from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score

# 1. Carregamento e Limpeza Inicial dos Dados
# ==========================================
# Carrega o DataFrame original de roubos e prepara a coluna alvo.

df_ML = df_roubos1.copy() # Cria uma cópia do DataFrame original para evitar modificar os dados brutos.

# Garante que a coluna alvo 'roubos' exista somando todas as categorias de roubo.
# Filtra colunas que contêm 'roubo' no nome (case-insensitive) e que não são 'total_roubos'.
colunas_roubo = [col for col in df_ML.columns if 'roubo' in col.lower() and 'total' not in col.lower()]
df_ML['roubos'] = df_ML[colunas_roubo].sum(axis=1) # Soma as contagens de todas as subcategorias de roubo para criar a variável alvo.

# Remove a coluna 'Unnamed: 0' se existir, que geralmente é um índice gerado automaticamente ao salvar/carregar CSVs/Excel.
if 'Unnamed: 0' in df_ML.columns:
    df_ML = df_ML.drop(columns=['Unnamed: 0'])

# 2. Codificação da Variável Categórica 'CISP'
# ==========================================
# Transforma a identificação textual do CISP em um formato numérico para o modelo.

df_ML['cisp'] = df_ML['cisp'].astype(str) # Garante que a coluna 'cisp' seja tratada como string.
le = LabelEncoder() # Inicializa o LabelEncoder.
df_ML['cisp_codificado'] = le.fit_transform(df_ML['cisp']) # Codifica cada identificador CISP único com um número inteiro.

# ==========================================
# 3. FEATURE ENGINEERING: Criação de Lags e Média Móvel
# ==========================================
# Gera variáveis temporais que capturam o histórico de roubos para cada CISP,
# essenciais para modelos de séries temporais.

# Passo A: Ordena o DataFrame para garantir o cálculo correto dos lags.
# A ordenação por CISP, ano e mês é crucial para que as operações 'shift' e 'rolling'
# funcionem corretamente dentro de cada grupo (CISP) e na sequência temporal.
df_ML = df_ML.sort_values(by=['cisp', 'ano', 'mes'])

# Passo B: Cria as features de lag e média móvel.
# 'lag_1': Roubos do mês anterior. Representa a inércia imediata.
df_ML['lag_1'] = df_ML.groupby('cisp')['roubos'].shift(1)
# 'lag_12': Roubos do mesmo mês no ano anterior. Captura a sazonalidade anual.
df_ML['lag_12'] = df_ML.groupby('cisp')['roubos'].shift(12)

# 'media_3m': Média móvel dos roubos dos últimos 3 meses (excluindo o mês atual).
# O '.shift(1)' é importante para evitar "data leakage", pois garante que a média
# não inclua a informação do mês que estamos tentando prever.
df_ML['media_3m'] = df_ML.groupby('cisp')['roubos'].transform(lambda x: x.rolling(window=3).mean().shift(1))

# Passo C: Limpeza de nulos e zeros após a criação de features.
# Remove linhas que não possuem dados históricos completos para os lags/médias móveis.
# Isso é comum, pois os primeiros meses (e anos para lag_12) não terão valores de lag.
df_ML = df_ML.dropna(subset=['lag_1', 'media_3m', 'lag_12'])
# Remove linhas onde a contagem de roubos é zero. Isso pode ser uma decisão de modelagem
# para focar apenas em períodos com ocorrências de roubo, ou pode ser ajustado
# dependendo da meta de previsão (prever 0s também).
df_ML = df_ML[df_ML['roubos'] > 0]

# ==========================================
# 4. PREPARAÇÃO PARA O TREINAMENTO DO MODELO
# ==========================================
# Define as variáveis preditoras (features) e a variável alvo (y), e divide os dados em conjuntos de treino e teste.

# Ordena cronologicamente novamente antes da divisão para garantir uma divisão temporal correta.
# Isso é crucial para simular um cenário de previsão real, onde o modelo é treinado em dados
# passados e avaliado em dados futuros.
df_ML = df_ML.sort_values(by=['ano', 'mes'])

# Atualiza a lista de colunas preditoras a serem usadas no modelo.
features = ['cisp_codificado', 'mes', 'ano', 'lag_1', 'media_3m', 'lag_12']
X = df_ML[features] # Variáveis independentes (preditoras).
y = df_ML['roubos'] # Variável dependente (alvo).

# Divisão Temporal (80% treino, 20% teste).
# `shuffle=False` é essencial para dados de séries temporais, mantendo a ordem cronológica.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# ==========================================
# 5. TRANSFORMAÇÃO LOGARÍTMICA E TREINO DO MODELO
# ==========================================
# Aplica uma transformação logarítmica à variável alvo e treina o modelo XGBoost.

# Aplica a transformação logarítmica (log1p = log(1+x)) à variável alvo do conjunto de treino.
# Isso ajuda a estabilizar a variância e tornar a distribuição mais normal, o que é benéfico
# para muitos modelos de regressão, especialmente com dados de contagem que são frequentemente assimétricos.
y_train_log = np.log1p(y_train)

# Configura e inicializa o modelo XGBoost Regressor.
# n_estimators: número de árvores.
# learning_rate: taxa de aprendizado, controla o tamanho do passo em cada iteração.
# max_depth: profundidade máxima de cada árvore, controla a complexidade do modelo.
# random_state: para reprodutibilidade dos resultados.
modelo = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)
modelo.fit(X_train, y_train_log) # Treina o modelo com os dados de treino transformados.

# ==========================================
# 6. PREVISÃO E REVERSÃO DA ESCALA ORIGINAL
# ==========================================
# Realiza previsões no conjunto de teste e reverte a transformação logarítmica.

previsoes_log = modelo.predict(X_test) # Realiza previsões no conjunto de teste (ainda na escala logarítmica).
# Reverte a transformação logarítmica para obter as previsões na escala original (expm1 = exp(x)-1).
previsoes_finais = np.expm1(previsoes_log)
