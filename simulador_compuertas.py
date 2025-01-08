import tkinter as tk
from tkinter import messagebox

class PantallaPrincipal:
    def __init__(self, root, continuar_callback):
        self.root = root
        self.root.title("Proyecto Final Matemáticas Discretas")
        self.continuar_callback = continuar_callback

        self.frame_inicio = tk.Frame(root)
        self.frame_inicio.pack()
        root.geometry('750x500')

        tk.Label(self.frame_inicio, text="Universidad Nacional Autónoma de México", font=("Times New Roman", 16)).pack(pady=20)
        tk.Label(self.frame_inicio, text="Facultad de estudios superiores Acatlán", font=("Times New Roman", 16)).pack(pady=20)
        tk.Label(self.frame_inicio, text="Matemáticas Aplicadas y Computación", font=("Times New Roman", 16)).pack(pady=20)
        tk.Label(self.frame_inicio, text="Matemáticas Discretas", font=("Times New Roman", 16)).pack(pady=20)
        tk.Label(self.frame_inicio, text="Profesor: Christian Carlos Delgado Elizondo", font=("Times New Roman", 16)).pack(pady=20)
        tk.Label(self.frame_inicio, text="Victor de Jesus Alcantara Mendez", font=("Times New Roman", 16)).pack(pady=20)
        tk.Button(self.frame_inicio, text="Continuar", command=self.continuar_callback).pack(pady=10)

    def ocultar(self):
        self.frame_inicio.pack_forget()

class OpcionCompuerta:
    def __init__(self, root, continuar_callback):
        self.root = root
        self.continuar_callback = continuar_callback
        self.compuerta_seleccionada = None

        self.frame_opciones = tk.Frame(root)
        self.frame_opciones.pack()

        tk.Label(self.frame_opciones, text="Seleccione una compuerta lógica", font=("Arial", 16)).pack(pady=10)

        self.frame_botones = tk.Frame(self.frame_opciones)
        self.frame_botones.pack(side=tk.LEFT, padx=20)

        self.botones_compuerta = {}
        for compuerta in ["AND", "OR", "NOT", "XOR", "XNOR", "NAND"]:
            self.botones_compuerta[compuerta] = tk.Button(self.frame_botones, text=compuerta, command=lambda c=compuerta: self.seleccionar_compuerta(c))
            self.botones_compuerta[compuerta].pack(pady=5)

        self.descripcion_label = tk.Label(self.frame_opciones, text="", font=("Arial", 12), fg="blue")
        self.descripcion_label.pack(pady=10)

        self.btn_continuar = tk.Button(self.frame_opciones, text="Continuar", state="disabled", command=self.continuar_callback)
        self.btn_continuar.pack(side=tk.BOTTOM, pady=20, anchor="se")

    def seleccionar_compuerta(self, compuerta):
        self.compuerta_seleccionada = compuerta
        self.btn_continuar.config(state="normal")
        
        descripciones = {
            "AND": "La salida es 1 si todas las entradas son 1.",
            "OR": "La salida es 1 si al menos una entrada es 1.",
            "NOT": "Invierte la entrada: 0 a 1, 1 a 0.",
            "XOR": "La salida es 1 si las entradas son diferentes.",
            "XNOR": "La salida es 1 si las entradas son iguales.",
            "NAND": "La salida es 1 si no todas las entradas son 1."
        }
        self.descripcion_label.config(text=f"{compuerta}: {descripciones[compuerta]}")

    def ocultar(self):
        self.frame_opciones.pack_forget()


class SimulacionEntradas:
    def __init__(self, root, compuerta, repetir_callback, menu_principal_callback, salir_callback):
        self.root = root
        self.compuerta = compuerta
        self.repetir_callback = repetir_callback
        self.menu_principal_callback = menu_principal_callback
        self.salir_callback = salir_callback
        self.num_entradas = None

        self.frame_simulacion = tk.Frame(root)
        self.frame_simulacion.pack()

        tk.Label(self.frame_simulacion, text=f"Realizar simulación para: {compuerta}", font=("Arial", 16)).pack(pady=10)

        self.frame_botones = tk.Frame(self.frame_simulacion)
        self.frame_botones.pack()

        self.btns_variables = []
        for i, num in enumerate([2, 3, 4]):
            btn = tk.Button(self.frame_botones, text=str(num), command=lambda n=num: self.seleccionar_variables(n))
            btn.grid(row=0, column=i, padx=10)
            self.btns_variables.append(btn)

        self.frame_entradas = tk.Frame(self.frame_simulacion)
        self.frame_entradas.pack(pady=10)

        self.entradas = []
        self.resultado_label = tk.Label(self.frame_simulacion, text="Resultado: ", font=("Arial", 12))
        self.resultado_label.pack(pady=10)

        self.frame_botones_acciones = tk.Frame(self.frame_simulacion)

    def seleccionar_variables(self, num):
        self.num_entradas = num
        for btn in self.btns_variables:
            btn.config(state="disabled")

        for widget in self.frame_entradas.winfo_children():
            widget.destroy()

        self.entradas = []
        for i in range(num):
            tk.Label(self.frame_entradas, text=f"Entrada {i + 1}: ").grid(row=i, column=0, padx=5)
            entrada = tk.Entry(self.frame_entradas, width=5)
            entrada.grid(row=i, column=1, padx=5)
            self.entradas.append(entrada)

        tk.Button(self.frame_simulacion, text="Calcular", command=self.calcular_resultado).pack(pady=10)

    def calcular_resultado(self):
        try:
            valores = [self.validar_entrada(e.get()) for e in self.entradas]
            resultado = self.operar(valores)
            self.resultado_label.config(text=f"Resultado: {resultado}")
            self.bloquear_entradas()
            self.mostrar_botones_acciones()
        except ValueError as e:
            self.resultado_label.config(text=str(e))

    def operar(self, valores):
        if self.compuerta == "AND":
            return int(all(valores))
        elif self.compuerta == "OR":
            return int(any(valores))
        elif self.compuerta == "NOT":
            return int(not valores[0])
        elif self.compuerta == "XOR":
            return int(sum(valores) % 2)
        elif self.compuerta == "XNOR":
            return int(all(v == valores[0] for v in valores))
        elif self.compuerta == "NAND":
            return int(not all(valores))

    def validar_entrada(self, entrada):
        if entrada not in ("0", "1"):
            raise ValueError("Por favor, escoja valores válidos (1 y/o 0).")
        return int(entrada)

    def bloquear_entradas(self):
        for entrada in self.entradas:
            entrada.config(state="disabled")

    def mostrar_botones_acciones(self):
        for widget in self.frame_botones_acciones.winfo_children():
            widget.destroy()

        self.frame_botones_acciones.pack()

        tk.Button(self.frame_botones_acciones, text="Repetir", command=self.repetir_callback).pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame_botones_acciones, text="Menú Principal", command=self.menu_principal_callback).pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame_botones_acciones, text="Salir", command=self.salir_callback).pack(side=tk.LEFT, padx=10)

    def ocultar(self):
        self.frame_simulacion.pack_forget()

class SimuladorCompuertas:
    def __init__(self, root):
        self.root = root

        self.pantalla_principal = PantallaPrincipal(root, self.mostrar_opciones_compuerta)
        self.opcion_compuerta = None
        self.simulacion = None

    def mostrar_opciones_compuerta(self):
        if self.simulacion:
            self.simulacion.ocultar()
        if self.pantalla_principal:
            self.pantalla_principal.ocultar()
        self.opcion_compuerta = OpcionCompuerta(self.root, self.mostrar_simulacion)

    def mostrar_simulacion(self):
        if self.opcion_compuerta:
            self.opcion_compuerta.ocultar()
            compuerta = self.opcion_compuerta.compuerta_seleccionada
            self.simulacion = SimulacionEntradas(
                self.root, compuerta, self.reiniciar_simulacion, self.mostrar_opciones_compuerta, self.salir_programa
            )

    def reiniciar_simulacion(self):
        if self.simulacion:
            compuerta = self.simulacion.compuerta
            self.simulacion.ocultar()
            self.simulacion = SimulacionEntradas(
                self.root, compuerta, self.reiniciar_simulacion, self.mostrar_opciones_compuerta, self.salir_programa
            )

    def salir_programa(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorCompuertas(root)
    root.mainloop()

