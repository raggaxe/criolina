
from flask import Flask, session, Markup, Response
from flask import request, render_template, url_for, redirect, flash, send_file
from flask_mail import Mail, Message
from datetime import datetime
from passlib.hash import sha256_crypt
import warnings

from dbconnect import connection
from functools import wraps
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
import random

import math

from autualizador import InsertSql, UpdateQuerySql, SelectSql, eventos



mes = str(datetime.now().strftime("%b"))
dia = str(datetime.now().strftime("%d"))
hora = str(datetime.now().strftime("%H:%M:%S"))

num_Os = []
user_online = []
app = Flask(__name__)

mail_settings = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 465,
    'MAIL_USE_TLS':False,
    'MAIL_USE_SSL': True,
    'MAIL_USERNAME':'rafael.figueiradafoz@gmail.com',
    'MAIL_PASSWORD': 'ttvjkembddcfqjxs'

}

app.config.update(mail_settings)

mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rootpass@localhost/festa_facil'

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY']='my_love_dont_try'


############ METODOS APLICADOS ####################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#
# def invoice(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'invoice' in session:
#             return f(*args, **kwargs)
#         else:
#             flash("Nao possui nenhum pedido")
#             return redirect(url_for('dashboard'))
#     return wrap
#
#








def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Precisa fazer o Login")
            return redirect(url_for('index'))
    return wrap




############ METODOS APLICADOS ####################




def check_user_Login(login):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM usuarios WHERE LOGIN={login}""")
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))
def check_user_ID(id):
    try:
        c,conn = connection()
        x = c.execute(f"""SELECT * FROM usuarios WHERE id_usuario={id}""")
        if int(x) > 0:
            myresult = c.fetchall()
            return myresult
        if int(x) == 0:
            return False
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))


def generateOTP():
    # Declare a string variable
    # which stores all string
    string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6):
        OTP += string[math.floor(random.random() * length)]
    return OTP



def ADD_pontos(pontos, id):
    user = SelectSql('usuarios','id_usuarios',id)
    for x in user:
        add = int(x[6]) + int(pontos)
        UpdateQuerySql({'PONTOS':add},'usuarios','id_usuarios',id)



############ INDEX ####################

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        festas = SelectSql('eventos','STATUS', 'OK')
        links = SelectSql('instagram','STATUS', 'OK')
        print(festas)

        return render_template('index.html', festas=festas, links=links)
    except Exception as e:
        print(f' ERROR:       {str(e)}')
        return (str(e))





# ############ ROTAS DIRETAS ####################
@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    flash('Voce esta saindo do APP! Obrigado','logout')
    return redirect(url_for('index'))
@app.errorhandler(404)
def pag_not_found(e):
    return render_template("404.html")


        ##### DASHBOARD #####
@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required

def dashboard():
    delyvery_list = []
    realizado_list = []
    id = session['ID_User']
    user = SelectSql('usuarios', 'id_usuarios',id)
    pedidos = SelectSql('invoice', 'id_usuarios',id)
    for p in pedidos:
        status = p[5]

        if status == 'A ENTREGAR':
            delyvery_list.append(status)
        if status == 'REALIZADO':
            realizado_list.append(status)


    to_delivery = len(delyvery_list)
    realizados = len(realizado_list)
    n_pedidos = len(pedidos)
    # print(to_delivery)


    return render_template('dashboard.html', user=user[0], pontos=user[0][6],
                           invoice = pedidos, pop_pedidos= n_pedidos,
                           to_delivery=to_delivery, realizados=realizados)




# @app.route('/page_forgot_password', methods=['GET', 'POST'])
# def email_forgot():
#     return render_template('redirect.html')


@app.route('/pedidos_promo', methods=['GET', 'POST'])
def pedidos_promo():

    return render_template('pedidos_promo.html')


@app.route('/transfer/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    if filename == None:
        filename = 'teste'
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)




############ ROTAS LOGIN / DASHBOARD ####################


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    try:
        if request.method == 'POST':

            if request.form['POP_UP'] == 'pedidos_promo':
                email = request.form['EMAIL']
                password = request.form['PASSWORD']
                check_user = SelectSql('usuarios', 'LOGIN', email)
                page_url = request.form['POP_UP']

                if check_user == False:
                    flash("Login ou Senha Errada, confira e tenta novamente", 'erro')

                    return redirect(url_for(page_url))
                else:
                    for person in check_user:
                        id = person[0]
                        check_password = person[4]
                        nome = person[1]
                        apelido = person[2]
                        end = person[7]
                        if sha256_crypt.verify(password, check_password):
                            session['logged_in'] = True
                            session['email'] = email
                            session['Completo'] = f'{nome} {apelido}'
                            session['Nome'] = f'{nome}'
                            session['ID_User'] = id
                            session['delivery'] = end
                            print('certo')

                            return redirect(url_for(page_url))

                        else:
                            print('senha erro')
                            flash("Login ou Senha Errada, confira e tenta novamente", 'erro')
                            return redirect(url_for(page_url))
            else:
                email = request.form['EMAIL']
                password = request.form['PASSWORD']
                check_user = SelectSql('usuarios', 'LOGIN', email)

                if check_user == False:
                    flash("Login ou Senha Errada, confira e tenta novamente", 'erro')

                    return redirect(url_for('index'))
                else:
                    for person in check_user:

                        id = person[0]
                        check_password = person[4]
                        nome = person[1]
                        apelido = person[2]
                        end = person[7]
                        if sha256_crypt.verify(password, check_password):
                            session['logged_in'] = True
                            session['email'] = email
                            session['Completo'] = f'{nome} {apelido}'
                            session['Nome'] = f'{nome}'
                            session['ID_User'] = id
                            session['delivery'] = end
                            print('certo')

                            return redirect(url_for('dashboard'))

                        else:
                            print('senha erro')
                            flash("Login ou Senha Errada, confira e tenta novamente", 'erro')
                            return redirect(url_for('index'))

            # if email == "admin@admin.com" and password == "123456":
            #     session['admin'] = True
            #
            #
            #
            #
            #     return redirect(url_for('dashboard'))
            #

        return render_template("index.html", error=error)

    except Exception as e:
        # flash(e)
        return redirect(url_for('index'))





############ ROTAS DE TRABALHO ####################



#
#         ##### EMAIL FORGOT / TOKEN  #####
#
#
#
# @app.route('/token/<string:email>', methods=['GET', 'POST'])
# def token(email):
#     token = generateOTP()
#     print(token)
#     UpdateQuerySql({'OTP': token}, 'usuarios', 'EMAIL', email)
#     user = SelectSql('usuarios', 'LOGIN', email)
#     for item in user:
#         # id = item[0]
#         nome_completo = f'{item[3]} {item[4]}'
#     if __name__ == '__main__':
#         with app.app_context():
#             msg = Message(subject='Pedido de Nova Senha',
#                           sender=app.config.get('MAIL_USERNAME'),
#                           recipients=[email],
#                           html=render_template('email_reply.html', token=token, user=nome_completo))
#             mail.send(msg)
#             flash('Verifique o seu e-mail, um novo código foi enviado.', 'login')
#             return render_template('insert_code.html', email=email)
#
# @app.route('/send_email_password', methods=['GET', 'POST'])
# def index_mail():
#     email = request.form['email']
#     token = generateOTP()
#     print(token)
#     user = SelectSql('usuarios','LOGIN',email)
#     if user == False:
#         flash(f'Esse email não está cadastrado!!! Verifique se está correto o email {email}','erro')
#         return redirect(url_for('email_forgot'))
#     else:
#         UpdateQuerySql({'OTP': token}, 'usuarios', 'EMAIL',email)
#         for item in user:
#             nome_completo = f'{item[3]} {item[4]}'
#         if __name__ == '__main__':
#             with app.app_context():
#                 msg = Message(subject='Código para alteração de password Guia Figueira da Foz',
#                             sender=app.config.get('MAIL_USERNAME'),
#                               recipients=[email],
#                               html=render_template('email_reply.html',token=token, user=nome_completo))
#                 mail.send(msg)
#                 return render_template('insert_code.html', email=email)
#
#
# @app.route('/confima_code', methods=['GET', 'POST'])
# def confirma_code():
#     if request.method == "POST":
#         email = request.form['email']
#         code = request.form['code']
#         new_password = sha256_crypt.encrypt((str(request.form['new_password'])))
#         data = SelectSql('usuarios', 'LOGIN',email)
#         for item in data:
#             OTP = item[12]
#             if str(OTP) == str(code):
#                 UpdateQuerySql({'PASSWORD':new_password}, 'usuarios','EMAIL',email)
#                 flash('Senha Atualizada com Sucesso!', 'success')
#                 return redirect(url_for('LoginClientes'))
#             else:
#                 flash('Código não está correto, tente novamente', 'erro')
#                 return render_template('insert_code.html',email=email)
#
#
#
#         ####### REGISTER USUARIOS ##########

#
@app.route('/register', methods=['POST'])
def register():
    error = ''
    try:
        if request.method == 'POST':
            email = request.form['EMAIL']
            nome = request.form['NOME']
            apelido = request.form['SOBRENOME']
            check_user = SelectSql('usuarios', 'LOGIN', email)
            print(check_user)
            if check_user == False:
                password = sha256_crypt.encrypt((str(request.form['PASSWORD'])))
                # DATA = str(datetime.now().strftime("%b %d,%Y"))
                myDict = {
                    'LOGIN': email,
                    'PASSWORD' : password,
                    'NOME' : nome,
                    'SOBRENOME' : apelido,
                    'NOTIFICACOES' : 0 ,
                    'PONTOS' : 0,
                    'DATA_INSCRICAO': f'{dia} {mes}',
                    'ENDERECO': False

                }
                InsertSql(myDict,'usuarios')
                user = SelectSql('usuarios', 'LOGIN',email)
                for item in user:
                    id = item[0]
                session['logged_in'] = True
                session['email'] = email
                session['Completo'] = f'{nome} {apelido}'
                session['Nome'] = f'{nome}'
                session['ID_User'] = id
                session['delivery'] = False
                return redirect(url_for('dashboard'))
            else:
                flash('Usuário já cadastrado, escolha um email diferente', 'login')
                return redirect(url_for('index'))
        return redirect(url_for('index'))

    except Exception as e:
        flash(e)



@app.route('/invoice_promo', methods=['GET', 'POST'])
def invoice_promo():
    from datetime import timedelta
    d = datetime.today()
    if request.method == "POST":
        for post in request.form:
            #### PEDIDO ####
            while d.weekday() != 4:
                d += timedelta(1)
            data_entrega = str(d)
            dia_entrega = data_entrega[8:10]
            mes_entrega = data_entrega[5:7]
            ano_entrega = data_entrega[0:4]
            entrega = f'{dia_entrega}/{mes_entrega}/{ano_entrega}'
            if post == 'ENDERECO':
                #### INSERT USER ENDERECO #####
                myDict_user = {'ENDERECO':request.form['ENDERECO'],
                          'APT':request.form['APT'],
                          'BAIRRO':request.form['BAIRRO'],
                          'CEP':request.form['CEP'],
                          'TELEFONE': request.form['TELEFONE'],
                          }

                myDict_invoice = {'PEDIDO_1':request.form['PEDIDO_1'],
                          'PEDIDO_2':request.form['PEDIDO_2'],
                          'id_usuarios':request.form['ID'],
                          'DATA':f'{dia} {mes}',
                                  'STATUS': 'A ENTREGAR',
                         'CATEGORIA':'PROMOCAO',
                                  'ENTREGA':entrega}


                UpdateQuerySql(myDict_user,'usuarios','id_usuarios',request.form['ID'])
                InsertSql(myDict_invoice,'invoice')
                ADD_pontos(20, request.form['ID'])
                session['invoice'] = True
                session['delivery'] = True

                return redirect(url_for('dashboard'))
            else:
                myDict_invoice = {'PEDIDO_1': request.form['PEDIDO_1'],
                                  'PEDIDO_2': request.form['PEDIDO_2'],
                                  'id_usuarios': request.form['ID'],
                                  'DATA': f'{dia} {mes}',
                                  'STATUS': 'A ENTREGAR',
                                  'CATEGORIA': 'PROMOCAO',
                                  'ENTREGA':entrega}

                InsertSql(myDict_invoice, 'invoice')
                ADD_pontos(20, request.form['ID'])
                return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

@app.route('/delete_invoice/<string:id_data>', methods = ['GET'])
def delete(id_data):
    print(id_data)
    c, conn = connection()
    c.execute("DELETE FROM invoice WHERE id_invoice=%s", (id_data))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))



# ############## CONFIGURACOES DE USUARIOS #################
#
# @app.route('/edit_profile_photo', methods=['GET', 'POST'])
# def edit_profile_photo():
#     if request.method == "POST":
#         myDict = {}
#         if request.files['file']:
#             f = request.files['file']
#             print(f)
#             if f and allowed_file(f.filename):
#                 filename = secure_filename(f.filename)
#                 f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'avatar'+filename))
#                 myDict.update({'FOTO':'avatar'+filename})
#         UpdateQuerySql(myDict, 'usuarios','EMAIL',session['email'])
#         return redirect(url_for('dashboard'))
#
#
# @app.route('/usuarios/', methods=['GET', 'POST'])
# def usuarios():
#     c, conn = connection()
#     c.execute("SELECT  * FROM usuarios")
#     data = c.fetchall()
#     c.close()
#     return render_template('lista-Usuarios.html', usuarios=data )
#
#
#
# @app.route('/edit_usuario', methods=['GET', 'POST'])
# def edit_usuario():
#     if request.method == "POST":
#         data = []
#         myDict = {}
#         for post in request.form:
#             data.append(post)
#         for form in data:
#             request_form = request.form[form]
#             print(request_form)
#             myDict.update({form: request_form})
#             if request_form == '':
#                 request_form = "blank"
#                 myDict.update({form: request_form})
#             else:
#                 myDict.update({form: request_form})
#         print(myDict)
#         UpdateQuerySql(myDict, 'usuarios', 'EMAIL', session['email'])
#     return redirect(url_for('dashboard'))
#
#
# @app.route('/delete/<string:id_data>', methods = ['GET'])
# def delete(id_data):
#     flash("Record Has Been Deleted Successfully")
#     c, conn = connection()
#     c.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_data,))
#     return redirect(url_for('usuarios'))
#
#




def main ():
    app.secret_key = 'IPA_Criolina_1980'
    port = int(os.environ.get("PORT", 5002))
    app.run (host="0.0.0.0", port=port)

if __name__ == "__main__":
   main()

