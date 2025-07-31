import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from functools import partial
from DataBaser import *
import time
import os
import PIL
from PIL import Image, ImageTk
#limpa o terminal
os.system("cls")
def rgb(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"
#cores
cinza_escuro = rgb(20, 20, 20)
cinza_claro = rgb(50, 50, 50)

def fechar_tela(tela):
    tela.destroy()

def abrir_tela_cadastro_livro(janela):
    tela = tk.Toplevel(janela)
    tela.title("Cadastro de Livro")
    tela.geometry("400x400")
    tela.resizable(False, False)
    tela.configure(bg=cinza_escuro)
    tela.grab_set()
    
    label_nome = tk.Label(tela, text="Nome", font=("Arial", 16), bg=cinza_escuro, fg="white")
    label_nome.pack(pady=10)

    entry_nome = tk.Entry(tela, font=("Arial", 16), bg="white", fg="black")
    entry_nome.pack(pady=10)
    
    label_autor = tk.Label(tela, text="Autor", font=("Arial", 16), bg=cinza_escuro, fg="white")
    label_autor.pack(pady=10)

    entry_autor = tk.Entry(tela, font=("Arial", 16), bg="white", fg="black")
    entry_autor.pack(pady=10)

    label_foto_capa = tk.Label(tela, text="Foto da capa", font=("Arial", 16), bg=cinza_escuro, fg="white")
    label_foto_capa.pack(pady=10)

    entry_foto_capa = tk.Entry(tela, font=("Arial", 16), bg="white", fg="black")
    entry_foto_capa.pack(pady=10)
    
    button_cadastrar = tk.Button(tela, text="Cadastrar", font=("Arial", 16), bg="white", fg="black")
    button_cadastrar.pack(pady=10)
    
    button_cadastrar["command"] = lambda: cadastrar_livro(entry_nome.get(), entry_autor.get(), entry_foto_capa.get(),tela)
    #button_cadastrar.bind("<Button-1>", lambda event: fechar_tela(tela))

def tela_devolver_livro(livro_selecionado,janela):
    tela = tk.Toplevel(janela)
    tela.title("Devolução de livro")
    tela.geometry("400x400")
    tela.resizable(False, False)
    tela.configure(bg=cinza_escuro)
    tela.grab_set()

    label_titulo = tk.Label(tela, text="Devolução de livro", font=("Arial", 16), bg=cinza_escuro, fg="white")
    label_titulo.pack(pady=10)
    foto_capa = pegar_foto_livro(livro_selecionado)
    imagem = Image.open(foto_capa)
    imagem_redimensionada = imagem.resize((120, 170))  # largura, altura

    # Converte para imagem compatível com Tkinter
    foto_capa_tk = ImageTk.PhotoImage(imagem_redimensionada)

    # Cria o label e exibe
    label_foto_capa = tk.Label(tela, image=foto_capa_tk, bg=cinza_escuro)
    label_foto_capa.image = foto_capa_tk  # mantém referência
    label_foto_capa.pack(pady=10)

    # Conecta e busca os dados do aluguel
    conn, cursor = conectar()
    cursor.execute("""
        SELECT 
            l.nome, 
            p.nome, 
            p.telefone, 
            p.data_do_aluguel, 
            p.data_da_devolucao
        FROM livro l
        JOIN pessoa p ON l.id = p.livro_id
        WHERE l.alugado = 1 AND l.nome = ?
    """, (livro_selecionado,))
    dados = cursor.fetchone()
    conn.close()

    if dados:
        nome_livro, nome_pessoa, telefone, data_aluguel, data_devolucao = dados
        texto = (
            f"Livro: {nome_livro}\n"
            f"Alugado por: {nome_pessoa}\n"
            f"Telefone: {telefone}\n"
            f"Data do aluguel: {data_aluguel}\n"
            f"Data de devolução: {data_devolucao}"
        )

        label_info = tk.Label(tela, text=texto, font=("Arial", 16), bg=cinza_escuro, fg="white", justify="left")
        label_info.pack(pady=10)
        button_devolver = tk.Button(tela, text="Devolver", font=("Arial", 16), bg="white", fg="black")
        button_devolver.pack(pady=10)

def tela_alugar_livro(event, lista_livros,janela):
        selecionado = lista_livros.curselection()
        if not selecionado:
            return  # Nenhum item selecionado

        livro_selecionado = lista_livros.get(selecionado[0]).split(" - ")[0]

        conn, cursor = conectar()
        cursor.execute("SELECT nome, alugado FROM livro WHERE nome = ?", (livro_selecionado,))
        livro = cursor.fetchone()
        conn.close()

        if livro[1] == 1:
            tela_devolver_livro(livro_selecionado, janela)


        else:
            # Tela para alugar livro
            tela = tk.Toplevel(janela)
            tela.title("Alugar Livro")
            tela.geometry("400x600")
            tela.resizable(False, False)
            tela.configure(bg=cinza_escuro)
            tela.grab_set()

            foto_capa = pegar_foto_livro(livro_selecionado)
            imagem = Image.open(foto_capa)
            imagem_redimensionada = imagem.resize((120, 170))  # largura, altura

            # Converte para imagem compatível com Tkinter
            foto_capa_tk = ImageTk.PhotoImage(imagem_redimensionada)

            # Cria o label e exibe
            label_foto_capa = tk.Label(tela, image=foto_capa_tk, bg=cinza_escuro)
            label_foto_capa.image = foto_capa_tk  # mantém referência
            label_foto_capa.pack(pady=10)
            
            label_nome = tk.Label(tela, text="Nome", font=("Arial", 16), bg=cinza_escuro, fg="white")
            label_nome.pack(pady=10)


            entry_nome = tk.Entry(tela, font=("Arial", 16), bg="white", fg="black")
            entry_nome.pack(pady=10)

            label_telefone = tk.Label(tela, text="Telefone", font=("Arial", 16), bg=cinza_escuro, fg="white")
            label_telefone.pack(pady=10)

            entry_telefone = tk.Entry(tela, font=("Arial", 16), bg="white", fg="black")
            entry_telefone.pack(pady=10)

            label_data_de_entrega = tk.Label(tela, text="Data de Entrega", font=("Arial", 16), bg=cinza_escuro, fg="white")
            label_data_de_entrega.pack(pady=10)

            entry_data_de_entrega = tk.Entry(tela, font=("Arial", 16), bg="white", fg="black")
            entry_data_de_entrega.pack(pady=10)

            button_alugar = tk.Button(tela, text="Alugar", font=("Arial", 16), bg="white", fg="black")
            button_alugar.pack(pady=10)
            button_alugar["command"] = lambda: alugar_livro(
                livro_selecionado,
                entry_nome.get(),
                entry_telefone.get(),
                entry_data_de_entrega.get(),
                tela
            )

def abrir_tela_principal():
    janela = tk.Tk()
    janela.title("Minha Biblioteca")
    janela.state("zoomed")
    janela.geometry("800x600")
    janela.resizable(False, False)
    janela.configure(bg=cinza_claro)

    frame_topo = tk.Frame(janela, bg=cinza_escuro)
    frame_topo.pack(fill="x",pady=1)
    label_pesquisa = tk.Label(frame_topo, text="Pesquisa", font=("Arial", 16), bg=cinza_escuro, fg="white")
    label_pesquisa.grid(row=0, column=0, padx=10, pady=10)

    entry_pesquisa = tk.Entry(frame_topo, font=("Arial", 16), bg="white", fg="black")
    entry_pesquisa.grid(row=0, column=1, padx=10, pady=10)

    # Frame para exibir os livros
    frame_livros = tk.Frame(janela, bg=cinza_escuro)
    frame_livros.pack(fill="both", expand=True, pady=1)

    lista_livros = tk.Listbox(frame_livros, font=("Arial", 16), bg=cinza_escuro, fg="white")
    lista_livros.pack(fill="both", expand=True)

    # Importante: Passe os próprios widgets para a função partial, não seus valores .get().
    # A função `realizar_pesquisa` então obterá o valor atual quando for chamada.
    button_pesquisa = tk.Button(frame_topo, text="Pesquisar", font=("Arial", 16), bg="white", fg="black")
    button_pesquisa["command"] = partial(realizar_pesquisa, entry_pesquisa, lista_livros)
    button_pesquisa.grid(row=0, column=2, padx=1, pady=10)

    button_cadastrar_livro = tk.Button(frame_topo, text="Cadastrar Livro", font=("Arial", 16), bg="white", fg="black")
    button_cadastrar_livro["command"] = lambda: abrir_tela_cadastro_livro(janela)
    button_cadastrar_livro.grid(row=0, column=3, padx=1, pady=10)



    # Exibição inicial de todos os livros (opcional, mas bom para mostrar tudo inicialmente)
    # Isso exibirá todos os livros quando o aplicativo iniciar
    initial_livros = exibir_livros("") # Passe uma string vazia para obter todos os livros

    

















    

            
       








    for livro in initial_livros:
        lista_livros.insert(tk.END, f"{livro[0]} - {'Alugado' if livro[1] else 'Disponível'}")
    lista_livros.bind("<<ListboxSelect>>", lambda event: tela_alugar_livro(event,lista_livros,janela)  )
    janela.mainloop()
abrir_tela_principal()
    