from src.ssh import ssh
import re
from time import sleep
from Constantes.config import *
# from src.pdf_converter import *
import atexit
# from Constantes.regex import separadores




def bucle():
    # recorre el mapeo de los fsp en config.py, los separa y ejecuta
    for element in fsp:
        puertos = element.split("/")    
        f = puertos[0]
        s = puertos[1]
        p = puertos[2]
        PT(f,s,p)
        

def PT(f,s,p):
    
        #Esta consulta la dividiremos en 2 grupos el primero en el que obtienen los datos de serial y otros con informacion propia del cliente
        #Lista donde se almacenan los datos en conjunto
        lista = []
        total_onts = 0
        print(f"frame: {f} slot: {s} port: {p}\n")
        #consulta en ssh y el tiempo de delay
        resultado = ssh(f'interface gpon {f}/{s}\n display ont info {p} all | no-more',1.5)
        print(resultado)
        #condicionales para las busqueda y filtrado de datos
        lines = re.findall(f"{f}/ {s}/{p}.*?\n",resultado , re.DOTALL)
        
        match = re.search(f"the total of ONTs are: (\d+),", resultado)

        #Obtiene el valor total en enteros de la cantidad de ont presentes y los separa almacenandolos en total_onts
        if match:
            number_string = match.group(1)
            total_onts = int(number_string.replace(",","")) 
            

        #obtiene el numero total de ont del fsp y realiza un bucle recorriendolos todos en este caso los total_onts obtenidos
        for i in range(total_onts):

            #asigna el valor de del onu id obtenido de la consulta a su respectiva variable
            ont_id = lines[i].split()[2]
            
            """realiza un bucle en el cual empieza a leer las respuesta a partir del la linea del ultimo total_onts del primer grupo
            hasta el valor del total_onts * 2 dandose a entender que que si el total de texto en consulta es 100 en 2 grupos unidos 
            serian 50 cada grupo el primer bucle obtiene el valor del primer total y que serian 50 y el segundo grupo se estaria leyendo 
            hasta (50*2) igual a 100 dando el total de lineas"""

            for j in range(total_onts,total_onts*2):
                first_value = lines[j].split()[2]  
                # print(lines[j].split())
                if first_value == ont_id:
                    # print(lines[i].split()[2],lines[i].split()[3],lines[i].split()[4],lines[j].split()[3],lines[j].split()[4])
                    parts = lines[j].split()
                    if len(parts) >= 6:
                    
                        #Guarda los valores en una lista con sus respectivos identificadores
                            lista += [{
                        "onu_id": lines[i].split()[2],
                        "sn": lines[i].split()[3],
                        "status": lines[i].split()[4],
                        "Nombre": lines[j].split()[3],
                        "def": lines[j].split()[4],
                        "contrato": lines[j].split()[5],
                        }]
                    else:
                            #Guarda los valores en una lista con sus respectivos identificadores
                            lista += [{
                        "onu_id": lines[i].split()[2],
                        "sn": lines[i].split()[3],
                        "status": lines[i].split()[4],
                        "Nombre": lines[j].split()[3],
                        "def": lines[j].split()[4],
                        "contrato": "Error",#Esto se coloco porque me daba error ya que en ocaciones habia menos componentes en la lista en ve de 6 o mas tenia 5 porque en ocaciones
                                            #no contenia apellido y otro dato y daba error al retornar vacio
                        }]
                    
        respu = PT2(lista,f,s,p)  
        return respu

def PT2(Consulta1,f,s,p):
    
    #Aqui se almacenaran los datos juntos de ambas consultas
    lista = []
   
    #definicion de las potencias maximas que puede recibir en cada uno
    rango_potencia_ont_max = -25.00
    rango_potencia_olt_max = -30.00
    
    #se usan esta variables para definir el rango entre que lineas se comenzara a leer la respuesta y omitir la demas
    rango_lectura_respuesta_min = 57  # a partir de la linea 57
    rango_lectura_respuesta_max = -3  # todas las lineas siguiente menos las 3 ultimas

    #consulta en ssh y el tiempo de delay
    resultado = ssh(f'interface gpon {f}/{s}\n display ont optical-info {p} all | no-more',4)

    lines = resultado.split("\n")
    
    #bucle para obtener la respuesta en un rango el cual nos permitira omitir el texto basura generado en la consulta por la olt
    for line in lines[rango_lectura_respuesta_min:rango_lectura_respuesta_max]:
        #separa cada linea de la consulta
        sep = line.split()
        for i in range(len(Consulta1)):
            if sep[0] == Consulta1[i]['onu_id']:
                # compara si los valores tanto de ont como olt estan en rango
                if float(sep[1]) < rango_potencia_ont_max or float(sep[3]) < rango_potencia_olt_max:
                    

                    lista += [{
                    "onu_id": sep[0],
                    "rx_ont": sep[1],
                    "rx_olt": sep[3],
                    "sn": Consulta1[i]['sn'],
                    "Nombre": Consulta1[i]['Nombre'],
                    "status": Consulta1[i]['status'],
                    "contrato": Consulta1[i]['contrato'],
                    }]

    for i in range(len(lista)):
                  
        print(lista)            


    
