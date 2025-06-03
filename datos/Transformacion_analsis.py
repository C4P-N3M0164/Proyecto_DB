import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos desde el contenido CSV
csv_data = """
Date,Agente,code,Hour,Value
2024-04-27,1,ITLC,01,13789.59
2024-04-28,1,ITLC,01,10415.44
2024-04-29,1,ITLC,01,10133.05
2024-04-30,1,ITLC,01,14889.27
2024-04-27,2,CHCC,01,87466.92
2024-04-28,2,CHCC,01,91764.13
2024-04-29,2,CHCC,01,83626.48
2024-04-30,2,CHCC,01,86101.04
2024-04-27,3,TMVG,01,294.49
2024-04-28,3,TMVG,01,292.89
2024-04-29,3,TMVG,01,1076.26
2024-04-30,3,TMVG,01,1393.5
2024-04-27,4,RENG,01,0.0
2024-04-28,4,RENG,01,0.0
2024-04-29,4,RENG,01,0.0
2024-04-30,4,RENG,01,0.0
"""  # Se ha truncado el CSV para ejemplo

from io import StringIO

# Leer los datos
df = pd.read_csv(StringIO(csv_data))

# Convertir la columna de fecha a tipo datetime
df['Date'] = pd.to_datetime(df['Date'])

# Calcular el promedio de valores por Agente
promedios = df.groupby(['Agente', 'code'])['Value'].mean().reset_index()

# Ordenar de mayor a menor para obtener los 5 agentes con mayor promedio
top_agentes = promedios.sort_values(by='Value', ascending=False).head(5)

# Graficar
plt.figure(figsize=(10, 6))
plt.bar(top_agentes['code'], top_agentes['Value'], color='skyblue')
plt.title('Top 5 Agentes con Mayor Promedio de Valor')
plt.xlabel('Código del Agente')
plt.ylabel('Promedio de Valor')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar la gráfica
plt.show()
