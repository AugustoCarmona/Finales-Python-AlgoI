"""
Una facultad tiene un archivo secuencial CSV por cada una de sus 3 Sedes.
Dichos archivos están ordenados en forma ascendente, por Padrón, y contienen la información de las evaluaciones tomadas
en cada una de las 3 sedes.
Los campos son: padron (numérico), cod_materia (numérico), fecha (AAAAMMDD), calificación (numérico).
Se tiene también un archivo CSV que contiene para cada cod_materia, el nombre de la materia. Este archivo no tiene orden
alguno, y sólo puede ser leído una vez en todo el programa.
Se pide:

Procesar los archivos obteniendo como resultado un único archivo CSV, ordenado ascendentemente por Padrón,
dónde cada línea esté compuesta por:

    1) padrón, cod_materia, nombre_materia, fecha, calicacion ; y sólo si la materia fue aprobada por el alumno en el año 2020.
    En caso que el nombre de la materia no exista, esa línea debe ser enviada al archivo de errores.txt

    2) Informar las 5 materias con más aprobados durante el año 2020, ordenadas descendentemente por cantidad de aprobados.


Aclaraciones:

Sólo el archivo materias puede ser cargado totalmente en memoria.
Leer solo los archivos de entrada y solo una vez cada uno
Un mismo padrón puede aparecer en más de un archivo.
Un mismo padrón puede aparecer más de una vez en el mismo archivo.
El programa en Python debe ser estructurado, modular y claro.

"""
MAX_PADRON = '99999999999'
MAX_COD = '999999999999'


def leer_info(archivo):
    """
    Recibe un archivo como parametro y lee una linea de este, retornando el padron, el codigo de la materia, la fecha y
    la nota. En caso de ser la ultima linea, retorna como padron el centinela MAX_PADRON
    """
    linea = archivo.readline()
    if linea:
        padron, cod, fecha, nota = linea.rstrip("\n").split(",")
    else:
        padron, cod, fecha, nota = [MAX_PADRON, '0', '00000000', '0']
    return padron, cod, fecha, nota


def leer_info_materias(archivo):
    """
    Recibe un archivo(materias.csv) como parametro y lee una linea de este, retornando el codigo de la materia y su
    nombre. En caso de ser la ultima linea, retorna como codigo el centinela MAX_COD.
    """
    linea = archivo.readline()
    if linea:
        cod, materia = linea.rstrip("\n").split(",")
    else:
        cod, materia = [MAX_COD, 'Null']
    return cod, materia


def leer_info_merge(archivo):
    """
    Recibe un archivo(archivo_merge) como parametro y lee una linea de este, retornando el padron, el codigo de la
    materia, nombre de materia, la fecha y la nota. En caso de ser la ultima linea, retorna como padron el centinela
    MAX_PADRON

    """
    linea = archivo.readline()
    if linea:
        padron, cod, materia, fecha, nota = linea.rstrip("\n").split(",")
    else:
        padron, cod, materia, fecha, nota = [MAX_PADRON, '0', '0', '00000000', '0']
    return padron, cod, materia, fecha, nota


def abrir_archivos(*archivos):
    """
    Recibe una cantidad dinamica de paths a archivos y se encarga de abrir cada uno y meterlos en la lista de archivos
    a devolver.
    """
    lista_archivos = []
    for archivo in archivos:
        lista_archivos.append(open(archivo))
    return lista_archivos


def cerrar_archivos(*archivos):
    """
    Recibe una cantidad dinamica archivos ya abiertos y se encarga de cerrarlos.
    """
    for archivo in archivos:
        archivo.close()


def aprobado(nota):
    # Recibe un valor y devuelve true en caso de ser mayor o igual que 4.
    ap = False
    if int(nota) >= 4:
        ap = True
    return ap


def cargar_materia(archivo):
    """
    Recibe un archivo(materias.csv) y retorna un diccionario asi. {codigo_materia: nombre_materia}.
    """
    dic_cod_mat = {}
    cod, materia = leer_info_materias(archivo)
    while cod != MAX_COD:
        dic_cod_mat[cod] = materia
        cod, materia = leer_info_materias(archivo)
    return dic_cod_mat


def buscar_materia(cod, dic):
    # Busca la materia por codigo y retorna el nombre en caso de encontrarlo y "No existente" en caso de no existir.
    materia = "No existente"
    for key in dic:
        if key == cod:
            materia = dic[key]
    return materia


def escribir(salida, padron, cod, materia, fecha, nota):
    # Escribe en el archivo de salida pasado por parametro el padron, codigo de materia, materia, fecha y nota.
    linea = padron + "," + cod + "," + materia + "," + fecha + "," + nota + "\n"
    salida.write(linea)


def merge(ar_merge, ar_error, sede1, sede2, sede3, dic_cod_mat):
    """
    Recibe 2 archivos de salida (ar_merge) y (ar_error), 3 archivos a mergear y el diccionario con el codigo de materia
    y nombre de materia.
    Genera el merge_sedes.csv y el errores.txt.
    """
    padron1, cod1, fecha1, nota1 = leer_info(sede1)
    padron2, cod2, fecha2, nota2 = leer_info(sede2)
    padron3, cod3, fecha3, nota3 = leer_info(sede3)

    while padron1 != MAX_PADRON or padron2 != MAX_PADRON or padron3 != MAX_PADRON:
        menor = min(padron1, padron2, padron3)

        while menor == padron1:
            # print(padron1)
            if buscar_materia(cod1,
                              dic_cod_mat) == "No existente":  # No hace falta que esten aprobado para ir al errores.txt. Solo que no tengan materia.
                escribir(ar_error, padron1, cod1, "Sin nombre", fecha1, nota1)
            elif aprobado(nota1) and buscar_materia(cod1,
                                                    dic_cod_mat) != "No existente":  # Supongo que aquellas lineas que no tienen materia no las meto en el archivo_merge.
                escribir(ar_merge, padron1, cod1, buscar_materia(cod1, dic_cod_mat), fecha1, nota1)

            padron1, cod1, fecha1, nota1 = leer_info(sede1)
        while menor == padron2:
            # print(padron2)
            if buscar_materia(cod1, dic_cod_mat) == "No existente":
                escribir(ar_error, padron2, cod2, "Sin nombre", fecha2, nota2)
            elif aprobado(nota2) and buscar_materia(cod2, dic_cod_mat) != "No existente":
                escribir(ar_merge, padron2, cod2, buscar_materia(cod2, dic_cod_mat), fecha2, nota2)

            padron2, cod2, fecha2, nota2 = leer_info(sede2)
        while menor == padron3:
            # print(padron3)
            if buscar_materia(cod3, dic_cod_mat) == "No existente":
                escribir(ar_error, padron3, cod3, "Sin nombre", fecha3, nota3)
            elif aprobado(nota3) and buscar_materia(cod3, dic_cod_mat) != "No existente":
                escribir(ar_merge, padron3, cod3, buscar_materia(cod3, dic_cod_mat), fecha3, nota3)

            padron3, cod3, fecha3, nota3 = leer_info(sede3)

    print(
        "\nTermine de realizar el merge de las materias aprobadas (merge_sedes.csv).\nAquellas materias sin nombre fueron informadas en el errores.txt\n\n")


def crear_dic_aprobados(archivo):
    """
    Recibe un archivo(archivo_merge) y genera un diccionario asi--> {materia: cantidad de aprobados}.
    Retorna el diccionario ya ordenado por cantidad de aprobados de formas descendente.
    """
    dic_aprobados = {}
    padron, cod, materia, fecha, nota = leer_info_merge(archivo)
    while padron != MAX_PADRON:
        if materia not in dic_aprobados:
            dic_aprobados[materia] = 1
        else:
            dic_aprobados[materia] += 1
        padron, cod, materia, fecha, nota = leer_info_merge(archivo)
    return sorted(dic_aprobados.items(), key=lambda item: item[1], reverse=True)


def mostrar_top(dic, top):
    # Recibe un diccionario y el numero de top (ejemplo; Top 5). Imprime por pantalla el top de elementos en el diccionario previamente ordenado.
    print("TOP", "MATERIA", "APROBADOS")
    for i in range(top):
        print(i + 1, dic[i][0], dic[i][1])


def main():
    # Punto 1.
    sede1, sede2, sede3, materias = abrir_archivos("recursos/sede_1.csv", "recursos/sede_2.csv", "recursos/sede_3.csv",
                                                   "recursos/materias.csv")
    archivo_merge = open("merge_sedes.csv", "w")
    archivo_errores = open("errores.txt", "w")
    dic_cod_materias = cargar_materia(materias)  # Diccionario = {codigo: materia} cargado a partir del materias.csv
    merge(archivo_merge, archivo_errores, sede1, sede2, sede3, dic_cod_materias)
    cerrar_archivos(sede1, sede2, sede3, materias, archivo_merge, archivo_errores)

    # Punto 2.
    top = 5
    archivo_merge = open("merge_sedes.csv", "r")
    dic_aprobados = crear_dic_aprobados(archivo_merge)
    mostrar_top(dic_aprobados, top)


main()
