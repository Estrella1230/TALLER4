import tkinter as tk
from tkinter import ttk
import ply.lex as lex

tokens = (
    'RESERVADO',
    'IDENTIFICADOR',
    'OPERADOR',
    'NUMERO_ENTERO',
    'PUNTO',
    'FINAL',
    'DELIMITADOR',
    'NODEFINIDO'
)

palabra_reservada = ['static', 'void', 'for', 'int']
identificador = ['burbuja', 'arreglo']
operador = ['=', '+', '-', '*', '/']
delimitador = ['(', ')', '{', '}', ';', ',', '.']

t_ignore = ' \t'

contadores = {token: 0 for token in tokens}
tokens_encontrados = set()

def t_IDENTIFICADOR(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = 'IDENTIFICADOR'
    if t.value in palabra_reservada:
        t.type = 'RESERVADO'
    elif t.value in identificador:
        t.type = 'IDENTIFICADOR'
    else:
        t.type = 'NODEFINIDO'
    if t.value not in tokens_encontrados:
        contadores[t.type] += 1
        tokens_encontrados.add(t.value)
    return t

def t_OPERADOR(t):
    r'[-+*/=]'
    t.type = 'OPERADOR'
    if t.value not in tokens_encontrados:
        contadores[t.type] += 1
        tokens_encontrados.add(t.value)
    return t

def t_NUMERO_ENTERO(t):
    r'\d+'
    t.type = 'NUMERO_ENTERO'
    if t.value not in tokens_encontrados:
        contadores[t.type] += 1
        tokens_encontrados.add(t.value)
    return t

def t_PUNTO(t):
    r'\.'
    t.type = 'PUNTO'
    if t.value not in tokens_encontrados:
        contadores[t.type] += 1
        tokens_encontrados.add(t.value)
    return t

def t_FINAL(t):
    r';'
    t.type = 'FINAL'
    if t.value not in tokens_encontrados:
        contadores[t.type] += 1
        tokens_encontrados.add(t.value)
    return t

def t_DELIMITADOR(t):
    r'[\(\)\{\},]'
    t.type = 'DELIMITADOR'
    if t.value not in tokens_encontrados:
        contadores[t.type] += 1
        tokens_encontrados.add(t.value)
    return t

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()

def analizar_codigo():
    codigo = entrada_texto.get('1.0', tk.END)
    lexer.input(codigo)
    tokens = []
    lexemas = []
    lineas = []

    for tok in lexer:
        tokens.append(tok.type)
        lexemas.append(tok.value)
        lineas.append(tok.lineno)

    resultado_texto.delete(*resultado_texto.get_children())

    for token, lexema, linea in zip(tokens, lexemas, lineas):
        resultado_texto.insert("", tk.END, values=(token, lexema, linea))

    # Actualizar la tabla de totales
    total_tokens_label.config(text=f"Total de Tokens: {sum(contadores.values())}\n" +
                                  f"Total de RESERVADO: {contadores['RESERVADO']}\n" +
                                  f"Total de IDENTIFICADOR: {contadores['IDENTIFICADOR']}\n" +
                                  f"Total de OPERADOR: {contadores['OPERADOR']}\n" +
                                  f"Total de NUMERO_ENTERO: {contadores['NUMERO_ENTERO']}\n" +
                                  f"Total de PUNTO: {contadores['PUNTO']}\n" +
                                  f"Total de FINAL: {contadores['FINAL']}\n" +
                                  f"Total de DELIMITADOR: {contadores['DELIMITADOR']}\n" +
                                  f"Total de NODEFINIDO: {contadores['NODEFINIDO']}")

def borrar_codigo():
    entrada_texto.delete('1.0', tk.END)

ventana = tk.Tk()
ventana.title("Analizador de Código")

# Crear el marco principal
marco_principal = ttk.Frame(ventana)
marco_principal.grid(row=0, column=0, sticky="nsew")
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_rowconfigure(0, weight=1)
# Etiqueta y botón de borrado
etiqueta_codigo = ttk.Label(marco_principal, text="Ingrese el código a analizar:")
etiqueta_codigo.grid(row=0, column=0, sticky="w", padx=5, pady=5)
boton_borrar = ttk.Button(marco_principal, text="Borrar", command=borrar_codigo)
boton_borrar.grid(row=0, column=1, sticky="e", padx=5, pady=5)

# Área de entrada de texto
entrada_texto = tk.Text(marco_principal, height=10, width=50)
entrada_texto.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Botón de análisis
boton_analizar = ttk.Button(marco_principal, text="Analizar", command=analizar_codigo)
boton_analizar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

# Crear el marco para la tabla de tokens
marco_tokens = ttk.Frame(ventana)
marco_tokens.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
ventana.grid_columnconfigure(1, weight=1)

# Tabla de tokens
resultado_texto = ttk.Treeview(marco_tokens, columns=("Token", "Lexema", "Línea"))
resultado_texto.heading("Token", text="Token")
resultado_texto.heading("Lexema", text="Lexema")
resultado_texto.heading("Línea", text="Línea")
resultado_texto.grid(row=0, column=0, sticky="nsew")

# Crear el marco para la tabla de totales
marco_totales = ttk.Frame(marco_tokens)
marco_totales.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
marco_tokens.grid_columnconfigure(1, weight=1)

# Etiqueta para el recuento de tokens
total_tokens_label = ttk.Label(marco_totales, text="")
total_tokens_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

ventana.mainloop()