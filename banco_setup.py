import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash
from dotenv import load_dotenv
import os

print("Conectando...")
load_dotenv()
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password= os.getenv("DB_PASSWORD")
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `bibliotech`;")

cursor.execute("CREATE DATABASE `bibliotech`;")

cursor.execute("USE `bibliotech`;")

# criando tabelas
TABLES = {}
TABLES['Tecnologias'] = ('''
      CREATE TABLE `tecnologias` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(30) NOT NULL,
      `descricao` varchar(250) NOT NULL,
      `nivel` varchar(30) NOT NULL,
      `criador` varchar(60) NOT NULL,
      `ano_lancamento` int(4) NOT NULL,
      `categorias` varchar(255) NOT NULL,
      `recursos` varchar(200) NOT NULL,


      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Bruno Divino", "BD", generate_password_hash("alohomora").decode('utf-8')),
      ("Camila Ferreira", "Mila", generate_password_hash("paozinho").decode('utf-8')),
      ("Guilherme Louro", "Cake", generate_password_hash("python_eh_vida").decode('utf-8')),
      ("Guilherme Santos", "Tomelin", generate_password_hash("123456").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from bibliotech.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo tecnologias
tecnologias_sql = 'INSERT INTO tecnologias (nome, descricao, nivel, criador, ano_lancamento, categorias, recursos) VALUES (%s, %s, %s, %s, %s, %s, %s)'
tecnologias = [
    ('Python', 'Linguagem de programação de alto nível', 'Intermediário', 'Guido van Rossum', 1991,
     'Web, Data Science, Machine Learning', 'https://www.python.org/'),
    ('JavaScript', 'Linguagem de programação para web', 'Iniciante', 'Brendan Eich', 1995,
     'Web, Front-end', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript'),
    ('PHP', 'Linguagem de script para desenvolvimento web', 'Iniciante', 'Rasmus Lerdorf', 1995,
     'Web, Back-end', 'https://www.php.net/'),
    ('Java', 'Linguagem de programação orientada a objetos', 'Intermediário', 'James Gosling', 1995,
     'Desktop, Web, Mobile', 'https://www.java.com/')
]
converted_tecnologias = [(nome, descricao, nivel, criador, ano_lancamento, categorias, recursos)
                         for nome, descricao, nivel, criador, ano_lancamento, categorias, recursos in tecnologias]
cursor.executemany(tecnologias_sql, converted_tecnologias)

cursor.execute('select * from bibliotech.tecnologias')
print(' -------------  Tecnologias:  -------------')
for tecnologia in cursor.fetchall():
    print(tecnologia[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()