'''Una facultad tiene un archivo secuencial CSV por cada una de sus 3 Sedes.
Dichos archivos están ordenados en forma ascendente, por Padrón, y contienen la información de las evaluaciones tomadas en cada una de las 4 sedes.
Los campos son: padron (numérico), cod_materia (numérico), fecha (AAAAMMDD), calificación (numérico).
Se tiene también un archivo CSV que contiene para cada cod_materia, el nombre de la materia. Este archivo no tiene orden alguno, y sólo puede ser leído una vez en todo el programa. 
Se pide:

Procesar los archivos obteniendo como resultado un único archivo CSV, ordenado ascendentemente por Padrón, dónde cada línea esté compuesta por: padrón, cod_materia, nombre_materia, fecha, calicacion ; y sólo si la materia fue aprobada por el alumno en el año 2020.
En caso que el nombre de la materia no exista, esa línea debe ser enviada al archivo de errores.txt

Informar las 5 materias con más aprobados durante el año 2020, ordenadas descendentemente por cantidad de aprobados.'''

def leer_archivo(archivo):
    linea=archivo.readline().strip("\n").split(",")
    return linea if linea else ""

def grabar_archivo(linea, archivo):
    for i in range(len(linea)):
        if i<(len(linea)-1):
            archivo.write(linea[i]+",")
        else:
            archivo.write(linea[i]+"\n")

def realizar_merge(archivos, archivo_general, archivo_errores, materias):
    lineas=[]
    aprobados={}
    for materia in materias:
        aprobados[materia[1]]=0
    for archivo in archivos:
        lineas.append(leer_archivo(archivo))
    while lineas!=[]:
        menor=[]
        for i in range(len(lineas)):
            if menor==[]:
                menor=lineas[i]
                j=i
            elif lineas[i][0]<menor[0]:
                menor=lineas[i]
                j=i
        for i in range(len(materias)):
            if materias[i][0]==menor[1]:
                menor.insert(2, materias[i][1])
        if len(menor)==5:
            if int(menor[4])>=4 and '2020' in menor[3]:
                menor.append("Aprobada en 2020")
                aprobados[menor[2]]+=1
            grabar_archivo(menor, archivo_general)
        if len(menor)==4:
            if int(menor[3])>=4 and '2020' in menor[2]:
                menor.append("Aprobada en 2020")
            grabar_archivo(menor, archivo_errores)
        lineas[j]=leer_archivo(archivos[j])
        if lineas[j]==['']:
            del(lineas[j])
            archivos[j].close()
            del(archivos[j])
    return aprobados

def mostrar_aprobados(aprobados):
    i=0
    print("Lista ordenada descendientemente de aprobados en 2020:")
    for aprobado in sorted(aprobados,key=lambda l:aprobados[l],reverse=True):
        if i<5:
            print(aprobado,"con",aprobados[aprobado],"aprobados.")
        i+=1

def main():
    lista_archivos=["sede_1.csv","sede_2.csv","sede_3.csv"]
    archivos=[]
    materias=[]
    for archivo in lista_archivos:
        archivos.append(open(archivo,"r"))
    archivo_general=open("general.csv","w")
    archivo_materias=open("materias.csv","r")
    archivo_errores=open("errores.txt","w")
    linea=leer_archivo(archivo_materias)
    while linea!=['']:
        materias.append(linea)
        linea=leer_archivo(archivo_materias)
    archivo_materias.close()
    aprobados=realizar_merge(archivos, archivo_general, archivo_errores, materias)
    mostrar_aprobados(aprobados)
    archivo_general.close()
    archivo_errores.close() 

main()