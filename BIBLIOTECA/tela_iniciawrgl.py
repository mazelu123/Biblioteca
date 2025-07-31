import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minha Biblioteca")
        self.root.geometry("800x600")

        self.conn = None
        self.cursor = None
        self.conectar_banco_dados()

        self.criar_widgets()
        self.atualizar_lista_livros() # Carrega os livros do banco ao iniciar

        # Garante que a conexão com o banco de dados seja fechada ao sair
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)

    def conectar_banco_dados(self):
        """Conecta ao banco de dados SQLite e cria as tabelas se não existirem."""
        try:
            self.conn = sqlite3.connect("biblioteca.db")
            self.cursor = self.conn.cursor()

            # Criar a tabela 'livro'
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                autor TEXT NOT NULL,
                foto_capa TEXT,
                alugado BOOLEAN NOT NULL DEFAULT 0,
                alugado_por TEXT,
                telefone_cliente TEXT
            );
            """)

            # Adicionar colunas 'alugado_por' e 'telefone_cliente' se não existirem
            # Isso é útil para atualizações de esquema em bancos de dados existentes
            try:
                self.cursor.execute("ALTER TABLE livro ADD COLUMN alugado_por TEXT")
            except sqlite3.OperationalError:
                pass # Coluna já existe
            try:
                self.cursor.execute("ALTER TABLE livro ADD COLUMN telefone_cliente TEXT")
            except sqlite3.OperationalError:
                pass # Coluna já existe

            # Criar a tabela 'usuario' (não usada nesta versão, mas mantida por sua estrutura)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL
            );
            """)

            self.conn.commit()
            print("Conectado ao banco de dados e tabelas verificadas.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Não foi possível conectar ou criar o banco de dados: {e}")
            self.root.destroy() # Fecha a aplicação se não conseguir conectar ao banco

    def fechar_aplicacao(self):
        """Salva alterações e fecha a conexão com o banco de dados antes de sair."""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("Conexão com o banco de dados fechada.")
        self.root.destroy()

    def criar_widgets(self):
        """Cria e posiciona os elementos da interface gráfica."""
        # --- Seção de Pesquisa ---
        search_frame = tk.Frame(self.root, pady=10)
        search_frame.pack(fill="x")

        search_label = tk.Label(search_frame, text="Pesquisar Livro:")
        search_label.pack(side="left", padx=5)

        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(side="left", padx=5, expand=True, fill="x")
        self.search_entry.bind("<KeyRelease>", self.filtrar_livros) # Filtra ao digitar

        search_button = tk.Button(search_frame, text="Pesquisar", command=self.filtrar_livros)
        search_button.pack(side="left", padx=5)

        # --- Botão de Cadastro ---
        cadastro_frame = tk.Frame(self.root, pady=10)
        cadastro_frame.pack(fill="x")

        cadastro_button = tk.Button(cadastro_frame, text="Cadastrar Novo Livro", command=self.abrir_janela_cadastro_livro)
        cadastro_button.pack(pady=5)

        # --- Área de Exibição de Livros ---
        books_display_frame = tk.Frame(self.root, bd=2, relief="groove")
        books_display_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.books_listbox = tk.Listbox(books_display_frame, height=20, font=("Arial", 12))
        self.books_listbox.pack(side="left", fill="both", expand=True)
        self.books_listbox.bind("<Double-Button-1>", self.abrir_janela_alugar_livro) # Abre janela de aluguel ao duplo clique

        scrollbar = tk.Scrollbar(books_display_frame, orient="vertical", command=self.books_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.books_listbox.config(yscrollcommand=scrollbar.set)

    def abrir_janela_cadastro_livro(self):
        """Abre uma nova janela para o cadastro de um novo livro."""
        cadastro_window = tk.Toplevel(self.root)
        cadastro_window.title("Cadastrar Livro")
        cadastro_window.geometry("300x200")
        cadastro_window.transient(self.root) # Define como janela transitória (sempre acima da principal)
        cadastro_window.grab_set() # Bloqueia interação com a janela principal

        tk.Label(cadastro_window, text="Nome do Livro:").pack(pady=5)
        nome_entry = tk.Entry(cadastro_window, width=40)
        nome_entry.pack(pady=5)

        tk.Label(cadastro_window, text="Autor do Livro:").pack(pady=5)
        autor_entry = tk.Entry(cadastro_window, width=40)
        autor_entry.pack(pady=5)

        def salvar_livro():
            nome = nome_entry.get().strip()
            autor = autor_entry.get().strip()

            if nome and autor:
                try:
                    # Insere o livro no banco de dados
                    self.cursor.execute(
                        "INSERT INTO livro (nome, autor, alugado) VALUES (?, ?, ?)",
                        (nome, autor, 0) # 0 significa não alugado (disponível)
                    )
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", f"Livro '{nome}' de '{autor}' cadastrado!")
                    self.atualizar_lista_livros()
                    cadastro_window.destroy()
                except sqlite3.Error as e:
                    messagebox.showerror("Erro no Banco de Dados", f"Não foi possível cadastrar o livro: {e}")
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

        save_button = tk.Button(cadastro_window, text="Salvar Livro", command=salvar_livro)
        save_button.pack(pady=10)
        self.root.wait_window(cadastro_window) # Espera a janela de cadastro ser fechada

    def atualizar_lista_livros(self):
        """Carrega os livros do banco de dados e os exibe na Listbox, aplicando filtro se houver."""
        self.books_listbox.delete(0, tk.END) # Limpa a lista atual

        termo_pesquisa = self.search_entry.get().strip().lower()
        query = "SELECT id, nome, autor, alugado, alugado_por FROM livro"
        params = []

        if termo_pesquisa:
            query += " WHERE LOWER(nome) LIKE ? OR LOWER(autor) LIKE ?"
            params = [f"%{termo_pesquisa}%", f"%{termo_pesquisa}%"]

        try:
            self.cursor.execute(query, params)
            livros = self.cursor.fetchall() # Pega todos os resultados

            if not livros:
                self.books_listbox.insert(tk.END, "Nenhum livro encontrado.")
                return

            for livro_data in livros:
                book_id, nome, autor, alugado, alugado_por = livro_data
                status = "Alugado" if alugado else "Disponível"
                display_text = f"ID: {book_id} - {nome} - {autor} ({status})"
                if alugado and alugado_por:
                    display_text += f" por {alugado_por}"
                self.books_listbox.insert(tk.END, display_text)
                # Armazena o ID do livro junto com o item da Listbox para fácil recuperação
                self.books_listbox.item_data[self.books_listbox.size()-1] = book_id
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Não foi possível carregar os livros: {e}")

    # Adiciona um dicionário para mapear índices da listbox para IDs do banco de dados
    # Isso é necessário porque a Listbox só armazena strings.
    # Alternativamente, você pode parsear o ID da string exibida.
    # Para simplicidade e robustez, vamos usar um dicionário auxiliar.
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "books_listbox":
            self.books_listbox.item_data = {} # Inicializa o dicionário para IDs

    def filtrar_livros(self, event=None):
        """Chama a função para atualizar a lista de livros com base no filtro."""
        self.atualizar_lista_livros()

    def abrir_janela_alugar_livro(self, event):
        """Abre uma janela para alugar um livro selecionado."""
        selecionado_index = self.books_listbox.curselection()
        if not selecionado_index:
            return

        # Recupera o ID do livro a partir do item selecionado na Listbox
        # Usando o dicionário item_data para mapear o índice da listbox para o ID do banco de dados
        selected_listbox_index = selecionado_index[0]
        book_id = self.books_listbox.item_data.get(selected_listbox_index)

        if book_id is None:
            messagebox.showerror("Erro", "Não foi possível encontrar o ID do livro selecionado.")
            return

        try:
            self.cursor.execute("SELECT nome, alugado FROM livro WHERE id = ?", (book_id,))
            livro_data = self.cursor.fetchone()

            if not livro_data:
                messagebox.showerror("Erro", "Livro não encontrado no banco de dados.")
                return

            nome_livro, alugado_status = livro_data

            if alugado_status: # Se alugado_status for 1 (True)
                messagebox.showinfo("Livro Indisponível", "Este livro já está alugado.")
                return

            alugar_window = tk.Toplevel(self.root)
            alugar_window.title(f"Alugar: {nome_livro}")
            alugar_window.geometry("350x250")
            alugar_window.transient(self.root)
            alugar_window.grab_set()

            tk.Label(alugar_window, text=f"Alugar o livro: {nome_livro}").pack(pady=10)

            tk.Label(alugar_window, text="Nome do Cliente:").pack(pady=5)
            cliente_nome_entry = tk.Entry(alugar_window, width=40)
            cliente_nome_entry.pack(pady=5)

            tk.Label(alugar_window, text="Telefone do Cliente:").pack(pady=5)
            cliente_telefone_entry = tk.Entry(alugar_window, width=40)
            cliente_telefone_entry.pack(pady=5)

            def confirmar_aluguel():
                nome_cliente = cliente_nome_entry.get().strip()
                telefone_cliente = cliente_telefone_entry.get().strip()

                if nome_cliente and telefone_cliente:
                    try:
                        # Atualiza o status do livro no banco de dados
                        self.cursor.execute(
                            "UPDATE livro SET alugado = ?, alugado_por = ?, telefone_cliente = ? WHERE id = ?",
                            (1, nome_cliente, telefone_cliente, book_id) # 1 significa alugado (False)
                        )
                        self.conn.commit()
                        messagebox.showinfo("Sucesso", f"Livro '{nome_livro}' alugado por {nome_cliente}.")
                        self.atualizar_lista_livros()
                        alugar_window.destroy()
                    except sqlite3.Error as e:
                        messagebox.showerror("Erro no Banco de Dados", f"Não foi possível alugar o livro: {e}")
                else:
                    messagebox.showerror("Erro", "Por favor, preencha todos os dados do cliente.")

            confirm_button = tk.Button(alugar_window, text="Confirmar Aluguel", command=confirmar_aluguel)
            confirm_button.pack(pady=10)
            self.root.wait_window(alugar_window)
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Erro ao buscar detalhes do livro: {e}")


# --- Execução da Aplicação ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
