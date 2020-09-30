"""
Una Casa de artículos eléctricos registra las ventas de sus productos en un archivo CSV, por cada una de sus 4 Sucursales.  Los archivos están ordenados por código de producto en forma ascendente.

Cada uno de estos 4 archivos contiene la siguiente información:

codigo_producto: numérico
fecha_venta: AAAAMMDD
categoria: Iluminacion/Conductores/Ventilacion/Tomas/Termicas
cantidad_unidades: numéricas
Se pide confeccionar un programa modular en Python, para procesar la información de los 5 archivos, de manera de obtener como resultado:

Un archivo secuencial CSV ordenado por código de producto, con sólo un registro por cada código de producto. La línea debe estar formada por el código de producto, y la cantidad total vendida del producto. Si la categoría no es una de las mencionadas, la línea no tiene que procesarse y debe enviarse al archivo errores.txt, agregando a la línea la sucursal de la que proviene.
Informar para cada categoría la cantidad de productos vendidos, ordenada en forma ascendente por la cantidad vendida, sólo para los productos vendidos durante el 1er. semestre del año 2020.
Informar la cantidad de ventas totales por mes.
Aclaraciones:

No cargar ningún archivo en su totalidad en memoria
Leer solo los archivos de entrada y solo una vez cada uno
Un mismo código de producto puede aparecer en más de un archivo.
Un mismo código de producto puede aparecer más de una vez en el mismo archivo.
El programa en Python debe ser estructurado, modular y claro.
"""


COD_MAX = "999999"
FECHA_MAX = "99999999"
DEFAULT = COD_MAX+','+FECHA_MAX+',,'

# 1) Crear nuevo arhivo que tome codigo de producto y cantidad vendida total por producto de sucursales

def leer_archivos(archivo, default):
    linea = archivo.readline()
    return linea.rstrip('\n').split(',') if linea else default.split(',')

def generar_general_nuevo(archivo, codigo_producto, cant_vendida):
    codigo = str(codigo_producto)
    cantidad_unidades = str(cant_vendida)
    archivo.write(codigo + ',' + cantidad_unidades + '\n')

def generar_errores(archivo, codigo_producto, cant_vendida, sucursal_error):
    codigo = str(codigo_producto)
    cantidad_unidades = str(cant_vendida)
    archivo.write(codigo_producto + ',' + cant_vendida + ',' + sucursal_error + '\n')


# 2) Imprimir cantidad vendida por categoría primeros 6 meses de 2020

def separar_por_mes(fecha):
    mes = fecha[4:6]
    año = fecha[0:4]
    primer_semestre = False
    if str(año) =='2020' and str(mes) <= '06':
        primer_semestre = True
    return mes,primer_semestre

def separar_categorias(categoriaN, fechaN, cantidad_por_categoria):
    if categoriaN in cantidad_por_categoria:
        mes,es_primer_semestre = separar_por_mes(fechaN)
        if es_primer_semestre == True:
            cantidad_por_categoria[categoriaN] += 1

def imprimir_categorias(cantidad_por_categoria):
    for categoria in cantidad_por_categoria:
        print("\n ------------------------------ \n")
        print("La cantidad de productos vendidos para {} en el primer semestre 2020:".format(categoria))
        print(cantidad_por_categoria[categoria])


def combinar_archivos(sucursal_1,sucursal_2,sucursal_3,sucursal_4,sucursal_general,errores):
    codigo_producto1, fecha1, categoria1, cantidad_vendida1 = leer_archivos(sucursal_1,DEFAULT)
    codigo_producto2, fecha2, categoria2, cantidad_vendida2 = leer_archivos(sucursal_2,DEFAULT)
    codigo_producto3, fecha3, categoria3, cantidad_vendida3 = leer_archivos(sucursal_3,DEFAULT)
    codigo_producto4, fecha4, categoria4, cantidad_vendida4 = leer_archivos(sucursal_4,DEFAULT)

    cantidad_por_categoria = {'Iluminacion':0, 
                              'Conductores':0,
                              'Ventilacion':0,
                              'Tomas':0,
                              'Termicas':0}
    
    while (codigo_producto1 < COD_MAX) or (codigo_producto2 < COD_MAX) or (codigo_producto3 < COD_MAX) or (codigo_producto4 < COD_MAX):
        total_por_cuenta = 0
        total_vendido = 0
        codigo_menor = min(codigo_producto1,codigo_producto2,codigo_producto3,codigo_producto4)
        while codigo_producto1 == codigo_menor:
            if categoria1 in cantidad_por_categoria:
                total_por_cuenta += int(cantidad_vendida1)
                separar_categorias(categoria1, fecha1, cantidad_por_categoria)
            else:
                generar_errores(errores, codigo_producto1, cantidad_vendida1, "sucursal_1")
            codigo_producto1, fecha1, categoria1, cantidad_vendida1 = leer_archivos(sucursal_1,DEFAULT)
        while codigo_producto2 == codigo_menor:
            if categoria2 in cantidad_por_categoria:
                total_por_cuenta += int(cantidad_vendida2)
                separar_categorias(categoria2, fecha2, cantidad_por_categoria)
            else:
                generar_errores(errores, codigo_producto2, cantidad_vendida2, "sucursal_2")
            codigo_producto2, fecha2, categoria2, cantidad_vendida2 = leer_archivos(sucursal_2,DEFAULT)
        while codigo_producto3 == codigo_menor:
            if categoria3 in cantidad_por_categoria:
                total_por_cuenta += int(cantidad_vendida3)
                separar_categorias(categoria3, fecha3, cantidad_por_categoria)
            else:
                generar_errores(errores, codigo_producto3, cantidad_vendida3, "sucursal_3")
            codigo_producto3, fecha3, categoria3, cantidad_vendida3 = leer_archivos(sucursal_3,DEFAULT)
        while codigo_producto4 == codigo_menor:
            if categoria4 in cantidad_por_categoria:
                total_por_cuenta += int(cantidad_vendida4)
                separar_categorias(categoria4, fecha4, cantidad_por_categoria)
            else:
                generar_errores(errores, codigo_producto4, cantidad_vendida4, "sucursal_4")
            codigo_producto4, fecha4, categoria4, cantidad_vendida4 = leer_archivos(sucursal_4,DEFAULT)

        generar_general_nuevo(sucursal_general, codigo_menor, total_por_cuenta)

    imprimir_categorias(cantidad_por_categoria)



# 3) Imprimir ventas totales por mes 


# Disclaimer: NO LO TERMINE, ME FALTA ESE PUNTO


def main():
    sucursal_1 = open('datos/sucursal_1.csv', 'r')
    sucursal_2 = open('datos/sucursal_2.csv', 'r')
    sucursal_3 = open('datos/sucursal_3.csv', 'r')
    sucursal_4 = open('datos/sucursal_4.csv', 'r')
    sucursal_general = open('datos/sucursal_general.csv', 'w')
    errores = open('datos/errores.txt', 'w')

    combinar_archivos(sucursal_1,sucursal_2,sucursal_3,sucursal_4,sucursal_general, errores)
   

    sucursal_1.close()
    sucursal_2.close()
    sucursal_3.close()
    sucursal_4.close()
    sucursal_general.close()
    errores.close()

main()