import sqlite3
import tkinter as tk
import datetime
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
# Conectar ao banco de dados (será criado se não existir)

def pegar_foto_livro(nome):
    conn, cursor = conectar()
    cursor.execute("SELECT foto_capa FROM livro WHERE nome = ?", (nome,))
    foto_capa = cursor.fetchone()[0]
    conn.close()
    return foto_capa
def exibir_foto_livro(nome):
    imagem = Image.open(nome)
    imagem_redimensionada = imagem.resize((120, 170))  # largura, altura
    foto_capa_tk = ImageTk.PhotoImage(imagem_redimensionada)
    return foto_capa_tk
def alugar_livro(nome,nome_pessoa, telefone, data_de_entrega,tela):
    if nome == "" or telefone == "" or data_de_entrega == "":
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return
    print(nome,nome_pessoa, telefone, data_de_entrega)
    try:
        # Formato correto: com barras
        data_de_entrega_obj = datetime.strptime(data_de_entrega, "%d/%m/%Y").date()
    except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA.")
        return

    data_atual = datetime.now().date()

    if data_de_entrega_obj < data_atual:
        messagebox.showerror("Erro", "Data de entrega não pode ser anterior à data atual.")
        return

    conn, cursor = conectar()
    try:
        data_formatada = data_atual.strftime("%d/%m/%Y")
        cursor.execute("SELECT id FROM livro WHERE nome = ?", (nome,))
        livro_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO pessoa (nome, telefone,data_do_aluguel,data_da_devolucao,livro_id) VALUES (?, ?, ?, ?, ?)", (nome_pessoa, telefone,data_formatada,data_de_entrega,livro_id))
        cursor.execute("UPDATE livro SET alugado = 1 WHERE nome = ?", (nome,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Livro alugado com sucesso!")
        exibir_livros("")
        tela.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no banco de dados: {e}")
    finally:
        exibir_livros("")
        conn.close()  
    
    


def exibir_livros(nome):
    """
    Esta função é responsável por buscar livros no banco de dados com base no nome fornecido.
    Ela utiliza .
    """
    if nome == "alugado":
        conn, cursor = conectar()
        cursor.execute("SELECT nome,alugado FROM livro WHERE alugado = 1")
        livros = cursor.fetchall()
        conn.close()
        return livros
    else:
        conn, cursor = conectar()
        cursor.execute("SELECT nome,alugado FROM livro WHERE nome LIKE ?", (f"%{nome}%",))
        livros = cursor.fetchall()
        conn.close()
        return livros

def cadastrar_livro(nome,autor,foto_capa,tela):
    conn, cursor = conectar()
    if nome == "" or autor == "":
        messagebox.showerror("Erro", "Preencha os campos obrigatórios.")
        return
    if foto_capa == "":
        foto_capa = "imgs/livros/sem_foto.png"
    try:
        cursor.execute("SELECT id FROM livro WHERE nome = ?", (nome,))
        if cursor.fetchone() is not None:
            messagebox.showerror("Erro", "Livro já cadastrado.")
            return
        cursor.execute("INSERT INTO livro (nome,autor,foto_capa) VALUES (?,?,?)", (nome,autor,foto_capa))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no banco de dados: {e}")
        return
    finally:
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        tela.destroy()
    

def realizar_pesquisa(entry_widget, listbox_widget):
   
    termo_pesquisa = entry_widget.get()
    livros_encontrados = exibir_livros(termo_pesquisa)

    # Limpar resultados anteriores
    listbox_widget.delete(0, tk.END)

    # Exibir novos resultados
    if livros_encontrados:
        for livro in livros_encontrados:
            listbox_widget.insert(tk.END, f"{livro[0]} - {'Alugado' if livro[1] else 'Disponível'}")
    else:
        listbox_widget.insert(tk.END, "Nenhum livro encontrado.")


def conectar():
    conn = sqlite3.connect("biblioteca.db",timeout=10)
    cursor = conn.cursor()
    return conn, cursor

conn, cursor = conectar()
# Criar a tabela 'livro'
cursor.execute("""
CREATE TABLE IF NOT EXISTS livro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    autor TEXT NOT NULL,
    foto_capa TEXT,
    alugado BOOLEAN NOT NULL DEFAULT 0
);
""")

# Criar a tabela 'usuario'
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL
    
    );
""")
# Criar a tabela 'pessoa'

cursor.execute("""
CREATE TABLE IF NOT EXISTS pessoa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    data_do_aluguel TEXT NOT NULL DEFAULT (DATE('now')),
    data_da_devolucao TEXT NOT NULL DEFAULT (DATE('now', '+10 days')),
    livro_id INTEGER NOT NULL,
    FOREIGN KEY (livro_id) REFERENCES livro(id)
);
""")


    



print("Conectado ao banco de dados")

# Salvar alterações e fechar a conexão
conn.commit()
conn.close()
