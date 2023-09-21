from src.ssh import ssh
import re
from time import sleep


def PT():
    listado_unido = {}
    
    resultado = ssh('interface gpon 0/2\n display ont info 4 all | no-more',1.5)

    lines = re.findall(r"0/ 2/4.*?\n", resultado, re.DOTALL)

    for line in lines[:-1]:
        newline = line.replace("/"," ",2).split()
        # print(newline)
        print(newline)
    PT2()
def PT2():

    resultado = ssh('interface gpon 0/2\n display ont optical-info 4 all | no-more',4)
    
    lines = resultado.split("\n")
    for line in lines[57:-3]:
        print(line.split())

def Unir():
    print("Hola")