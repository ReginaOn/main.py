from flask import Flask, render_template, url_for, redirect
from data import db_session
from data.users import User
from data.registerForm import RegisterForm
from data.loginForm import LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required
db_session.global_init("db/blogs.sqlite")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def bootstrap():
    return render_template('first.html')


@app.route('/magazin')
def mag():
    return render_template('magazin.html')


@app.route('/personal')
def person():
    return render_template('personal.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registr', methods=['GET', 'POST'])
def reqistr():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registr.html', title='Регистрация',form=form, message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('registr.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('registr.html', title='Регистрация', form=form)



if __name__ == "__main__":
    db_session.global_init("db/blogs.sqlite")
    app.run()

