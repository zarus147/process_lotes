from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, PULP_CBC_CMD
import numpy as np
import pandas as pd


def optimizar_lotes(df_selected, peso_minimo, peso_maximo, auRec_min, auRec_max):
    """
    Función para optimizar la selección de lotes según restricciones de peso y promedio de auRec.

    Parámetros:
        df_selected (pd.DataFrame): DataFrame con los datos de los lotes.
        peso_minimo (float): Peso mínimo permitido.
        peso_maximo (float): Peso máximo permitido.
        auRec_min (float): Valor mínimo permitido para el promedio de auRec.
        auRec_max (float): Valor máximo permitido para el promedio de auRec.

    Retorna:
        dict: Un diccionario con los resultados de la optimización.
    """
    # 🛠️ Limpiar el DataFrame (eliminar valores no válidos)
    df_selected = df_selected.replace([np.inf, -np.inf], np.nan)
    df_selected = df_selected.dropna(subset=['tmsBase', 'auRec'])

    print('Cantidad de lotes después de limpiar datos:')
    print(len(df_selected))
    print('__________________________________________________')

    # 🚀 Crear el problema de optimización
    problema = LpProblem("Optimización_Lotes_Peso_auRec", LpMaximize)

    # ✅ Variables binarias (1 si el lote se usa, 0 si no)
    variables = {i: LpVariable(f"Lote_{df_selected.iloc[i]['id']}", cat="Binary") for i in range(len(df_selected))}

    # ✅ Restricción de peso total (debe estar entre peso_minimo y peso_maximo)
    peso_total = lpSum(variables[i] * df_selected.iloc[i]['tmsBase'] for i in range(len(df_selected)))
    problema += peso_total <= peso_maximo, "Restricción de peso máximo"
    problema += peso_total >= peso_minimo, "Restricción de peso mínimo"

    # ✅ Objetivo: Maximizar la cantidad de lotes seleccionados dentro del rango de peso
    total_lotes = lpSum(variables[i] for i in range(len(df_selected)))
    problema += total_lotes, "Maximizar cantidad de lotes"

    # 🏆 Resolver el problema usando el solver CBC
    problema.solve(PULP_CBC_CMD(msg=False))

    # 📌 Mostrar la mejor combinación de lotes seleccionados
    print("Lotes seleccionados:")
    peso_total_solucion = 0
    auRec_total_solucion = 0
    lotes_seleccionados = 0  # Contador de lotes seleccionados
    lotes_seleccionados_array = []

    for i in range(len(df_selected)):
        if value(variables[i]) == 1:
            lote = df_selected.iloc[i]
            nuevo_peso_total = peso_total_solucion + lote['tmsBase']
            nuevo_auRec_total = auRec_total_solucion + lote['auRec']
            nuevo_promedio_auRec = nuevo_auRec_total / (lotes_seleccionados + 1)

            # 🚨 Verificar que el peso y el auRec promedio estén dentro de los límites
            if nuevo_peso_total > peso_maximo or not (auRec_min <= nuevo_promedio_auRec <= auRec_max):
                continue  # No incluir este lote si se pasa el peso o el promedio de auRec está fuera del rango

            # ✅ Si el lote cumple con las condiciones, se agrega al grupo
            peso_total_solucion = nuevo_peso_total
            auRec_total_solucion = nuevo_auRec_total
            lotes_seleccionados += 1
            lotes_seleccionados_array.append(lote['id'])

    # 📊 Mostrar resultados finales
    if lotes_seleccionados > 0:
        promedio_auRec_final = auRec_total_solucion / lotes_seleccionados
        print(f"\n✅ Peso total: {peso_total_solucion:.3f} (Debe estar entre {peso_minimo} y {peso_maximo})")
        print(f"✅ Promedio de auRec: {promedio_auRec_final:.5f} (Debe estar entre {auRec_min} y {auRec_max})")
        lotes_seleccionados_array = [int(lote_id) for lote_id in lotes_seleccionados_array]
        print(f"\n✅ Cantidad de lotes seleccionados: {lotes_seleccionados}")
        print(f"✅ IDs de los lotes seleccionados: {lotes_seleccionados_array}")

        # Retornar los resultados como un diccionario
        return {
            "peso_total": peso_total_solucion,
            "promedio_auRec": promedio_auRec_final,
            "cantidad_lotes_seleccionados": lotes_seleccionados,
            "ids_lotes_seleccionados": lotes_seleccionados_array
        }
    else:
        print("\n❌ No se encontró una combinación válida dentro del rango de peso y auRec.")
        return {
            "peso_total": None,
            "promedio_auRec": None,
            "cantidad_lotes_seleccionados": 0,
            "ids_lotes_seleccionados": []
        }
    

def optimizar_lotes_csv(peso_minimo, peso_maximo, auRec_min, auRec_max):
    """
    Función para optimizar la selección de lotes según restricciones de peso y promedio de auRec.

    Parámetros:
        peso_minimo (float): Peso mínimo permitido.
        peso_maximo (float): Peso máximo permitido.
        auRec_min (float): Valor mínimo permitido para el promedio de auRec.
        auRec_max (float): Valor máximo permitido para el promedio de auRec.

    Retorna:
        dict: Un diccionario con los resultados de la optimización.
    """

    csv_path = "/app/lotes.csv"

    df_selected = pd.read_csv(csv_path)


    # 🛠️ Limpiar el DataFrame (eliminar valores no válidos)
    df_selected = df_selected.replace([np.inf, -np.inf], np.nan)
    df_selected = df_selected.dropna(subset=['tmsBase', 'auRec'])

    print('Cantidad de lotes después de limpiar datos:')
    print(len(df_selected))
    print('__________________________________________________')

    # 🚀 Crear el problema de optimización
    problema = LpProblem("Optimización_Lotes_Peso_auRec", LpMaximize)

    # ✅ Variables binarias (1 si el lote se usa, 0 si no)
    variables = {i: LpVariable(f"Lote_{df_selected.iloc[i]['id']}", cat="Binary") for i in range(len(df_selected))}

    # ✅ Restricción de peso total (debe estar entre peso_minimo y peso_maximo)
    peso_total = lpSum(variables[i] * df_selected.iloc[i]['tmsBase'] for i in range(len(df_selected)))
    problema += peso_total <= peso_maximo, "Restricción de peso máximo"
    problema += peso_total >= peso_minimo, "Restricción de peso mínimo"

    # ✅ Objetivo: Maximizar la cantidad de lotes seleccionados dentro del rango de peso
    total_lotes = lpSum(variables[i] for i in range(len(df_selected)))
    problema += total_lotes, "Maximizar cantidad de lotes"

    # 🏆 Resolver el problema usando el solver CBC
    problema.solve(PULP_CBC_CMD(msg=False))

    # 📌 Mostrar la mejor combinación de lotes seleccionados
    print("Lotes seleccionados:")
    peso_total_solucion = 0
    auRec_total_solucion = 0
    lotes_seleccionados = 0  # Contador de lotes seleccionados
    lotes_seleccionados_array = []

    for i in range(len(df_selected)):
        if value(variables[i]) == 1:
            lote = df_selected.iloc[i]
            nuevo_peso_total = peso_total_solucion + lote['tmsBase']
            nuevo_auRec_total = auRec_total_solucion + lote['auRec']
            nuevo_promedio_auRec = nuevo_auRec_total / (lotes_seleccionados + 1)

            # 🚨 Verificar que el peso y el auRec promedio estén dentro de los límites
            if nuevo_peso_total > peso_maximo or not (auRec_min <= nuevo_promedio_auRec <= auRec_max):
                continue  # No incluir este lote si se pasa el peso o el promedio de auRec está fuera del rango

            # ✅ Si el lote cumple con las condiciones, se agrega al grupo
            peso_total_solucion = nuevo_peso_total
            auRec_total_solucion = nuevo_auRec_total
            lotes_seleccionados += 1
            lotes_seleccionados_array.append(lote['id'])

    # 📊 Mostrar resultados finales
    if lotes_seleccionados > 0:
        promedio_auRec_final = auRec_total_solucion / lotes_seleccionados
        print(f"\n✅ Peso total: {peso_total_solucion:.3f} (Debe estar entre {peso_minimo} y {peso_maximo})")
        print(f"✅ Promedio de auRec: {promedio_auRec_final:.5f} (Debe estar entre {auRec_min} y {auRec_max})")
        lotes_seleccionados_array = [int(lote_id) for lote_id in lotes_seleccionados_array]
        print(f"\n✅ Cantidad de lotes seleccionados: {lotes_seleccionados}")
        print(f"✅ IDs de los lotes seleccionados: {lotes_seleccionados_array}")

        # Retornar los resultados como un diccionario
        return {
            "peso_total": peso_total_solucion,
            "promedio_auRec": promedio_auRec_final,
            "cantidad_lotes_seleccionados": lotes_seleccionados,
            "ids_lotes_seleccionados": lotes_seleccionados_array
        }
    else:
        print("\n❌ No se encontró una combinación válida dentro del rango de peso y auRec.")
        return {
            "peso_total": None,
            "promedio_auRec": None,
            "cantidad_lotes_seleccionados": 0,
            "ids_lotes_seleccionados": []
        }