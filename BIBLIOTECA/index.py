from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tela_inicial import abrir_tela_principal

import DataBaser

def rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

# cores
cinza_escuro = rgb(20, 20, 20)
cinza_claro = rgb(50, 50, 50)

#cria janela
janela = Tk() 
janela.title("Tela de login")
janela.geometry("600x300")
janela.configure(background=cinza_claro) 
janela.resizable(False, False)# não permite redimensionar a janela
janela.iconbitmap("imgs/channels4_profile.ico")
#//////////////////////imagens///////////////////
logo = PhotoImage(file="imgs/logo.png")



#////////////////////////////////// widgets ////////////////////////
frame_esquerdo = Frame(janela, width=180, height=300, bg=cinza_escuro, relief="raise")
frame_esquerdo.pack(side=LEFT)

frame_direito = Frame(janela, width=419.1, height=300, bg=cinza_escuro, relief="raise")
frame_direito.pack(side=RIGHT)

label_logo = Label(frame_esquerdo, image=logo, bg=cinza_escuro)
label_logo.place(x=40, y=10)

label_usuario = Label(frame_direito, text="Usuário:", bg=cinza_escuro, fg=rgb(255, 255, 255), font=("Arial", 16))
label_usuario.place(x=40, y=10)

entry_usuario = ttk.Entry(frame_direito, width=20, font=("Arial", 16))
entry_usuario.place(x=40, y=40)

label_senha = Label(frame_direito, text="Senha:", bg=cinza_escuro, fg=rgb(255, 255, 255), font=("Arial", 16))
label_senha.place(x=40, y=70)

entry_senha = ttk.Entry(frame_direito, width=20, show="*", font=("Arial", 16))
entry_senha.place(x=40, y=100)
import sqlite3
from tkinter import messagebox

def login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    if usuario == "" or senha == "":
        messagebox.showerror("Login", "Preencha todos os campos!")
    else:
        try:
            # Abre uma conexão local ao banco de dados
            conn = sqlite3.connect("biblioteca.db")
            cursor = conn.cursor()

            # Executa a consulta de validação
            cursor.execute("SELECT * FROM usuario WHERE nome = ? AND senha = ?", (usuario, senha))
            resultado = cursor.fetchone()

            if resultado:
                
                
                janela.destroy()
                messagebox.showinfo("Login", "Login realizado com sucesso!")
                abrir_tela_principal()
            
            else:
                messagebox.showerror("Login", "Usuário ou senha incorretos!")

        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", f"Erro: {e}")
        finally:
            if conn:
                conn.close()
    

    
botao_login = Button(frame_direito, text="Login", bg=cinza_escuro, fg=rgb(255, 255, 255), font=("Arial", 16), command=login)
botao_login.place(x=130, y=140)


janela.mainloop()

