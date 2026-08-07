# Arquivo gerado a partir do notebook Transporte_Crimes.ipynb
# Mantém a ordem das células de código para este tema.

# --- Célula 22 ---
rotas = pd.read_csv('routes.txt', sep=',')
passagem_valor = pd.read_csv('fare_attributes.txt', sep=',')
tempo_parada = pd.read_csv('stop_times.txt', sep=',')
viagens = pd.read_csv('trips.txt', sep=',')

# --- Célula 23 ---
viagens['trip_short_name'].unique()
