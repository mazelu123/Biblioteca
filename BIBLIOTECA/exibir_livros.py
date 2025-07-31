from tkinter import *
from tkinter import ttk
import DataBaser
import sqlite3

def rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

#cores
cinza_escuro = rgb(20, 20, 20)
cinza_claro = rgb(50, 50, 50)

def exibir_livros():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livro")
    livros = cursor.fetchall()
    conn.close()
    return livros


