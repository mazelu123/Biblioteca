import sqlite3

# Função para conectar ao banco de dados
def conectar():
    """
    Conecta ao banco de dados 'biblioteca.db'.
    Se o banco de dados não existir, ele será criado.
    Retorna a conexão e o cursor.
    """
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    return conn, cursor

# Conectar ao banco de dados e criar tabelas (se não existirem)
def inicializar_banco_de_dados():
    """
    Conecta ao banco de dados e garante que as tabelas 'livro' e 'usuario' existam.
    """
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()
    print("Banco de dados inicializado e tabelas verificadas.")

# Dados de exemplo para livros
livros_exemplo = [
    {"nome": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "foto_capa": "imgs/livros/sem_foto.png"},
    {"nome": "1984", "autor": "George Orwell", "foto_capa": "imgs/livros/sem_foto.png"},
    {"nome": "Dom Quixote", "autor": "Miguel de Cervantes", "foto_capa": "imgs/livros/sem_foto.png"},
    {"nome": "Orgulho e Preconceito", "autor": "Jane Austen", "foto_capa": "imgs/livros/sem_foto.png"},
    {"nome": "Cem Anos de Solidão", "autor": "Gabriel García Márquez", "foto_capa": "imgs/livros/sem_foto.png"}
]

def semear_livros():
    """
    Insere dados de exemplo na tabela 'livro'.
    Primeiro, limpa a tabela para evitar duplicatas em execuções repetidas.
    """
    conn, cursor = conectar()

    try:
        # Opcional: Limpar a tabela 'livro' antes de semear para evitar duplicatas
        cursor.execute("DELETE FROM livro")
        print("Dados existentes da tabela 'livro' foram limpos.")

        # Inserir os livros de exemplo
        for livro in livros_exemplo:
            cursor.execute(
                "INSERT INTO livro (nome, autor, foto_capa, alugado) VALUES (?, ?, ?, ?)",
                (livro["nome"], livro["autor"], livro["foto_capa"], 0) # alugado é 0 (Falso) por padrão
            )
            print(f"Livro '{livro['nome']}' inserido.")

        conn.commit()
        print("Semeadura de livros concluída com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao semear livros: {e}")
        conn.rollback() # Reverter alterações em caso de erro
    finally:
        conn.close()

if __name__ == "__main__":
    inicializar_banco_de_dados() # Garante que as tabelas existam
    semear_livros() # Popula a tabela 'livro' com dados de exemplo
