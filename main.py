import flask
from flask import *
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm, SearchForm
from flask_login import *
from test import Ozon_items
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

def main():
    db_session.global_init("db/blogs.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def start():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search', text=form.search_line.data, filters='По популярности'))
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
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
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
    text = request.args.get('text').strip()
    filters = request.args.get('filters').strip()
    print(filters)
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
    k = Ozon_items(f'https://www.ozon.ru/search/?from_global=true&text={text}&sorting={oz_filt}')
    s = k.lib
    if sort:
        s.sort(key=kek, reverse=rev)
    return render_template('place.html', lil=s, title='Резултаты запроса', text=text, filters=filters, ost=ol)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    main()