import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 1. Criar nova tabela com os campos corretos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudo_novo (
        id INTEGER PRIMARY KEY,
        materia VARCHAR(100) NOT NULL,
        data VARCHAR(20) NOT NULL,
        categoria TEXT DEFAULT 'Pessoal'
    )
""")

# 2. Copiar os dados da tabela antiga para a nova (sem o campo 'tema')
cursor.execute("""
    INSERT INTO estudo_novo (id, materia, data, categoria)
    SELECT id, materia, data, categoria FROM estudo
""")

# 3. Apagar a tabela antiga
cursor.execute("DROP TABLE estudo")

# 4. Renomear a nova tabela para o nome original
cursor.execute("ALTER TABLE estudo_novo RENAME TO estudo")

conn.commit()
conn.close()

print("✔️ Estrutura corrigida! Campo 'tema' removido com sucesso.")
