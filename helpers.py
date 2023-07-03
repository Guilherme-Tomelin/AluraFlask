import os
from bibliotech import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class FormularioTecnologia(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1,max=30)])
    descricao = StringField('Descrição', [validators.DataRequired(), validators.Length(min=1,max=250)])
    nivel = StringField('Nível', [validators.DataRequired(), validators.Length(min=1,max=30)])
    criador = StringField('Criador', [validators.DataRequired(), validators.Length(min=1,max=60)])
    ano_lancamento = StringField('Ano de Lançamento', [validators.DataRequired(), validators.Length(min=4,max=4)])
    categorias = StringField('Categorias', [validators.DataRequired(), validators.Length(min=1,max=255)])
    recursos = StringField('Recursos', [validators.DataRequired(), validators.Length(min=1,max=200)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'icon{id}' in nome_arquivo:
            return nome_arquivo
    
    return 'default.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))