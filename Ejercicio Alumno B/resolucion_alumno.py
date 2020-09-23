FIN = chr(255)
CAMPOS_CSV = 4

def abrir_archivos(*archivos):
    '''le llega por parametro la ruta de n archivos, los abre y devuelve una
    lista con el contenido de los archivos.'''
    return [open(archivo, 'r') for archivo in archivos]

def leer_linea(archivo):
    '''lee una linea del archivo que le llega por parametro y si es el final del
    archivo devuelve un FIN, y sino una lista con los campos de la linea (separados).'''
    linea = archivo.readline()

    return linea.strip('\n').split(',') if linea else [FIN] * CAMPOS_CSV

def leer_primeras_lineas(archivos):
    '''lee una linea de cada archivo de la tupla que llega por paramtro y devuelve
    una lista de listas (cada elemento de la lista padre es una lista hija con los
    campos de la linea del csv).'''
    return [leer_linea(archivo) for archivo in archivos]

def escribir_salida(salida, entrada, linea):
    '''escribe en el archivo de salida una linea.'''
    salida.write(f'{",".join(linea)}\n')

def procesar_linea(entrada, linea, datos):
    '''recibe una linea, el archivo de entrada y el diccionario de datos; con
    esto, se procesan los datos de interes y luego se lee la siguiente linea
    de la entrada.'''

    cod_articulo, fecha_registro, tipo_op, cant_unidades = linea
    año = fecha_registro[:4]
    mes = int(fecha_registro[4:6])
    if año not in datos:
        datos[año] = {'meses': {}}
    if mes not in datos[año]['meses']:
        datos[año]['meses'][mes] = 0
    datos[año]['meses'][mes] += int(cant_unidades) if tipo_op == 'DEVOL' else 0

    return leer_linea(entrada), datos

def merge(salida, *entradas):
    '''lee secuencialmente a los archivos de entrada, busca la menor linea y la
    escribe en el archivo de salida hasta que no hay mas lineas para leer.'''

    datos = {}
    lineas = leer_primeras_lineas(entradas)
    menor = sorted(lineas, key=lambda x: x[0])[0]
    while menor[0] != FIN:
        indice_menor = lineas.index(menor)
        escribir_salida(salida, entradas[indice_menor], menor)
        lineas[indice_menor], datos = procesar_linea(entradas[indice_menor], menor, datos)
        menor = sorted(lineas, key=lambda x: x[0])[0]

    return datos

def mostrar_datos(datos):
    '''ordena e imprime los datos del diccionario.'''

    datos_ordenados = sorted(datos.items(), key=lambda x: x[1]['meses'])
    print(datos_ordenados)
    for año, datos in datos_ordenados:
        print(año)
        for mes, devoluciones in datos['meses'].items():
            print(f'Mes: {mes}, Devoluciones: {devoluciones}')

def cerrar_archivos(*archivos):
    '''cierra los archivos que le lleguen por parametro'''

    for archivo in archivos:
        archivo.close()

def main():
    sucursal1, sucursal2, sucursal3, sucursal4, sucursal5 = abrir_archivos('sucursal1.csv', 'sucursal2.csv', 'sucursal3.csv', 'sucursal4.csv', 'sucursal5.csv')
    archivo_salida = open('sucursales.csv', 'w+')
    datos = merge(archivo_salida, sucursal1, sucursal2, sucursal3, sucursal4, sucursal5)
    mostrar_datos(datos)
    cerrar_archivos(archivo_salida, sucursal1, sucursal2, sucursal3, sucursal4, sucursal5)

main()

'''
FIN = chr(255)
CAMPOS = 4

def abrir_archivos(*archivos):
    return [open(archivo, 'r') for archivo in archivos]

def leer_linea(archivo):
    linea = archivo.readline()
    return linea.strip('\n').split(',') if linea else [FIN] * CAMPOS

def leer_primeras_lineas(archivos):
    return [leer_linea(archivo) for archivo in archivos]

def escribir_salida(salida, entrada, linea):
    salida.write(f'{",".join(linea)}\n')
    return leer_linea(entrada)

def merge(salida, *entradas):
    lineas = leer_primeras_lineas(entradas)
    menor = sorted(lineas, key=lambda x: x[0])[0]
    while menor[0] != FIN:
        indice_menor = lineas.index(menor)
        lineas[indice_menor] = escribir_salida(salida, entradas[indice_menor], menor)
        menor = sorted(lineas, key=lambda x: x[0])[0]

def separacion(str1, str2=''):
    return ' ' * (len(str1) - len(str2))

def corte_control(salida):
    "ubica el cursor en el comienzo del archivo de salida y ordena los datos
    en una lista por año y por mes."
    salida.seek(0)
    cod_articulo, fecha_registro, tipo_op, cant_unidades = leer_linea(salida)
    año = fecha_registro[:4]
    mes = fecha_registro[4:6]
    while cod_articulo != FIN:
        devoluciones_año = 0
        año_ant = año
        print(f'Año: {año}\n')
        print(f'{separacion("Año: ")}Mes\tDevoluciones')
        while cod_articulo != FIN and año_ant == año:
            devoluciones_mes = 0
            mes_ant = mes
            while cod_articulo != FIN and año_ant == año and mes_ant == mes:
                if tipo_op == 'DEVOL':
                    devoluciones_mes += int(cant_unidades)
                cod_articulo, fecha_registro, tipo_op, cant_unidades = leer_linea(salida)
                if cod_articulo != FIN:
                    año = fecha_registro[:4]
                    mes = fecha_registro[4:6]
            #muestra las devoluciones del mes si es que hubieron
            if devoluciones_mes:
                print(f'{separacion("Año: "+"Mes", mes_ant)}{mes_ant}\t{separacion("Devoluciones", str(devoluciones_mes))}{devoluciones_mes}')
        devoluciones_año += devoluciones_mes
    print(f'Devoluciones del año: {devoluciones_año}')

def cerrar_archivos(*archivos):
    for archivo in archivos:
        archivo.close()

def main():
    sucursal1, sucursal2, sucursal3, sucursal4, sucursal5 = abrir_archivos('sucursal1.csv', 'sucursal2.csv', 'sucursal3.csv', 'sucursal4.csv', 'sucursal5.csv')
    archivo_salida = open('sucursales.csv', 'w+')
    merge(archivo_salida, sucursal1, sucursal2, sucursal3, sucursal4, sucursal5)
    corte_control(archivo_salida)
    cerrar_archivos(archivo_salida, sucursal1, sucursal2, sucursal3, sucursal4, sucursal5)

main()
'''
