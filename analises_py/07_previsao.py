# Arquivo gerado a partir do notebook Transporte_Crimes.ipynb
# Mantém a ordem das células de código para este tema.

# --- Célula 94 ---
# 7. Avaliação Final do Modelo
# ============================
# Calcula métricas de desempenho para avaliar a qualidade das previsões.

mae = mean_absolute_error(y_test, previsoes_finais) # Erro Médio Absoluto.
mape = mean_absolute_percentage_error(y_test, previsoes_finais) * 100 # Erro Percentual Médio Absoluto.
r2 = r2_score(y_test, previsoes_finais) # Coeficiente de Determinação (R²).

print(f"--- Resultado Final ---")
print(f"MAE: {mae:.2f} roubos") # Apresenta o MAE.
print(f"MAPE: {mape:.2f}%")   # Apresenta o MAPE.
print(f"R² Score: {r2:.4f} ({r2*100:.2f}%)") # Apresenta o R².

# ==========================================
# 8. VISUALIZAÇÃO DOS RESULTADOS
# ==========================================
# Gera gráficos para visualizar a importância das features, a comparação entre valores reais e previstos, e a dispersão.

fig, axes = plt.subplots(1, 3, figsize=(22, 6)) # Cria uma figura com 3 subplots.

# Gráfico 1: Importância das Var iáveis
# Mostra quais features foram mais relevantes para o modelo.
importancia = pd.Series(modelo.feature_importances_, index=features).sort_values() # Calcula e ordena a importância das features.
importancia.plot(kind='barh', ax=axes[0], color='skyblue') # Plota a importância como um gráfico de barras horizontais.
axes[0].set_title('Importância das Variáveis')

# Gráfico 2: Comparação Real vs Previsto (Amostra)
# Compara visualmente os primeiros 100 valores reais com os previstos.
axes[1].plot(y_test.values[:100], label='Real', color='black', alpha=0.6) # Valores reais.
axes[1].plot(previsoes_finais[:100], label='Previsto', color='red', linestyle='--') # Valores previstos.
axes[1].set_title('Amostra: Real vs Previsto')
axes[1].legend() # Adiciona a legenda.

# Gráfico 3: Dispersão: Real vs Previsto
# Avalia a relação geral entre os valores reais e previstos.
sns.scatterplot(ax=axes[2], x=y_test, y=previsoes_finais, alpha=0.3, color='darkblue') # Gráfico de dispersão.
# Adiciona uma linha diagonal (y=x) para representar a previsão perfeita.
axes[2].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
# Adiciona o texto do R² no gráfico de dispersão para uma visualização rápida da qualidade do ajuste.
axes[2].text(0.05, 0.95, f'R² = {r2:.2f}', transform=axes[2].transAxes, fontsize=12, fontweight='bold', color='red')
axes[2].set_title('Dispersão: Real vs Previsto')

plt.tight_layout() # Ajusta o layout para evitar sobreposição de elementos.
plt.show() # Exibe os gráficos.
