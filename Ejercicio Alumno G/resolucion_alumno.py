'''Una facultad tiene un archivo secuencial CSV por cada una de sus 3 Sedes.
Dichos archivos están ordenados en forma ascendente, por Padrón, y contienen 
la información de las evaluaciones tomadas en cada una de las 4 sedes.
Los campos son: padron (numérico), cod_materia (numérico), fecha (AAAAMMDD), calificación (numérico).
Se tiene también un archivo CSV que contiene para cada cod_materia, el nombre de la materia. 
Este archivo no tiene orden alguno, y sólo puede ser leído una vez en todo el programa. 
Se pide:

Procesar los archivos obteniendo como resultado un único archivo CSV, 
ordenado ascendentemente por Padrón, dónde cada línea esté compuesta por:
 padrón, cod_materia, nombre_materia, fecha, calicacion ; 
 y sólo si la materia fue aprobada por el alumno en el año 2020.
En caso que el nombre de la materia no exista, 
esa línea debe ser enviada al archivo de errores.txt

Informar las 5 materias con más aprobados durante el año 2020, 
ordenadas descendentemente por cantidad de aprobados.

Aclaraciones:

Sólo el archivo materias puede ser cargado totalmente en memoria.
Leer solo los archivos de entrada y solo una vez cada uno
Un mismo padrón puede aparecer en más de un archivo.
Un mismo padrón puede aparecer más de una vez en el mismo archivo.
El programa en Python debe ser estructurado, modular y claro.'''

#Seteo de Variables, sin la ruta no me anda, favor cambiar para probar
MAX = ['99999999','','','']
ruta = 'C:\\Users\\churro\\Documents\\FINAL2209\\Ejercicio Python\\'


def leer_lineas(archivo):
    #lectura de archivos para merge
    linea = archivo.readline()
    if linea:
        devolver = linea.rstrip('\n').split(',')
    else:
        devolver = MAX
    return devolver

def archivo_materias(lista):
    #Recopilacion de datos del archivo materias
   archivo = open(ruta +'materias.csv','r')
   lineas = leer_lineas_materias(archivo,lista)
   archivo.close()

def leer_lineas_materias(archivo,lista):
    #Lectura del archivo materias.csv
    lineas = archivo.readlines()
    for linea in lineas:
        devolver =linea.rstrip('\n').split(',')
        codigo = devolver[0]
        nombre = devolver[1]
        lista[codigo] = nombre
        
        
def escribir_archivos(linea,salida,errores,materias):
    #Escritura de archivo de errores y mergeados

    #Seteo de variables para mas facil lectura
    padron = linea[0]
    codigo = linea[1]
    fecha = linea[2]
    calificacion = linea[3]
    anio = fecha[:4]
    linea_a_imprimir = []


    if codigo in materias:
        if anio == '2020' and int(calificacion) >= 4 :
            nombre = materias[codigo]
            linea_a_imprimir = [padron, codigo,nombre, fecha,calificacion+'\n']
            salida.write(','.join(linea_a_imprimir))
    else:
        linea_errores = [padron, codigo, fecha,calificacion+'\n']
        errores.write(','.join(linea_errores))
        
def imprimir_aprobados(diccionario):
    #Imprime por consola las materias con mas aprobados

    #Ordeno el diccionario en base a la cantidad de aprobados
    diccionario_arreglado = sorted(diccionario.items(),key = lambda x:x[1], reverse = True)
    
    for i in diccionario_arreglado[:5]:
        codigo_materia = i[0]
        aprobados = i[1]
        linea_a_imprimir = 'La materia de codigo: ' + str(codigo_materia) + ' aprobaron ' + str(aprobados) + ' estudiantes'
        print(linea_a_imprimir)


def materias_aprobadas(linea,diccionario):
    #Genero un diccionario con el codigo de la materia y la cantidad de gente que la aprobo

    codigo = linea[1]
    calificacion = int(linea[3])
    fecha = linea[2]
    anio = fecha[:4]
    
    if calificacion >= 4 and anio == '2020':
        if codigo in diccionario:
            diccionario[codigo] += 1
        else:
            diccionario[codigo] = 1
        

def merge():

    #Apertura de archivos
    sede1 = open(ruta +'sede_1.csv','r')
    sede2 = open(ruta +'sede_2.csv','r')
    sede3 = open(ruta +'sede_3.csv','r')
    salida = open(ruta + 'sedes.csv', 'w')
    errores = open(ruta + 'errores.txt', 'w')

    #Inicializacion de variables
    materias = {}
    materias_aprobar = {}

    #Carga en memoria del archivo materias.csv 
    archivo_materias(materias)


    #Merge
    linea1, linea2, linea3 = leer_lineas(sede1),leer_lineas(sede2),leer_lineas(sede3)
    while linea1 != MAX or linea2 != MAX or linea3 != MAX :
        minimo = min(linea1[0],linea2[0],linea3[0])
        while linea1[0] == minimo:
            escribir_archivos(linea1,salida,errores,materias)
            materias_aprobadas(linea1,materias_aprobar)
            linea1= leer_lineas(sede1)
        while linea2[0] == minimo:
            escribir_archivos(linea2,salida,errores,materias)
            materias_aprobadas(linea2,materias_aprobar)
            linea2= leer_lineas(sede2)
        while linea3[0] == minimo:
            escribir_archivos(linea3,salida,errores,materias)
            materias_aprobadas(linea3,materias_aprobar)
            linea3= leer_lineas(sede3)

    #Impresion por consola de aprobados
    imprimir_aprobados(materias_aprobar)

    #Cerrada de archivos
    sede1.close()
    sede2.close()
    sede3.close()
    salida.close()
    errores.close()

def main():
    merge()
main()