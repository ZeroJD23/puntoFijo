import tkinter as tk
from tkinter import messagebox
import sympy as sp
from fpdf import FPDF
import os

def metodo_punto_fijo(funcion_str, g_funcion_str, xi_inicial, error_absoluto_ingresado, decimales):
    x = sp.symbols('x')
    funcion = sp.sympify(funcion_str)
    g_funcion = sp.sympify(g_funcion_str)
    
    xi = round(float(xi_inicial), decimales)
    iteraciones = []
    paso = 1
    
    while True:
        xi_mas_1 = round(float(g_funcion.subs(x, xi).evalf()), decimales)  # Sustituye xi en g(x)
        error_absoluto = round(abs((xi_mas_1 - xi) / xi_mas_1) * 100, decimales)  # Calcula error absoluto
        iteraciones.append((paso, xi, xi_mas_1, error_absoluto))  # Guarda los valores en la lista
        
        if error_absoluto <= error_absoluto_ingresado:
            break  # Si el error es menor o igual al ingresado, termina el bucle
        
        xi = xi_mas_1  # Actualiza xi
        paso += 1
    
    evaluacion_final = round(float(funcion.subs(x, xi).evalf()), decimales)  # Evalúa f(x) con la última raíz
    return iteraciones, error_absoluto, evaluacion_final

def generar_pdf(iteraciones, error, evaluacion_final, funcion_str, g_funcion_str, error_absoluto_ingresado, xi_inicial):

    x = sp.symbols('x')
    g_funcion = sp.sympify(g_funcion_str)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "Metodo de Punto Fijo", ln=True, align='C') 
    pdf.cell(200, 10, "Estudiantes", ln=True, align='C')
    pdf.cell(200, 10, "Jhoan David Quiñones Lobo", ln=True, align='C')
    pdf.cell(200, 10, "Sharol Melissa Sanchez Rojas", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(200, 10, f"F(x) = {funcion_str} = 0;   Xi = {xi_inicial};   G(x) = {g_funcion_str};   Ea = {error_absoluto_ingresado};",  ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(45, 10, "Iteración", border=1)
    pdf.cell(45, 10, "xi", border=1)
    pdf.cell(45, 10, "xi+1", border=1)
    pdf.cell(45, 10, "Error a(%)",border=1)
    pdf.ln()

    pdf.set_font("Arial", style='', size=12)
    for paso, xi, xi1, error in iteraciones:

        pdf.cell(45, 10, str(paso), border=1)
        pdf.cell(45, 10, str(xi), border=1)
        pdf.cell(45, 10, str(xi1), border=1)
        pdf.cell(45, 10, str(error), border=1)
        pdf.ln()

    for paso, xi, xi1, error in iteraciones:

        gx_string = str(g_funcion).replace("x", f"({xi})") 
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, f"Iteración {paso}", ln=True, align='L')
        pdf.set_font("Arial", style='', size=12)
        pdf.cell(200, 10, f"Xi = {xi}", ln=True, align='L')
        pdf.cell(200, 10, "remplazando xi en la funcion de g(x)", ln=True, align='L')
        pdf.cell(200, 10, f"Xi+1 = {gx_string} = {xi1}", ln=True, align='L')
        pdf.cell(200, 10, "Calculamos el error absoluto", ln=True, align='L')
        pdf.cell(200, 10, f"Ea = ({xi1} - {xi} / {xi1}) x 100 = {error}", ln=True, align='L')

    pdf.set_font("Arial", style='B', size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Raiz aproximada: {iteraciones[-1][2]}", ln=True)
    pdf.cell(200, 10, f"Error absoluto calculado: {error}%", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, f"Evaluamos la Función f(x): f({iteraciones[-1][2]}) = {evaluacion_final}", ln=True)
    
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    ruta_pdf = os.path.join(carpeta_descargas, "punto_fijo_resultado.pdf")
    pdf.output(ruta_pdf)
    
    messagebox.showinfo("PDF Generado", f"El archivo ha sido guardado en:\n{ruta_pdf}")

def calcular():
    try:
        funcion_str = entrada_funcion.get()
        g_funcion_str = entrada_g_funcion.get()
        xi_inicial = float(entrada_xi.get())
        error_absoluto_ingresado = float(entrada_tolerancia.get())
        decimales = int(entrada_decimales.get())
        
        iteraciones, error, evaluacion_final = metodo_punto_fijo(funcion_str, g_funcion_str, xi_inicial, error_absoluto_ingresado, decimales)
        generar_pdf(iteraciones, error, evaluacion_final, funcion_str, g_funcion_str,error_absoluto_ingresado, xi_inicial)
    except Exception as e:
        messagebox.showerror("Error", f"Se ha producido un error: {e}")

ventana = tk.Tk()
ventana.title("Metodo de Punto Fijo")

tk.Label(ventana, text="Funcion f(x):").grid(row=0, column=0)
entrada_funcion = tk.Entry(ventana)
entrada_funcion.grid(row=0, column=1)

tk.Label(ventana, text="Funcion g(x):").grid(row=1, column=0)
entrada_g_funcion = tk.Entry(ventana)
entrada_g_funcion.grid(row=1, column=1)

tk.Label(ventana, text="Valor inicial xo:").grid(row=2, column=0)
entrada_xi = tk.Entry(ventana)
entrada_xi.grid(row=2, column=1)

tk.Label(ventana, text="Error absoluto:").grid(row=3, column=0)
entrada_tolerancia = tk.Entry(ventana)
entrada_tolerancia.grid(row=3, column=1)

tk.Label(ventana, text="Numero de decimales:").grid(row=4, column=0)
entrada_decimales = tk.Entry(ventana)
entrada_decimales.grid(row=4, column=1)

tk.Button(ventana, text="Calcular", command=calcular).grid(row=5, columnspan=2)

ventana.mainloop()
