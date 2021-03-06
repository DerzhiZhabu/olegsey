import flask
import requests
from flask import *
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm, SearchForm
from flask_login import *
from test import Ozon_items
import os
from transliterate import translit
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def start():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search', text=form.search_line.data, filters='По популярности', page='1'))
    return render_template('search.html', title='Введите ваш запрос', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            image=form.image.data.name
        )
        form.image.data.save(f'static/img/{form.name.data}.png')
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        f = open(f'static/izb/{form.name.data}.json', 'w', encoding='utf-8')
        json.dump([], f)
        f.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    text = '+'.join(request.args.get('text').strip().split())
    text = translit(text, 'ru', reversed=True)
    filters = request.args.get('filters').strip()
    page = request.args.get('page').strip()
    oz_filt = 'mem'
    ol = ['По популярности', 'По возрастанию цены', 'По убыванию цены']
    ol.remove(filters)
    if filters == 'По популярности':
        oz_filt = 'score'
        sort = False
    elif filters == 'По возрастанию цены':
        oz_filt = 'price'
        sort = True
        kek = lambda s: s['cost']
        rev = False
    elif filters == 'По убыванию цены':
        oz_filt = 'price_desc'
        kek = lambda s: s['cost']
        rev = True
        sort = True
    k = Ozon_items(f'https://www.ozon.ru/search/?from_global=true&text={text}&sorting={oz_filt}&page={page}')
    s = k.lib
    if sort:
        s.sort(key=kek, reverse=rev)
    return render_template('place.html', lil=s, title='Резултаты запроса', text=text, filters=filters, ost=ol, page=page,)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/profile')
def profile():
    username = current_user.name
    f = open(f'static/izb/{username}.json', 'r', encoding='utf-8')
    izb = json.load(f)
    f.close()
    return render_template('profile.html', name=username, title='Профлиь', izbr=izb)



@app.route('/privet', methods=['get', 'post'])
def privet():
    name = request.args.get('name')
    link = request.args.get('link')
    image = request.args.get('image')
    cost = request.args.get('cost')
    platform = request.args.get('platform')
    delete = request.args.get('delete')
    redir = request.args.get('redir')
    if delete == 'True':
        ol = int(request.args.get('ol'))
    var = {'name': name,
           'mag': platform,
           'link': link,
           'cost': cost,
           'image': image}
    f = open(f'static/izb/{current_user.name}.json', 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    if delete == 'False':
        if len(data) == 0:
            ol = 0
        else:
            ol = data[-1]['ol'] + 1
    var['ol'] = ol
    if delete == 'False':
        k = 0
        for i in data:
            if i['link'] == var['link']:
                k = 1
                break
        if k == 0:
            data.append(var)
    else:
        for i in data:
            if i['ol'] == var['ol']:
                data.remove(i)
    f = open(f'static/izb/{current_user.name}.json', 'w', encoding='utf-8')
    json.dump(data, f)
    f.close()
    if redir == 'False':
        return render_template('close.html')
    else:
        return redirect('/profile')


if __name__ == '__main__':
    main()