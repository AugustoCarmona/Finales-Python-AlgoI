"""Una facultad tiene un archivo secuencial CSV por cada una de sus 4 Sedes.
Dichos archivos están ordenados en forma ascendente, por Padrón, y contienen la información de las
 evaluaciones tomadas en cada una de las 4 sedes.
Los campos son: padron (numérico), cod_materia (numérico), fecha (AAAAMMDD), calificación (numérico).
Se tiene también en memoria una lista de tuplas con el siguiente formato:
[(cod_materia, nombre_materia),…].
Declarar en el programa, una acorde a los datos contenidos en los archivos.

Se pide:

Procesar los archivos obteniendo como resultado un único archivo CSV, ordenado ascendentemente por Padrón, 
dónde cada línea esté compuesta por: padrón, cod_materia, nombre_materia, fecha, calicacion ; y sólo si la 
materia fue aprobada por el alumno.

Informar las 5 materias con menos aprobados, ordenadas ascendentemente por cantidad de aprobados.

Aclaraciones:

No cargar ningún archivo en su totalidad en memoria.
Leer solo los archivos de entrada y solo una vez cada uno
Un mismo padrón puede aparecer en más de un archivo.
Un mismo padrón puede aparecer más de una vez en el mismo archivo.
El programa en Python debe ser estructurado, modular y claro."""


maximo = 9999999999
diccionario_aprobados = {}
def leer_linea(archivo):
    linea = archivo.readline()
    if linea:
        devolucion = linea.rstrip("\n").split(",")
    else:
        devolucion = [maximo, "", "", ""]
    return devolucion

lista_materias = [(7540, "Algo1"), (7541, "Algo2"), (7542, "Algo3"), (6469, "AM1"), (7501, "Fisica1"), (6103, "AM2"), (6105, "AM3"), (7065, "Fisica2"), (8200, "Quimica1"), (8100, "Quimica2"), (9100, "IPC")]

def escribir(linea, archivo):
    if int(linea[3]) >= 4:
        nombre_materia = ""
        linea_a_escribir = ""
        for tupla in lista_materias:
            if tupla[0] == int(linea[1]):
                nombre_materia = tupla[1]
        linea.insert(2, nombre_materia)
        if nombre_materia not in diccionario_aprobados:
            diccionario_aprobados[nombre_materia] = 1
        else:
            diccionario_aprobados[nombre_materia] += 1
        for elemento in linea:
            linea_a_escribir += str(elemento) + ","
        archivo.write(linea_a_escribir[:-1] + "\n")


def merge():
    sede1 = open("sede1.csv", "r")
    sede2 = open("sede2.csv", "r")
    sede3 = open("sede3.csv", "r")
    sede4 = open("sede4.csv", "r")
    linea1, linea2, linea3, linea4 = leer_linea(sede1), leer_linea(sede2), leer_linea(sede3), leer_linea(sede4)
    with open("notas_totales.csv", "w") as escritura:   
        while linea1[0] != maximo or linea2[0] != maximo or linea3[0] != maximo or linea4[0] != maximo:
            men = min(int(linea1[0]), int(linea2[0]), int(linea3[0]), int(linea4[0]))
            while int(linea1[0]) == men:
                escribir(linea1, escritura)
                linea1 = leer_linea(sede1)
            while int(linea2[0]) == men:
                escribir(linea2, escritura)
                linea2 = leer_linea(sede2)
            while int(linea3[0]) == men:
                escribir(linea3, escritura)
                linea3  = leer_linea(sede3)
            while int(linea4[0]) == men:
                escribir(linea4, escritura)
                linea4 = leer_linea(sede4)
    sede1.close()
    sede2.close()
    sede3.close()
    sede4.close()


def imprimir_ranking(diccionario):
    dic_ordenado = sorted(diccionario.items(), key = lambda x:x[1])
    print("Las 5 materias con menos aprobados fueron:")
    for materia in dic_ordenado[:5]:
        print(materia[0] + " - " + str(materia[1]) + " aprobado/s")

def main():
    merge()
    imprimir_ranking(diccionario_aprobados)

main()