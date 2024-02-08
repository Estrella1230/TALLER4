import ply.lex as lex
import tkinter as tk

tokens = (
    'RESERVADO',
    'IDENTIFICADOR',
    'OPERADOR',
    'NUMERO_ENTERO',
    'NUMERO_DECIMAL',
    'PUNTO',
    'FINAL',
    'DELIMITADOR',
    'NODEFINIDO'
)

palabra_reservada = ['static', 'void', 'int', 'public']
identificador = ['main', 'n']
delimitador = ['(', ')', '{', '}']

t_ignore = ' \t'

def t_IDENTIFICADOR(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value in palabra_reservada:
        t.type = 'RESERVADO'
    elif t.value in identificador:
        t.type = 'IDENTIFICADOR'
    else:
        t.type = 'NODEFINIDO'
    return t

def t_DELIMITADOR(t):
    r'[\(\)\{\}]'
    t.type = 'DELIMITADOR'
    return t 

def t_OPERADOR(t):
    r'='
    t.type = 'OPERADOR'
    return t 

def t_NUMERO_DECIMAL(t):
    r'\d+\.\d+'
    t.type = 'NUMERO_DECIMAL'
    return t

def t_NUMERO_ENTERO(t):
    r'\d+'
    t.type = 'NUMERO_ENTERO'
    return t

def t_PUNTO(t):
    r'\.'
    t.type = 'PUNTO'
    return t

def t_FINAL(t):
    r';'
    t.type = 'FINAL'
    return t

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

lexer = lex.lex()

def analizar_codigo():
    codigo = entrada_texto.get('1.0', tk.END)
    lexer.input(codigo)
    tokens = []
    lexemas = []
    lineas = []
    
    palabra_actual = ""
    for char in codigo:
        if char.isalnum() or char == '_':
            palabra_actual += char
        else:
            if palabra_actual:
                lexer.input(palabra_actual)
                tok = lexer.token()
                if tok:
                    tokens.append(tok.type)
                    lexemas.append(tok.value)
                    lineas.append(lexer.lineno)
                palabra_actual = ""
            
            if char.strip():  # Si no es un espacio en blanco
                lexer.input(char)
                tok = lexer.token()
                if tok:
                    tokens.append(tok.type)
                    lexemas.append(tok.value)
                    lineas.append(lexer.lineno)
    
    # Limpiar resultados anteriores
    resultado_texto.delete('1.0', tk.END)
    
    # Mostrar resultados en la interfaz de usuario con colores
    for token, lexema, linea in zip(tokens, lexemas, lineas):
        resultado_texto.insert(tk.END, f"Token: {token}, Lexema: {lexema}, Linea: {linea}\n")
        if token == 'RESERVADO':
            resultado_texto.tag_add('reservado', f"{resultado_texto.index(tk.END)}-12c", tk.END)
        elif token == 'IDENTIFICADOR':
            resultado_texto.tag_add('identificador', f"{resultado_texto.index(tk.END)}-12c", tk.END)
        elif token == 'OPERADOR':
            resultado_texto.tag_add('operador', f"{resultado_texto.index(tk.END)}-12c", tk.END)
        elif token == 'NUMERO_ENTERO' or token == 'NUMERO_DECIMAL':
            resultado_texto.tag_add('numero', f"{resultado_texto.index(tk.END)}-12c", tk.END)
        elif token == 'PUNTO':
            resultado_texto.tag_add('punto', f"{resultado_texto.index(tk.END)}-12c", tk.END)
        elif token == 'FINAL':
            resultado_texto.tag_add('final', f"{resultado_texto.index(tk.END)}-12c", tk.END)
        elif token == 'NODEFINIDO':
            resultado_texto.tag_add('nodefinido', f"{resultado_texto.index(tk.END)}-12c", tk.END)
    
    resultado_texto.tag_config('reservado', foreground='blue')
    resultado_texto.tag_config('identificador', foreground='green')
    resultado_texto.tag_config('operador', foreground='orange')
    resultado_texto.tag_config('numero', foreground='purple')
    resultado_texto.tag_config('punto', foreground='orange')
    resultado_texto.tag_config('final', foreground='red')
    resultado_texto.tag_config('nodefinido', foreground='gray')

def borrar_codigo():
    entrada_texto.delete('1.0', tk.END)

# Crear ventana tkinter
ventana = tk.Tk()
ventana.title("Analizador de Código")

# Configuración de colores y estilos
color_fondo = "#FFC0CB"  # rosa claro
color_botones = "#800080"  # morado
color_texto_botones = "white"
color_texto = "#333333"

ventana.configure(bg=color_fondo)

# Crear frame para los botones
frame_botones = tk.Frame(ventana, bg=color_fondo)
frame_botones.pack(pady=5)

# Etiqueta y botón para borrar el código
etiqueta_codigo = tk.Label(frame_botones, text="Ingrese el código a analizar:", bg=color_fondo, fg=color_texto)
etiqueta_codigo.pack(side=tk.LEFT, padx=10)

boton_borrar = tk.Button(frame_botones, text="Borrar", bg=color_botones, fg=color_texto_botones, command=borrar_codigo)
boton_borrar.pack(side=tk.LEFT, padx=10)

# Crear un área de texto para ingresar el código
entrada_texto = tk.Text(ventana, height=10, width=50)
entrada_texto.pack(pady=5)

# Botón para analizar el código
boton_analizar = tk.Button(ventana, text="Analizar", bg=color_botones, fg=color_texto_botones, command=analizar_codigo)
boton_analizar.pack(pady=5)

# Separador
separador = tk.Label(ventana, text="Resultados del análisis:", bg=color_fondo, fg=color_texto)
separador.pack(pady=5)

# Crear un área de texto para mostrar los resultados
resultado_texto = tk.Text(ventana, height=10, width=50)
resultado_texto.pack(pady=5)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()