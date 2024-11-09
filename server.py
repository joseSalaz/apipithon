import paramiko
from flask import Flask, send_file
import os

app = Flask(__name__)

# Configuración SSH
hostname = 'ssh-natureza.alwaysdata.net'
port = 22
username = 'natureza_anon'
password = '(123456)'

# Ruta donde se guardará el archivo localmente en el sistema Windows
archivo_local = 'e:/chamba/JSalazar.xlsx'  # Cambiar la ruta aquí

# Ruta del archivo en el servidor remoto
archivo_remoto = 'JSalazar.xlsx'

def descargar_archivo_remoto():
    # Conexión SSH para descargar el archivo
    try:
        # Crear el cliente SSH
        client = paramiko.SSHClient()

        # Cargar las claves del sistema
        client.load_system_host_keys()

        # Auto-aceptar claves de hosts desconocidos
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar al servidor SSH
        client.connect(hostname, username=username, password=password, port=port)

        # Crear el cliente SFTP para la transferencia de archivos
        sftp = client.open_sftp()

        # Descargar el archivo desde el servidor remoto
        sftp.get(archivo_remoto, archivo_local)
        print(f'Archivo {archivo_remoto} descargado correctamente.')

        # Cerrar la conexión SFTP y SSH
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error al conectar o descargar el archivo: {e}")

@app.route('/descargar')
def descargar():
    # Descargar el archivo desde el servidor remoto
    descargar_archivo_remoto()

    # Retornar el archivo descargado para que se pueda descargar via HTTP
    return send_file(archivo_local, as_attachment=True)

if __name__ == '__main__':
    # Iniciar el servidor HTTP en el puerto 5000
    app.run(debug=True, port=5000)
