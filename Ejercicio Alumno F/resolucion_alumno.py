"""
Una facultad tiene un archivo secuencial CSV por cada una de sus 3 Sedes.
Dichos archivos están ordenados en forma ascendente, por Padrón, y contienen la información de las evaluaciones
tomadas en cada una de las 4 sedes.
Los campos son: padron (numérico), cod_materia (numérico), fecha (AAAAMMDD), calificación (numérico).
Se tiene también un archivo CSV que contiene para cada cod_materia, el nombre de la materia.
Este archivo no tiene orden alguno, y sólo puede ser leído una vez en todo el programa. 
Se pide:

Procesar los archivos obteniendo como resultado un único archivo CSV, ordenado ascendentemente por Padrón,
dónde cada línea esté compuesta por: padrón, cod_materia, nombre_materia, fecha, calicacion ;
y sólo si la materia fue aprobada por el alumno en el año 2020.
En caso que el nombre de la materia no exista, esa línea debe ser enviada al archivo de errores.txt

Informar las 5 materias con más aprobados durante el año 2020, ordenadas descendentemente por cantidad de aprobados.

Aclaraciones:

Sólo el archivo materias puede ser cargado totalmente en memoria.
Leer solo los archivos de entrada y solo una vez cada uno
Un mismo padrón puede aparecer en más de un archivo.
Un mismo padrón puede aparecer más de una vez en el mismo archivo.
El programa en Python debe ser estructurado, modular y claro.
"""
ultimo = "999999"
FIN = [ultimo,"","",""]

def leer_linea(archivo):
    linea = archivo.readline()
    return linea.rstrip("\n").split(",") if linea else FIN

def cargar_materias():
    datos = {}
    ar_materias = open("materias.csv")
    linea = ar_materias.readline().rstrip("\n").split(",")
    while linea != ['']:
    
        cod_materia, nombre_materia = linea
        datos[cod_materia] = nombre_materia
        linea = ar_materias.readline().rstrip("\n").split(",")
        
    return datos

def abrir_archivos(l_archivos):
    return [open(archivo) for archivo in l_archivos]

def procesar_aprobados(dicc, cod_materia):
    
    if cod_materia not in dicc:
        dicc[cod_materia] = 1
    else:
        dicc[cod_materia] += 1
    return dicc

def procesar_linea(linea, dicc, ar_errores, ar_aprobados, aprobados):    
    
    padron, cod_materia, fecha, calificacion = linea
    año = fecha[:4]
    if cod_materia not in dicc:
        ar_errores.write(",".join(linea)+"\n")
    else:
        if int(calificacion) >= 4 and año == "2020":
            ar_aprobados.write(padron+","+cod_materia+","+dicc[cod_materia]+","+fecha+","+calificacion+"\n")
            aprobados = procesar_aprobados(aprobados, cod_materia)
    return aprobados

def imprimir_informe(aprobados, nombres_materias):
    
    datos = sorted(aprobados.items() , key = lambda x:x[1], reverse = True)
    print("{:<35} {}".format("Materia","Aprobados"))
    
    for materia in datos[:5]:
        print("{:<35} {}".format(nombres_materias[materia[0]], materia[1]))
            
            
def cerrar_archivos(archivos):
    for archivo in archivos:
        archivo.close()
    
def merge(archivos):
    ar_errores = open("errores.txt", "w")
    ar_aprobados = open("aprobados_2020.csv", "w")
    dicc_materias = cargar_materias()
    aprobados = {}
    lineas = [leer_linea(archivo) for archivo in archivos]
    menor = min(lineas, key = lambda x:x[0])
    while menor[0] != ultimo:
        indice = lineas.index(menor)
        aprobados = procesar_linea(menor, dicc_materias, ar_errores, ar_aprobados, aprobados)
        lineas[indice] = leer_linea(archivos[indice])
        menor = min(lineas, key = lambda x:x[0])
    imprimir_informe(aprobados, dicc_materias)
    ar_errores.close()
    ar_aprobados.close()
        
def main():
    l_archivos = ["sede_1.csv", "sede_2.csv", "sede_3.csv"]
    archivos = abrir_archivos(l_archivos)
    merge(archivos)
    cerrar_archivos(archivos)
    
main()