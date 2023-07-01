from flask import Flask, render_template, request, redirect, session, flash, url_for

class Tecnologia:
    def __init__(self, nome, descricao, nivel, criador, ano_lancamento, categorias, recursos):
        self.nome=nome
        self.descricao=descricao 
        self.nivel=nivel
        self.criador=criador
        self.ano_lancamento=ano_lancamento
        self.categorias=categorias
        self.recursos=recursos

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Bruno Divino", "BD", "senha")
usuario2 = Usuario("Camila Ferreira", "Mila", "senha2")
usuario3 = Usuario("Guilherme Louro", "Cake", "senha3")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 }

app = Flask(__name__)
app.secret_key = 'aprendendoflask'

app.config['TEMPLATES_AUTO_RELOAD'] = True

tech1 = Tecnologia('Python', 'Linguagem de programação de alto nível', 'Intermediário', 'Guido van Rossum', 1991, ['Web', 'Data Science', 'Machine Learning'], ['https://www.python.org/'])
tech2 = Tecnologia('JavaScript', 'Linguagem de programação para web', 'Iniciante', 'Brendan Eich', 1995, ['Web', 'Front-end'], ['https://developer.mozilla.org/en-US/docs/Web/JavaScript'])
tech3 = Tecnologia('PHP', 'Linguagem de script para desenvolvimento web', 'Iniciante', 'Rasmus Lerdorf', 1995, ['Web', 'Back-end'], ['https://www.php.net/'])
tech4 = Tecnologia('Java', 'Linguagem de programação orientada a objetos', 'Intermediário', 'James Gosling', 1995, ['Desktop', 'Web', 'Mobile'], ['https://www.java.com/'])
lista_tecnologias = [tech1, tech2, tech3, tech4]


@app.route('/')
def index():
    return render_template('lista.html', titulo='Lista de tecnologias', tecnologias = lista_tecnologias)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Adicionar Tecnologia')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    descricao = request.form['descricao']
    nivel = request.form['nivel']
    criador = request.form['criador']
    ano_lancamento = request.form['ano_lancamento']
    categorias = request.form['categorias']
    recursos = request.form['recursos']

    tech = Tecnologia(nome,descricao,nivel,criador,ano_lancamento,categorias,recursos)
    lista_tecnologias.append(tech)
    return redirect(url_for('index'))

#--------------------------------------LOGIN--------------------------------------

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)