from src.ssh import ssh
import re
from time import sleep


def PT():
    lista1 = []
    lista2 = []
    contador = 0
    comparador = "-----------------------------------------------------------------------------"
    resultado = ssh('interface gpon 0/2\n display ont info 4 all | no-more',1.5)

    SEPARADO = resultado.split("\r\n ")
    for line in SEPARADO[:-1]:
        if comparador in line:
            contador += 1  
        if contador == 9:
            lista1.append(line)
    
        if contador == 11:
            lista2.append(line)
       
    def decodificar(lista1):
            
        
        for i in range(len(lista1)):
            lista1[i] = lista1[i].strip()

        if lista1[0] == comparador:
            lista1.pop(0)

        return lista1
            

    respuesta = decodificar(lista1) 
    PT2(respuesta)
    
def PT2(lista1):
    #Rango de lineas donde se define desde que line en la respuesta se tomara y hasta donde
    linea_min = 57
    linea_max = -3
    lista = []
    resultado = ssh('interface gpon 0/2\n display ont optical-info 4 all | no-more',4)
    
    lines = resultado.split("\n")
    for line in lines[linea_min:linea_max]:
        lista.append(line)

    

def Unir(lista1,lista2):
    print("Hola")