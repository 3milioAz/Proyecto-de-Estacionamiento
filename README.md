## 📸 Interfaz del Proyecto

[Captura de la Interfaz](imagenes/interfaz.png)

## 💻 Uso de entorno virtual (opcional)

Se recomienda usar un entorno virtual de Python (venv) para no instalar las librerias necesarias para el proyecto en tu python principal y provocar problemas mas tarde.  

### Crear un entorno virtual

- En tu terminal o cmd deberas escribir las siguientes instrucciones de acuerdo a tu sistema operativo

En Windows:
```
python -m venv venv
```
En macOS / Linux:
```
python3 -m venv venv
```
### Activar el entorno virtual

En Windows:
```
venv\Scripts\activate
```
En macOS / Linux:
```
source venv/bin/activate
```
## 📦 Archivo requirements.txt

Este proyecto incluye un archivo `requirements.txt` con las librerias necesarias. 

### Instalar librerias necesarias

- Con el entorno virtual ya activado deberas escribir en tu terminal:
```
pip install -r requirements.txt
```
- Y ya con eso tienes todo para poder ejecutar el archivo principal.

## 👨‍🏫 Manual de Uso

- Primero vamos a abrir el archivo principal llamado: `estacionamiento.py`
- Ya abierto el archivo se nos abrira una interfaz que nos dara acceso a las siguientes funciones
- Pulsar el boton **"🎫 Generar Ticket"** creara tu nuevo ticket de estacionamiento con un codigo unico.
- Copia el código generado.
- Ingresa el código previamente copiado en la sección debajo del texto **Codigo del Ticket** y oprime el boton **🔍 Consultar Ticket** para ver los datos de tu estancia y calcular el monto a pagar.
- Usa la **hora simulada** para pruebas de tiempo (si requieres saber cuanto pagaras en una hora determinada). Solo necesitas ingresar primero la hora que se busca simular (en el formato que ahi aparece) y volver a dar click en el boton **🔍 Consultar Ticket**.
- Ingresa la cantidad de billetes y monedas que vayas a entregar en la seccion donde aparecen los diferentes montos, y posteriormente da click en el boton **💰 Pagar** para poder pagar tu ticket.
- Da click en el boton  **📜 Ver todos los tickets** para poder observar en la parte de arriba todos los boletos genrados hasta ese momento en la base de datos (los pagados no apareceran ya que son borrados inmediatamente al ser solventados).

## ⚙️ Base de datos

El sistema usa **SQLite** para guardar los tickets (especificamente sqlite3). El archivo `tickets.db` se crea automáticamente en la carpeta del proyecto o en el area de trabajo donde se este trabajando en ese momento.

## 👤 Autor

- Nombre: Emilio Azael Valencia Lopez
- Contacto: ux24ii161@ux.edu.mx
