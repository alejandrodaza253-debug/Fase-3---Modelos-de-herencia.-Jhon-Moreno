import tkinter as tk
from tkinter import messagebox

class Dispositivo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = False

    def encender(self):
        self.estado = True
        return f"{self.nombre} is ON"

    def apagar(self):
        self.estado = False
        return f"{self.nombre} is OFF"

    def status(self):
        estado = "ON" if self.estado else "OFF"
        return f"{self.nombre}: {estado}"

    def configurar(self, *args):
        if len(args) == 1:
            return f"{self.nombre} configured in {args[0]} mode"
        elif len(args) == 2:
            return f"{self.nombre} mode: {args[0]}, intensity: {args[1]}"
        elif len(args) == 3:
            return f"{self.nombre} mode: {args[0]}, intensity: {args[1]}, time: {args[2]}"
        else:
            return f"{self.nombre} default configuration"


class BombillaInteligente(Dispositivo):
    def status(self):
        estado = "ON" if self.estado else "OFF"
        return f"{self.nombre} (Light): {estado}"


class CortinaInteligente(Dispositivo):
    def status(self):
        estado = "OPEN" if self.estado else "CLOSED"
        return f"{self.nombre} (Curtain): {estado}"


class TermostatoInteligente(Dispositivo):
    def status(self):
        estado = "ON" if self.estado else "OFF"
        return f"{self.nombre} (Thermostat): {estado}"


class ControlCentral:
    def __init__(self):
        self.dispositivos = []

    def agregar(self, dispositivo):
        self.dispositivos.append(dispositivo)

    def encender_todos(self):
        return [d.encender() for d in self.dispositivos]

    def apagar_todos(self):
        return [d.apagar() for d in self.dispositivos]

    def estado_general(self):
        return [(d.status(), d.estado) for d in self.dispositivos]

    def configurar_dispositivo(self, index, *args):
        return self.dispositivos[index].configurar(*args)


control = ControlCentral()

control.agregar(BombillaInteligente("Living Room Light"))
control.agregar(CortinaInteligente("Bedroom Curtain"))
control.agregar(TermostatoInteligente("Main Thermostat"))

root = tk.Tk()
root.title("Smart Home Control Panel")
root.geometry("550x580")
root.configure(bg="#1e1e2f")

title = tk.Label(root, text="SMART HOME CONTROL", fg="white", bg="#1e1e2f", font=("Arial", 16, "bold"))
title.pack(pady=10)

output = tk.Text(root, height=12, width=60, bg="#2e2e3f", fg="white")
output.pack(pady=10)

listbox = tk.Listbox(root, height=5, bg="#2e2e3f", fg="white")
for d in control.dispositivos:
    listbox.insert(tk.END, d.nombre)
listbox.pack(pady=10)

def mostrar_estados(estados):
    output.delete(1.0, tk.END)
    for texto, estado in estados:
        if estado:
            output.insert(tk.END, texto + "\n", "on")
        else:
            output.insert(tk.END, texto + "\n", "off")

output.tag_config("on", foreground="lightgreen")
output.tag_config("off", foreground="red")

def encender():
    control.encender_todos()
    mostrar_estados(control.estado_general())

def apagar():
    control.apagar_todos()
    mostrar_estados(control.estado_general())

def estado():
    mostrar_estados(control.estado_general())

def encender_individual():
    seleccion = listbox.curselection()
    if not seleccion:
        messagebox.showwarning("Warning", "Select a device")
        return
    control.dispositivos[seleccion[0]].encender()
    mostrar_estados(control.estado_general())

def apagar_individual():
    seleccion = listbox.curselection()
    if not seleccion:
        messagebox.showwarning("Warning", "Select a device")
        return
    control.dispositivos[seleccion[0]].apagar()
    mostrar_estados(control.estado_general())

def configurar():
    seleccion = listbox.curselection()
    if not seleccion:
        messagebox.showwarning("Warning", "Select a device")
        return
    resultado = control.configurar_dispositivo(seleccion[0], "Auto", 70, "08:00 PM")
    messagebox.showinfo("Configuration", resultado)

frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=10)

tk.Button(frame, text="Turn ON All", bg="green", fg="white", width=15, command=encender).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Turn OFF All", bg="red", fg="white", width=15, command=apagar).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Show Status", bg="blue", fg="white", width=15, command=estado).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame, text="Configure Device", bg="orange", fg="black", width=15, command=configurar).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Turn ON Selected", bg="darkgreen", fg="white", width=15, command=encender_individual).grid(row=2, column=0, padx=5, pady=5)
tk.Button(frame, text="Turn OFF Selected", bg="darkred", fg="white", width=15, command=apagar_individual).grid(row=2, column=1, padx=5, pady=5)

root.mainloop()

# El programa desarrollado corresponde a un sistema de control de dispositivos inteligentes implementado en Python utilizando la biblioteca Tkinter para la interfaz gráfica. 
# Se diseñó aplicando los principios de la programación orientada a objetos, mediante una clase base llamada Dispositivo, de la cual heredan las clases BombillaInteligente, CortinaInteligente y TermostatoInteligente,
# permitiendo así la reutilización del código y la escalabilidad del sistema. Cada dispositivo puede encenderse, apagarse y mostrar su estado, haciendo uso del polimorfismo para que, aunque se utilicen los mismos métodos,
# cada uno responda de manera diferente. Además, se implementó una simulación de sobrecarga en el método configurar() mediante el uso de argumentos variables. La clase ControlCentral se encarga de gestionar todos los dispositivos,
# permitiendo acciones tanto globales como individuales. Finalmente, la interfaz gráfica facilita la interacción del usuario mediante botones y visualización de estados, destacando en colores verde y rojo los dispositivos encendidos y apagados respectivamente.
