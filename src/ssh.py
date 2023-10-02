import paramiko
from time import sleep
import re
from Constantes.config import *

puerto = PORT
host = devices[f"OLT1"]["ip"]
usuario = devices[f"OLT1"]["user"]
contrasena = devices[f"OLT1"]["pass"]
wait = 1.5

def ssh(comand,delay):
    
    ssh = paramiko.SSHClient()
    try:  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=puerto, username=usuario, password=contrasena)
        shell = ssh.invoke_shell()

        shell.send("enable\n")
        shell.send("config\n")
        shell.send("scroll 512\n")

        
        resultado = comando(shell, comand,delay)
        
    except paramiko.AuthenticationException:
        print("Error de autenticación. Verifica las credenciales.")
    except paramiko.SSHException as e:
        print("Error al establecer la conexión SSH:", str(e))
    except paramiko.BadHostKeyException as e:
        print("Error de clave del host:", str(e))
    except Exception as e:
        print("Ocurrió un error inesperado:", str(e))
    finally:
        ssh.close()
    return resultado

def enter(shell):
    shell.send("\n")
    shell.send("\n")
    sleep(wait)

def comando(shell,comando,delay):
    shell.send(comando)
    enter(shell)
    sleep(delay)
    data = ""
    chunk = shell.recv(9999).decode("latin-1")
    data += chunk
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    data = ansi_escape.sub("", data)
    return data

def close_ssh():
    ssh.close()



    

