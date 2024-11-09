import pandas as pd
import io
import paramiko

def generar_reporte_excel():
    datos = {
        'ID': [1, 2, 3],
        'Nombre': ['Producto A', 'Producto B', 'Producto C'],
        'Precio': [10.5, 20.75, 30.0]
    }
    df = pd.DataFrame(datos)
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    print("Archivo Excel generado en memoria.")
    return excel_buffer

def crear_directorio_recursivo(sftp, path):
    directories = path.split("/")
    current_path = ""
    for directory in directories:
        if directory:
            current_path += f"/{directory}"
            try:
                sftp.mkdir(current_path)
                print(f"Directorio {current_path} creado.")
            except IOError:
                print(f"El directorio {current_path} ya existe.")

def subir_archivo_ssh(buffer, ruta_remota, host, username, password):
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cliente.connect(hostname=host, username=username, password=password, timeout=30)
    sftp = cliente.open_sftp()

    directorio = '/'.join(ruta_remota.split('/')[:-1])
    crear_directorio_recursivo(sftp, directorio)

    # Cambia aquí la ruta si es necesario después de verificar
    ruta_remota_verificada = "/home/natureza_anon/2221915/repo.xlsx"
    print(f"Intentando subir a la ruta: {ruta_remota_verificada}")
    
    # Intenta la subida del archivo
    sftp.putfo(buffer, ruta_remota_verificada)
    sftp.close()
    cliente.close()
    print("Archivo subido exitosamente al servidor.")

# Configuración de SSH
host = "ssh-natureza.alwaysdata.net"
username = "natureza_anon"
password = "(123456)"
ruta_remota = "/home/natureza_anon/2221915/repo.xlsx"

buffer = generar_reporte_excel()
subir_archivo_ssh(buffer, ruta_remota, host, username, password)
