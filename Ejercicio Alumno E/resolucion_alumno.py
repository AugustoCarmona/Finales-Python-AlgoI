"""

Una facultad tiene un archivo secuencial CSV por cada una de sus 3 Sedes.
Dichos archivos están ordenados en forma ascendente, por Padrón, y contienen la información de las evaluaciones tomadas en cada una de las 4 sedes.
Los campos son: padron (numérico), cod_materia (numérico), fecha (AAAAMMDD), calificación (numérico).
Se tiene también un archivo CSV que contiene para cada cod_materia, el nombre de la materia. Este archivo no tiene orden alguno, y sólo puede ser leído una vez en todo el programa. 
Se pide:

Procesar los archivos obteniendo como resultado un único archivo CSV, ordenado ascendentemente por Padrón, dónde cada línea esté compuesta por: padrón, cod_materia, nombre_materia, fecha, calicacion ; y sólo si la materia fue aprobada por el alumno en el año 2020.
En caso que el nombre de la materia no exista, esa línea debe ser enviada al archivo de errores.txt

Informar las 5 materias con más aprobados durante el año 2020, ordenadas descendentemente por cantidad de aprobados.

"""
def leer_sedes(sede,max_padron):
    
    linea=sede.readline().rstrip("\n").split(",")
    return linea if linea!=[""] else [max_padron,"","",""]

def grabar_errores(error,padron,codigo,fecha,calificacion):
    
    error.write(padron+","+codigo+","+fecha+","+calificacion+"\n")
    
    
def grabar_sedes_totales(sedes,padron,codigo,materia,fecha,calificacion):
    sedes.write(padron+","+codigo+","+materia+","+fecha+","+calificacion+"\n")
    
def procesar_archivo_materia(materias):
    datos_de_materias={}
    linea=materias.readline().rstrip("\n").split(",")
    while linea!=[""]:
        datos_de_materias[linea[0]]=linea[1]
        linea=materias.readline().rstrip("\n").split(",")
        
    return datos_de_materias
 
def imprimir_por_pantalla(dato):
    print("LAS 5 MATERIAS CON MAS APROBADAS DURANTE EL AÑO 2020 SON: \n")
    for posicion in dato:
        print("La materia: ",posicion[0]," fue aprobada con la cantidad de :",posicion[1] )
        print("")

def procesar_archivos(sede_1,sede_2,sede_3,errores,datos_de_materias,sedes_totales):
    mayor_materias_aprobadas={}
    max_padron="9999999999"
    padron_sede_1,cod_materia_sede_1,fecha_sede_1,calificacion_sede_1=leer_sedes(sede_1,max_padron)
    padron_sede_2,cod_materia_sede_2,fecha_sede_2,calificacion_sede_2=leer_sedes(sede_2,max_padron)
    padron_sede_3,cod_materia_sede_3,fecha_sede_3,calificacion_sede_3=leer_sedes(sede_2,max_padron)
    
    while padron_sede_1 != max_padron or padron_sede_2 != max_padron or padron_sede_3 != max_padron:
        
        menor_padron=min(padron_sede_1,padron_sede_2,padron_sede_3)
        
        while padron_sede_1==menor_padron:
            
            if cod_materia_sede_1 in datos_de_materias:
                
                if fecha_sede_1[:4]=="2020" and int(calificacion_sede_1)>=4:
                    grabar_sedes_totales(sedes_totales,padron_sede_1,cod_materia_sede_1,datos_de_materias[cod_materia_sede_1],fecha_sede_1,calificacion_sede_1)
                    
                    if  datos_de_materias[cod_materia_sede_1] not in mayor_materias_aprobadas:
                        mayor_materias_aprobadas[datos_de_materias[cod_materia_sede_1]]=1
                    
                    else:
                        mayor_materias_aprobadas[datos_de_materias[cod_materia_sede_1]]+=1
            else:
                grabar_errores(errores,padron_sede_1,cod_materia_sede_1,fecha_sede_1,calificacion_sede_1)
                
            padron_sede_1,cod_materia_sede_1,fecha_sede_1,calificacion_sede_1=leer_sedes(sede_1,max_padron)
            
        while padron_sede_2==menor_padron:
            
            if cod_materia_sede_2 in datos_de_materias:
                
                if fecha_sede_2[:4]=="2020" and int(calificacion_sede_2)>=4:
                        grabar_sedes_totales(sedes_totales,padron_sede_2,cod_materia_sede_2,datos_de_materias[cod_materia_sede_2],fecha_sede_2,calificacion_sede_2)
                        if  datos_de_materias[cod_materia_sede_2] not in mayor_materias_aprobadas:
                            mayor_materias_aprobadas[datos_de_materias[cod_materia_sede_2]]=1
                    
                        else:
                            mayor_materias_aprobadas[datos_de_materias[cod_materia_sede_2]]+=1
            
            else:
                
                grabar_errores(errores,padron_sede_2,cod_materia_sede_2,fecha_sede_2,calificacion_sede_2)
                
            padron_sede_2,cod_materia_sede_2,fecha_sede_2,calificacion_sede_2=leer_sedes(sede_2,max_padron)
            
        while padron_sede_3==menor_padron:
            
            if cod_materia_sede_3 in datos_de_materias:
                
                if fecha_sede_3[:4]=="2020" and int(calificacion_sede_3)>=4:
                        grabar_sedes_totales(sedes_totales,padron_sede_3,cod_materia_sede_3,datos_de_materias[cod_materia_sede_3],fecha_sede_3,calificacion_sede_3)
                        if  datos_de_materias[cod_materia_sede_3] not in mayor_materias_aprobadas:
                            mayor_materias_aprobadas[datos_de_materias[cod_materia_sede_3]]=1
                    
                        else:
                            mayor_materias_aprobadas[datos_de_materias[cod_materia_sede_3]]+=1
            
            else:
                
                grabar_errores(errores,padron_sede_3,cod_materia_sede_3,fecha_sede_3,calificacion_sede_3)
                
            padron_sede_3,cod_materia_sede_3,fecha_sede_3,calificacion_sede_3=leer_sedes(sede_3,max_padron)

    ordenada_materias_aprobadas=sorted(mayor_materias_aprobadas.items(),key=lambda posicion:posicion[1],reverse=True)
    imprimir_por_pantalla(ordenada_materias_aprobadas[:5])
          
#----------------------------------------BLOQUE PRINCIPAL-------------------------------------------------------------------------------------

sede_1=open("sede_1.csv","r")
sede_2=open("sede_2.csv","r")
sede_3=open("sede_3.csv","r")
materias=open("materias.csv","r")
sedes_totales=open("sedes_totales.csv","w")
errores=open("errores.txt","w")
datos_de_materias=procesar_archivo_materia(materias)
procesar_archivos(sede_1,sede_2,sede_3,errores,datos_de_materias,sedes_totales)
sede_1.close()
sede_2.close()
sede_3.close()
materias.close()
sedes_totales.close()
errores.close()


