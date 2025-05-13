import pandas as pd

# Cargar el archivo original
demareal_df = pd.read_csv("demareal.csv")
demacome_df = pd.read_csv("demacome.csv")

# Crear archivo de agentes únicos con ID autoincremental
agentes_df = demareal_df[["Agente"]].drop_duplicates()
agentes_df = agentes_df.reset_index(drop=True)
agentes_df.insert(0, 'id', range(1, len(agentes_df) + 1))
agentes_df.to_csv("agentes.csv", index=False)
print("Archivo de agentes creado como 'agentes.csv'")

# Crear diccionario de mapeo de Agente a ID
agente_to_id = dict(zip(agentes_df['Agente'], agentes_df['id']))

# Definir columnas fijas y columnas de horas
fixed_columns = ["Date", "Agente", "code"]
hour_columns = [col for col in demareal_df.columns if col.startswith("Hour")]

demareal_long = demareal_df.melt(
    id_vars=fixed_columns,
    value_vars=hour_columns,
    var_name="Hour",
    value_name="Value"
)

demareal_long["Hour"] = demareal_long["Hour"].str.replace("Hour", "")
# Reemplazar Agente con su ID correspondiente
demareal_long["Agente"] = demareal_long["Agente"].map(agente_to_id)
# Reemplazar valores vacíos por 0
demareal_long["Value"] = demareal_long["Value"].fillna(0)

# Guardar el resultado CSV
demareal_long.to_csv("demareal_transformado.csv", index=False)

print("Transformación completada. Archivo guardado como 'demareal_transformado.csv'")
print("Transformado datos comerciales...")
# Definir columnas fijas y columnas de horas
fixed_columns = ["Date", "code"]
hour_columns = [col for col in demacome_df.columns if col.startswith("Hour")]

demacome_long = demacome_df.melt(
    id_vars=fixed_columns,
    value_vars=hour_columns,
    var_name="Hour",
    value_name="Value"
)

demacome_long["Hour"] = demacome_long["Hour"].str.replace("Hour", "")
# Reemplazar valores vacíos por 0
demacome_long["Value"] = demacome_long["Value"].fillna(0)

demacome_long.to_csv("demacome_transformado.csv", index=False)

print("Transformación completada. Archivo guardado como 'demacome_transformado.csv'")