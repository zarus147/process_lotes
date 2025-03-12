import pandas as pd
import json


'''def procesar_diferenciasx(data1, data2):
    # Convertir a DataFrames
    df_desactualizado = pd.DataFrame(data2)
    df_actualizado = pd.DataFrame(data1)

    # Renombrar columnas en el DataFrame actualizado
    df_actualizado = df_actualizado.rename(columns={
        'AR1_CCODART': 'codigo', 
        'ST1_NSTODIS0000': 'stock',
        'ST1_NSTODIS0001': 'stock_alm_1',
    })

    # Filtrar solo las columnas necesarias en ambos DataFrames
    almacenes_interes = {
        "f7a42145-a016-4f58-aca5-3600bed17c24": "stock",
        "356e73f5-a4ff-4234-b39c-9e00303d90cb": "stock_alm_1",
    }
    
    # Filtrando los datos por almacenes de interés
    df_desactualizado = df_desactualizado[df_desactualizado['almacenSNCId'].isin(almacenes_interes.keys())]
    
    # Renombrando columnas del DataFrame desactualizado
    df_desactualizado["namealmacen"] = df_desactualizado["almacenSNCId"].map(almacenes_interes)
    df_desactualizado = df_desactualizado.rename(columns={"stock": "stock_old"})

    # Merge de todos los datos en una sola operación
    df_comparado = pd.merge(
        df_desactualizado,
        df_actualizado[["codigo", "stock", "stock_alm_1"]].melt(id_vars=["codigo"], 
                                                                var_name="namealmacen", 
                                                                value_name="stock_new"),
        on=["codigo", "namealmacen"]
    )

    # Filtrar las diferencias
    diferencias_stock = df_comparado[df_comparado["stock_old"] != df_comparado["stock_new"]]

    print('Columnas de diferencias stock: ', diferencias_stock.columns)

    # Seleccionar las columnas necesarias
    resultado = diferencias_stock[["codigo", "id", "stock_new", "stock_security", "stock_minimo", "stock_max"]].rename(columns={
         "stock_new": "stock"
    })
    

    return resultado.to_dict(orient="records")'''

def procesar_diferenciasx(data1, data2):

     # Convertir a DataFrames
    with open("/app/datasql.json", "r") as file:
        datasql = json.load(file)

    df_sql = pd.DataFrame(datasql)
    df_actualizado = pd.DataFrame(data1)

    print(df_sql.columns)

    # Renombrar columnas en el DataFrame actualizado
    df_actualizado = df_actualizado.rename(columns={
        'AR1_CCODART': 'CODIGOS', 
    })

     # Identificar los códigos que no están en df_actualizado
    codigos_no_en_actualizado = df_sql[~df_sql['CODIGOS'].isin(df_actualizado['CODIGOS'])]

    # Convertir a un array de diccionarios
    codigos_no_en_actualizado_array = codigos_no_en_actualizado.to_dict(orient='records')

    # Retornar solo el array de objetos con los códigos que no están
    return codigos_no_en_actualizado_array



   



def procesar_diferencias():
    with open("/app/arraydesactualizado.json", "r") as file:
        arraydesactualizado = json.load(file)

    with open("/app/arrayactualizado.json", "r") as file:
        arrayactualizado = json.load(file)

    # Convertir los arrays a DataFrames de Pandas
    df_desactualizado = pd.DataFrame(arraydesactualizado)
    df_actualizado = pd.DataFrame(arrayactualizado)

    # Realizar el merge para comparar por "code"
    df_comparado = pd.merge(df_desactualizado, df_actualizado, on="code", suffixes=('_old', '_new'))

    # Filtrar las diferencias de stock
    diferencias_stock = df_comparado[df_comparado["stock_old"] != df_comparado["stock_new"]]

    # Seleccionar solo los códigos y el stock actualizado
    resultado = diferencias_stock[["code", "stock_new"]].rename(columns={"stock_new": "stock"})

    # Convertir a lista de diccionarios y devolver el resultado
    return resultado.to_dict(orient="records")

'''def procesar_diferenciasx(data1, data2):
    # Convertir los arrays a DataFrames de Pandas
    df_desactualizado = pd.DataFrame(data2) 
    df_actualizado = pd.DataFrame(data1)

    #Se cuenta con 4 almacenes  
    #'0000', '0001', '0002', '0003', '0004'

    almacenes_interes = [
    {
        "id": "f7a42145-a016-4f58-aca5-3600bed17c24",  #representa la almacen 0000
        "namealmacen": "stock"
    },
    {
        "id": "356e73f5-a4ff-4234-b39c-9e00303d90cb", #representa la almacen 0001
        "namealmacen": "stock_alm_1"
    },]


    #Segun el negocio nos interesa el 0000 y 0001

    df_actualizado = df_actualizado.rename(columns={
        'AR1_CCODART': 'codigo', 
        'ST1_NSTODIS0000': 'stock',
        'ST1_NSTODIS0001': 'stock_alm_1',
        'ST1_NSTODIS0002': 'stock_alm_2',
        'ST1_NSTODIS0003': 'stock_alm_3',
        'ST1_NSTODIS0004': 'stock_alm_4',
    })



    res = []
    for x in almacenes_interes:
        almacenx = df_desactualizado[df_desactualizado['almacenSNCId'] == x["id"]]
        almacenx  = almacenx.rename(columns={'stock': x["namealmacen"]})
        df_comparado = pd.merge(
            almacenx, 
            df_actualizado[['codigo', x["namealmacen"]]], 
            on="codigo", 
            suffixes=('_old', '_new')
        )

        print("Columnas de df_comparado:", df_comparado.columns)
        # Filtrar las diferencias de stock
        diferencias_stock = df_comparado[df_comparado[f'{x["namealmacen"]}_old'] != df_comparado[f'{x["namealmacen"]}_new']]
        

        # Seleccionar solo los códigos y el stock actualizado
        resultado = diferencias_stock[["codigo", "id", f'{x["namealmacen"]}_new']].rename(columns={f'{x["namealmacen"]}_new': "stock"})

        # Convertir a lista de diccionarios y devolver el resultado
        print(resultado)
        res.extend(resultado.to_dict(orient="records"))

    
    return res
'''

'''def procesar_diferenciasx(data1, data2):
    # Convertir los arrays a DataFrames de Pandas
    df_desactualizado = pd.DataFrame(data2) 
    df_actualizado = pd.DataFrame(data1)

    #Se cuenta con 4 almacenes  
    #'0000', '0001', '0002', '0003', '0004'
    almacenes = [
        'f7a42145-a016-4f58-aca5-3600bed17c24', #representa la almacen 0000
        '356e73f5-a4ff-4234-b39c-9e00303d90cb',#representa la almacen 0001
        '0451a826-343f-4c68-adde-faf842df83de', #representa la almacen 0002
        '591286ba-4d5e-44dd-a10a-923b509b6e7e', #representa la almacen 0003
        '27a8fb72-93da-419a-a113-4985d285cc9b'  #representa la almacen 0004
    ]

    almacenes_interes = [
    {
        "id": "f7a42145-a016-4f58-aca5-3600bed17c24",
        "namealmacen": "stock"
    },
    {
        "id": "356e73f5-a4ff-4234-b39c-9e00303d90cb",
        "namealmacen": "stock_alm_1"
    },]


    #Segun el negocio nos interesa el 0000 y 0001

    df_actualizado = df_actualizado.rename(columns={
        'AR1_CCODART': 'codigo', 
        'ST1_NSTODIS0000': 'stock',
        'ST1_NSTODIS0001': 'stock_alm_1',
        'ST1_NSTODIS0002': 'stock_alm_2',
        'ST1_NSTODIS0003': 'stock_alm_3',
        'ST1_NSTODIS0004': 'stock_alm_4',
    })

    almacen1 = df_desactualizado[df_desactualizado['almacenSNCId'] == almacenes[0]]
    almacen2 = df_desactualizado[df_desactualizado['almacenSNCId'] == almacenes[1]]


    for x in almacenes_interes:
        almacenx = df_desactualizado[df_desactualizado['almacenSNCId'] == x["id"]]
        almacenx  = almacenx.rename(columns={'stock': x["namealmacen"]})
        df_comparado = pd.merge(
            almacenx, 
            df_actualizado[['codigo', x["namealmacen"]]], 
            on="codigo", 
            suffixes=('_old', '_new')
        )

        print("Columnas de df_comparado:", df_comparado.columns)

    

    
    # Realizar el merge para comparar por "code"
    #df_comparado = pd.merge(df_desactualizado, df_actualizado, on="codigo", suffixes=('_old', '_new'))
    df_comparado = pd.merge(almacen1, df_actualizado[['codigo', 'stock']], on="codigo", suffixes=('_old', '_new'))
    df_comparado2 = pd.merge(almacen2, df_actualizado[['codigo', 'stock_alm_1']], on="codigo", suffixes=('_old', '_new'))

    print("Clunas de df comparado",df_comparado.columns)
    print('--------------------------------------------------')
    print("Clunas de df Actualizado",df_actualizado.columns)
    print("Clunas de df Desactualizado",df_desactualizado.columns)
    print('--------------------------------------------------')

    print("Clunas de df comparado",df_comparado2.columns)


    # Filtrar las diferencias de stock
    diferencias_stock = df_comparado[df_comparado["stock_old"] != df_comparado["stock_new"]]

    # Seleccionar solo los códigos y el stock actualizado
    resultado = diferencias_stock[["codigo", "id", "stock_new"]].rename(columns={"stock_new": "stock"})

    # Convertir a lista de diccionarios y devolver el resultado
    return resultado.to_dict(orient="records")'''




'''def procesar_diferenciasx(data1, data2):
  

    # Convertir los arrays a DataFrames de Pandas
    df_desactualizado = pd.DataFrame(data2) 
    df_actualizado = pd.DataFrame(data1)

    #Se cuenta con 4 almacenes  
    #'0000', '0001', '0002', '0003', '0004'
    almacenes = [
        'f7a42145-a016-4f58-aca5-3600bed17c24', #representa la almacen 0000
        '356e73f5-a4ff-4234-b39c-9e00303d90cb',#representa la almacen 0001
        '0451a826-343f-4c68-adde-faf842df83de', #representa la almacen 0002
        '591286ba-4d5e-44dd-a10a-923b509b6e7e', #representa la almacen 0003
        '27a8fb72-93da-419a-a113-4985d285cc9b'  #representa la almacen 0004
    ]
    #Segun el negocio nos interesa el 0000 y 0001




    df_actualizado = df_actualizado.rename(columns={
        'AR1_CCODART': 'codigo', 

        'ST1_NSTODIS0000': 'stock'
        'ST1_NSTODIS0001': 'stock_alm_1'
        'ST1_NSTODIS0002': 'stock_alm_2'
        'ST1_NSTODIS0003': 'stock_alm_3'
        'ST1_NSTODIS0004': 'stock_alm_4'
    })

    print("Columnas de df_actualizado despues de renombrar:", df_actualizado.columns)

    # Realizar el merge para comparar por "code"
    df_comparado = pd.merge(df_desactualizado, df_actualizado, on="codigo", suffixes=('_old', '_new'))
    print("Columnas de df_comparado:", df_comparado.columns)

    # Filtrar las diferencias de stock
    diferencias_stock = df_comparado[df_comparado["stock_old"] != df_comparado["stock_new"]]

    # Seleccionar solo los códigos y el stock actualizado
    resultado = diferencias_stock[["codigo", "id", "stock_new"]].rename(columns={"stock_new": "stock"})

    # Convertir a lista de diccionarios y devolver el resultado
    return resultado.to_dict(orient="records")
'''
    

'''def procesar_diferenciasx(data):

    df_data = pd.DataFrame(data)

    df_comparado = pd.merge(df_data, df_data, on="AR1_CCODART", suffixes=('_old', '_new'))

    diferencias_stock = df_comparado[df_comparado["ST1_NSTODIS0000_old"] != df_comparado["ST1_NSTODIS0000_new"]]

    resultado = diferencias_stock[["AR1_CCODART", "ST1_NSTODIS0000_new"]].rename(columns={"ST1_NSTODIS0000_new": "ST1_NSTODIS0000"})

    return resultado.to_dict(orient="records")'''
