import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos transformados
demareal = pd.read_csv("demareal_transformado.csv")
demacome = pd.read_csv("demacome_transformado.csv")
agentes = pd.read_csv("agentes.csv")

# Convertir la columna Date a datetime
demareal['Date'] = pd.to_datetime(demareal['Date'])
demacome['Date'] = pd.to_datetime(demacome['Date'])

def graficar_patrones_horarios(patrones_hora):
    plt.figure(figsize=(15, 8))
    
    # Gráfico de línea para la demanda promedio
    plt.subplot(2, 1, 1)
    sns.lineplot(data=patrones_hora, x='Hour', y='mean', marker='o')
    plt.title('Demanda Promedio por Hora')
    plt.xlabel('Hora')
    plt.ylabel('Demanda Promedio')
    plt.grid(True)
    
    # Gráfico de barras para la desviación estándar
    plt.subplot(2, 1, 2)
    sns.barplot(data=patrones_hora, x='Hour', y='std')
    plt.title('Variabilidad de la Demanda por Hora')
    plt.xlabel('Hora')
    plt.ylabel('Desviación Estándar')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('patrones_horarios_detallado.png')
    plt.close()

def graficar_agentes(oportunidades):
    plt.figure(figsize=(15, 10))
    
    # Top 10 agentes con mayor potencial de mejora
    top_10 = oportunidades.head(10)
    
    # Gráfico de barras horizontales
    plt.subplot(2, 1, 1)
    sns.barplot(data=top_10, y='id', x='potencial_mejora')
    plt.title('Top 10 Agentes con Mayor Potencial de Mejora')
    plt.xlabel('Potencial de Mejora')
    plt.ylabel('ID del Agente')
    
    # Gráfico de dispersión
    plt.subplot(2, 1, 2)
    sns.scatterplot(data=oportunidades, x='mean', y='potencial_mejora')
    plt.title('Relación entre Demanda Promedio y Potencial de Mejora')
    plt.xlabel('Demanda Promedio')
    plt.ylabel('Potencial de Mejora')
    
    plt.tight_layout()
    plt.savefig('analisis_agentes.png')
    plt.close()

def graficar_comparacion_demandas(comparacion):
    plt.figure(figsize=(15, 10))
    
    # Gráfico de línea para demanda real vs comercial
    plt.subplot(2, 1, 1)
    comparacion_diaria = comparacion.groupby('Date')[['Value_real', 'Value_comercial']].mean().reset_index()
    plt.plot(comparacion_diaria['Date'], comparacion_diaria['Value_real'], label='Demanda Real')
    plt.plot(comparacion_diaria['Date'], comparacion_diaria['Value_comercial'], label='Demanda Comercial')
    plt.title('Comparación de Demanda Real vs Comercial')
    plt.xlabel('Fecha')
    plt.ylabel('Demanda')
    plt.legend()
    plt.grid(True)
    
    # Gráfico de barras para el porcentaje de diferencia
    plt.subplot(2, 1, 2)
    sns.boxplot(data=comparacion, x='Hour', y='porcentaje_diferencia')
    plt.title('Distribución de Diferencias por Hora')
    plt.xlabel('Hora')
    plt.ylabel('Porcentaje de Diferencia')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('comparacion_demandas.png')
    plt.close()

# Análisis de demanda por hora
def analizar_patrones_horarios():
    # Agrupar por hora y calcular estadísticas
    patrones_hora = demareal.groupby('Hour')['Value'].agg(['mean', 'std', 'max']).reset_index()
    
    # Generar gráficos
    graficar_patrones_horarios(patrones_hora)
    
    return patrones_hora

# Análisis de demanda por agente
def analizar_agentes():
    # Agrupar por agente y calcular estadísticas
    patrones_agente = demareal.groupby('Agente')['Value'].agg(['mean', 'std', 'max']).reset_index()
    patrones_agente = patrones_agente.merge(agentes, left_on='Agente', right_on='id')
    
    # Identificar agentes con mayor potencial de mejora
    patrones_agente['coeficiente_variacion'] = patrones_agente['std'] / patrones_agente['mean']
    patrones_agente['potencial_mejora'] = patrones_agente['max'] - patrones_agente['mean']
    
    # Generar gráficos
    graficar_agentes(patrones_agente)
    
    return patrones_agente

# Análisis de demanda comercial vs real
def analizar_diferencias_comercial_real():
    # Agrupar datos por fecha y hora
    demanda_real = demareal.groupby(['Date', 'Hour'])['Value'].sum().reset_index()
    demanda_comercial = demacome.groupby(['Date', 'Hour'])['Value'].sum().reset_index()
    
    # Unir los datos
    comparacion = demanda_real.merge(demanda_comercial, on=['Date', 'Hour'], suffixes=('_real', '_comercial'))
    
    # Calcular diferencias y oportunidades
    comparacion['diferencia'] = comparacion['Value_real'] - comparacion['Value_comercial']
    comparacion['porcentaje_diferencia'] = (comparacion['diferencia'] / comparacion['Value_comercial']) * 100
    
    # Generar gráficos
    graficar_comparacion_demandas(comparacion)
    
    return comparacion

# Función principal de análisis
def analizar_rentabilidad():
    print("Iniciando análisis de rentabilidad...")
    
    # Realizar análisis
    patrones_horarios = analizar_patrones_horarios()
    patrones_agentes = analizar_agentes()
    comparacion_demandas = analizar_diferencias_comercial_real()
    
    # Identificar oportunidades de mejora
    oportunidades = patrones_agentes[patrones_agentes['potencial_mejora'] > 0].sort_values('potencial_mejora', ascending=False)
    
    # Generar reporte
    print("\n=== OPORTUNIDADES DE MEJORA ===")
    print("\nTop 5 agentes con mayor potencial de mejora:")
    print(oportunidades[['id', 'potencial_mejora']].head())
    
    print("\nHoras con mayor demanda promedio:")
    print(patrones_horarios.sort_values('mean', ascending=False).head())
    
    print("\nDiferencia promedio entre demanda real y comercial:")
    print(f"{comparacion_demandas['porcentaje_diferencia'].mean():.2f}%")
    
    # Guardar resultados
    oportunidades.to_csv('oportunidades_mejora.csv', index=False)
    comparacion_demandas.to_csv('comparacion_demandas.csv', index=False)
    
    print("\nSe han generado los siguientes archivos de visualización:")
    print("- patrones_horarios_detallado.png")
    print("- analisis_agentes.png")
    print("- comparacion_demandas.png")

if __name__ == "__main__":
    analizar_rentabilidad() 