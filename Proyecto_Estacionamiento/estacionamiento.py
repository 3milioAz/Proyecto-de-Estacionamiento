import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

import random
import string
import datetime

import sqlite3

# Inicializamos la base de datos
con = sqlite3.connect('tickets.db') # connect (crea el archivo si no existe)
cur = con.cursor()

# Crea la tabla si no existe
cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (codigo TEXT PRIMARY KEY, fecha_hora TEXT)
""")

con.commit()
con.close()


costo_total = 0.0

ticket_actual_pagando = None


def generar_ticket():
    boton_generar.config(state=tk.DISABLED) # Desactiva el botón una vez usado
    
    codigo = generar_codigo()
    hora_entrada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Usando la funcion datetime.now devuelve la hora actual, y .strftime vuelve la hora en datetime en texto para poderla guardar en la base de datos
    
    guardar_ticket_en_db(codigo, hora_entrada)

    texto_mostrado = f"Ticket generado:\n-Código: {codigo}\n-Hora: {hora_entrada}" # Crea un texto que le dice al usuario que su ticket fue creado y le da informacion
    ticket_generado_var.set(texto_mostrado) # Guarda el texto en la label para mostrarlo en pantalla

def generar_codigo():
    letras = string.ascii_uppercase # Esta constante contiene todas las letras mayusculas (ABC..YZ)
    numeros = string.digits # Esta constante contiene todos los digitos (012...89)
    codigo = ''.join(random.choices(letras + numeros, k=8)) # Random choices de la combinacion (letras + numeros) elige k elementos y ''.join() los une en una cadena
    return codigo

def guardar_ticket_en_db(codigo, fecha_hora):
    con = sqlite3.connect('tickets.db')
    cur = con.cursor()
    cur.execute("""
        INSERT INTO tickets VALUES (?, ?)
    """, (codigo, fecha_hora))
    con.commit()
    con.close()

def consultar_ticket():
    codigo = ticket_var.get().strip() # .get() obtiene el codigo ingresado con el usuario, y .strip() elimina todo espacio que el usuario haya dejado por error al inicio o al final del codigo
    if not codigo:
        respuesta_consulta_var.set("Por favor ingrese el código de su ticket.") # .set() cambia el texto de respues....._var para que en el label aparezca el mensaje "Porfavor ingrese...."
        return

    con = sqlite3.connect('tickets.db')
    cur = con.cursor()

    cur.execute("SELECT fecha_hora FROM tickets WHERE codigo = ?", (codigo,))
    fila = cur.fetchone() # Regresa el primer registro que cumplia con las reglas seleccionadas
    con.close()

    if fila:
        hora_entrada_str = fila[0] # fila[0] nos devuelve el valor de la hora que corresponde al codigo consultado
        hora_entrada = datetime.datetime.strptime(hora_entrada_str, "%Y-%m-%d %H:%M:%S")  # .strptime() convierte la hora de la base de datos de string a datetime para poder ser usada para calcular el tiempo transcurrido
        
        hora_salida = datetime.datetime.now() 
        
        hora_simulada_str = hora_simulada_var.get().strip()

        if hora_simulada_str: # Usa la hora simulada ingresada a menos que no cumpla el formato especifico
            try:
                hora_salida = datetime.datetime.strptime(hora_simulada_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                respuesta_consulta_var.set("Formato de hora inválido. Use AAAA-MM-DD HH:MM:SS")
                return
        else:
            hora_salida = datetime.datetime.now() # .now() nos devuelve la hora actual

        diferencia = hora_salida - hora_entrada # Calculamos la diferencia de tiempo entre la hora de entrada y la actual
        minutos = diferencia.total_seconds() / 60 # Con .total_seconds() convertimos la diferencia de tiempo en segundos y despues la convertimos a minutos 
        
        costo = (minutos // 30) * 21  # Aqui establecemos el costo del estacionamiento por minuto

        global costo_total, ticket_actual_pagando # Aqui guardamos el costo y el codigo que se va a pagar en una variable global
        costo_total = costo
        ticket_actual_pagando = codigo

        texto = (
            f"Consulta del ticket:\n- Código: {codigo}\n- Hora entrada: {hora_entrada_str}\n- Hora salida/actual: {hora_salida.strftime('%Y-%m-%d %H:%M:%S')}\n- Tiempo total: {minutos:.1f} min\n- Monto a pagar: ${costo:.2f}"
        )
    else:
        texto = "No se encontró ningún ticket con ese código."

    respuesta_consulta_var.set(texto) # Con esto establecemos la variable con el resultado obtenido (si es que se encuentra o no)


def realizar_pago():
    global costo_total
    global ticket_actual_pagando

    try:
        n50 = int(billetes_50_var.get())
        n20 = int(billetes_20_var.get())
        n10 = int(monedas_10_var.get())
        n5 = int(monedas_5_var.get())
        n2 = int(monedas_2_var.get())
    except ValueError:
        resultado_pago_var.set("Todas las cantidades deben ser números enteros.")
        return

    # Calcular total entregado multiplicando las cantidades por los montos
    total_entregado = (n50 * 50) + (n20 * 20) + (n10 * 10) + (n5 * 5) + (n2 * 2)

    if total_entregado < costo_total:
        faltante = costo_total - total_entregado
        resultado_pago_var.set(f"❌ Monto insuficiente. Faltan ${faltante:.2f}.")
    else:
        cambio = total_entregado - costo_total

        con = sqlite3.connect('tickets.db')
        cur = con.cursor()
        cur.execute("DELETE FROM tickets WHERE codigo = ?", (ticket_actual_pagando,))
        con.commit()
        con.close()

        resultado_pago_var.set(f"✅ Pago exitoso. Su cambio es: ${cambio:.2f}.")

        ticket_actual_pagando = None # Se hace esto para limpiar la variable y evitar poder volver a pagar el mismo ticket

def cargar_tickets():
    boton_ver_tickets.config(state=tk.DISABLED)

    con = sqlite3.connect('tickets.db')
    cur = con.cursor()

    cur.execute("SELECT codigo, fecha_hora FROM tickets ORDER BY fecha_hora")
    filas = cur.fetchall() # .fetchall() nos regresa todos los registros encontrados en el cur
    con.close() 

    if not filas:
        lista_tickets_text.insert(tk.END, "No hay tickets registrados.\n")
        return

    for fila in filas:
        codigo, fecha_hora = fila
        lista_tickets_text.insert(tk.END, f"🪪 Código: {codigo} | Fecha y hora: {fecha_hora}\n")




window = ttk.Window(themename="estacionamiento")

window.title('Estacionamiento Barato') # Le agrega un nombre a la ventana
window.geometry('1000x1400+100+100')
window.resizable(True, True)


# 1.----------------------------Generación de Boletos------------------------------------
# Boton para imprimir nuevo boleto
# Registra hora de entrada y genera un codigo unico
# Guardar el registro en memoria o en archivo.
# (Extra) Generar el boleto como un archivo PDF.

label_bienvenida = tk.Label(
    window,
    text="Bienvenid@ al mejor estacionamiento de Dubai",
    font=("Arial", 11, "bold"),
    justify="center",
    anchor="nw"
)
label_bienvenida.pack(pady=15)

boton_generar = ttk.Button(window,
                   text="🎫 Generar Ticket",
                   command=generar_ticket,
                   bootstyle="success-outline",
                   width=20,
                   padding=10)
boton_generar.pack(pady=10)

ticket_generado_var = tk.StringVar()
ticket_generado_label = tk.Label(
    window,
    textvariable=ticket_generado_var,
    justify="center",
    anchor="nw",
    wraplength=400
)
ticket_generado_label.pack(pady=2)

# 2.----------------------------Consulta de Boletos-------------------------------------------------
# Sección para ingresar el código del boleto.
# Mostrar:
#     - Hora de entrada
#     - Hora de salida (puede tomarse como la hora actual o la simulada)
#     - Tiempo total de estacionamiento
#     - Cálculo del monto a pagar.

label_descripcion = tk.Label(
    window,
    text = 'Codigo del Ticket:',
    font=("Arial", 9, "bold"),
    justify = "center",
    anchor="nw",
    wraplength=400,
    )
label_descripcion.pack()

ticket_var = tk.StringVar(value='')
ticket_entry = tk.Entry(textvariable=ticket_var)
ticket_entry.pack()

boton_consultar = ttk.Button(
    window,
    text="🔍 Consultar Ticket",
    command=consultar_ticket,
    bootstyle="info-outline"
)
boton_consultar.pack(pady=10)

respuesta_consulta_var = tk.StringVar()
respuesta_consulta_label = tk.Label(
    window,
    textvariable=respuesta_consulta_var,
    justify="center",
    anchor="nw",
    wraplength=500
)
respuesta_consulta_label.pack(pady=10)



# 3.---------------------------Simulación de Tiempo------------------------------------------------
# Permitir modificar la hora actual para pruebas o simulación del paso del tiempo.

label_hora_simulada = tk.Label(
    window,
    text="(Opcional) Hora simulada (AAAA-MM-DD HH:MM:SS):",
    font=("Arial", 9, "bold"),
    justify="center",
    anchor="nw",
    wraplength=400
)
label_hora_simulada.pack(pady=2)

hora_simulada_var = tk.StringVar()
hora_simulada_entry = tk.Entry(window, textvariable=hora_simulada_var)
hora_simulada_entry.pack(pady=10)



# 4.------------------------------Gestión de Pago------------------------------------------------
# Ingreso del monto pagado (número de billetes y monedas).
# Calcular y mostrar el cambio.
# Validar que el monto pagado sea suficiente.

label_pago = tk.Label(
    window,
    text="Si ya ingreso el codigo de su boleto correctamente y desea pagarlo.\nIngrese la cantidad de billetes y monedas:",
    font=("Arial", 9, "bold"),
    justify="center",
    anchor="nw"
)
label_pago.pack(pady=5)

frame_dinero = tk.Frame(window)
frame_dinero.pack(pady=5)


billetes_50_var = tk.StringVar(value="0")
tk.Label(frame_dinero, text="$50:", font=("Arial", 9, "bold")).grid(row=0, column=0)
tk.Entry(frame_dinero, textvariable=billetes_50_var, width=5).grid(row=0, column=1)

billetes_20_var = tk.StringVar(value="0")
tk.Label(frame_dinero, text="$20:", font=("Arial", 9, "bold")).grid(row=0, column=2)
tk.Entry(frame_dinero, textvariable=billetes_20_var, width=5).grid(row=0, column=3)

monedas_10_var = tk.StringVar(value="0")
tk.Label(frame_dinero, text="$10:", font=("Arial", 9, "bold")).grid(row=1, column=0)
tk.Entry(frame_dinero, textvariable=monedas_10_var, width=5).grid(row=1, column=1)

monedas_5_var = tk.StringVar(value="0")
tk.Label(frame_dinero, text="$5:", font=("Arial", 9, "bold")).grid(row=1, column=2)
tk.Entry(frame_dinero, textvariable=monedas_5_var, width=5).grid(row=1, column=3)

monedas_2_var = tk.StringVar(value="0")
tk.Label(frame_dinero, text="$2:", font=("Arial", 9, "bold")).grid(row=2, column=0)
tk.Entry(frame_dinero, textvariable=monedas_2_var, width=5).grid(row=2, column=1)

monedas_1_var = tk.StringVar(value="0")
tk.Label(frame_dinero, text="$1:", font=("Arial", 9, "bold")).grid(row=2, column=2)
tk.Entry(frame_dinero, textvariable=monedas_1_var, width=5).grid(row=2, column=3)

boton_pagar = ttk.Button(
    window,
    text="💰 Pagar",
    command=realizar_pago,
    bootstyle="warning-outline"
)
boton_pagar.pack(pady=5)

resultado_pago_var = tk.StringVar()
resultado_pago_label = tk.Label(
    window,
    textvariable=resultado_pago_var,
    justify="center",
    anchor="nw",
    wraplength=600
)
resultado_pago_label.pack(pady=10)



# 5.---------------------------Persistencia de Datos------------------------------------------------
# Los boletos emitidos deben almacenarse (texto o SQLite).
# Al reiniciar el programa debe cargar los boletos emitidos.

label_lista_tickets = tk.Label(
    window,
    text="📜 Lista de tickets registrados:",
    font=("Arial", 9, "bold"),
    justify="center",
    anchor="nw"
)
label_lista_tickets.pack(pady=5)

lista_tickets_text = tk.Text(window, height=7, width=60)
lista_tickets_text.pack(pady=5)

boton_ver_tickets = ttk.Button(
    window,
    text="📜 Ver todos los tickets",
    command=cargar_tickets,
    bootstyle="secondary-outline"
)
boton_ver_tickets.pack(pady=10)


#-------------------------------Cosas Extra-------------------------li----
# Que tambien el codigo sea uno de barras
# Traer un lector de codigo de barras
# Impresora termica para el boleto
# Interfaz de carritos estacionados y decirle donde estacionar


window.mainloop()