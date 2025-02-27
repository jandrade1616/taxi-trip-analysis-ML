#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Cargar los archivos CSV
path_01 = '/datasets/project_sql_result_01.csv'
path_04 = '/datasets/project_sql_result_04.csv'
path_07 = '/datasets/project_sql_result_07.csv'

# Leer los archivos CSV en DataFrames
df_sql_result_01 = pd.read_csv(path_01)
df_sql_result_04 = pd.read_csv(path_04)

# Mostrar las primeras filas de ambos DataFrames para estudiar su contenido
print(df_sql_result_01.head())
print(df_sql_result_04.head())

# Verificar los tipos de datos
print(df_sql_result_01.info())
print(df_sql_result_04.info())


# In[2]:


# Identificar los 10 principales barrios en términos de finalización
top_10_neighborhoods = df_sql_result_04.nlargest(10, 'average_trips')

# Hacer gráficos: empresas de taxis y número de viajes, y los 10 barrios principales por número de finalizaciones
import matplotlib.pyplot as plt

# Gráfico de los 10 barrios principales por número de finalizaciones
plt.figure(figsize=(12, 6))
top_10_neighborhoods.plot(kind='bar', x='dropoff_location_name', y='average_trips', legend=False)
plt.title('Top 10 barrios con mayor viajes finalizados (noviembre 2017)')
plt.ylabel('Promedio de viajes')
plt.xlabel('Barrios')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Segmentar los 10 competidores con mayores viajes 
top_10_companies = df_sql_result_01.sort_values(by='trips_amount', ascending=False).head(10)

# Crear el gráfico del top 10
plt.figure(figsize=(10, 6))
ax = top_10_companies.plot(
    kind='bar', 
    x='company_name', 
    y='trips_amount', 
    legend=False,
    ax=plt.gca()
)

plt.title('Top 10 compañías de taxis por número de viajes (15-16 noviembre 2017)')
plt.ylabel('Cantidad de viajes')
plt.xlabel('Compañía de taxis')

# Agregar los números de viajes encima de cada barra
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=8)

# Ajustar la rotación de las etiquetas en el eje x
plt.xticks(rotation=45, ha='right')

# Ajustar espaciado para evitar superposición
plt.tight_layout()
plt.show()


# In[3]:


import pandas as pd
from scipy import stats

# Cargar el archivo CSV
path_07 = '/datasets/project_sql_result_07.csv'
df_sql_result_07 = pd.read_csv(path_07)

# Filtro de datos
saturday_rainy = df_sql_result_07[df_sql_result_07['weather_conditions'] == 'Bad']['duration_seconds']
saturday_clear = df_sql_result_07[df_sql_result_07['weather_conditions'] == 'Good']['duration_seconds']

# Prueba de Levene para comparar las varianzas
levene_stat, levene_p_value = stats.levene(saturday_rainy, saturday_clear)

# Nivel de significación para la prueba de Levene
alpha = 0.05

# Mostrar el resultado de la prueba de Levene
print(f'Levene statistic: {levene_stat}')
print(f'P-value (Levene test): {levene_p_value}')

# Decidir si las varianzas son iguales
equal_var = True if levene_p_value > alpha else False

# La prueba t de Student para muestras independientes usando el resultado de la prueba de Levene
t_stat, p_value = stats.ttest_ind(saturday_rainy, saturday_clear, equal_var=equal_var)

# Mostrar resultados de la prueba t
print(f'T-statistic: {t_stat}')
print(f'P-value: {p_value}')

# Conclusión basada en la prueba t
if p_value < alpha:
    print("Rechazamos la hipótesis nula: La duración promedio de los viajes en sábados con lluvia SÍ ES diferente a la de los sábados sin lluvia.")
else:
    print("No se puede rechazar la hipótesis nula: No hay evidencia suficiente para afirmar que la duración promedio de los viajes es diferente en sábados lluviosos y no lluviosos.")

