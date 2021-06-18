from flask import render_template, redirect, request, url_for, flash, abort
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import SignatureExpired
from mosk import app, mail, bcrypt, um
from mosk.users import users
from mosk.users.models import User
from mosk.users.forms import SignUpForm, LoginForm, EditProfileForm, EmailForm, ResetPasswordForm
from random import randint

code = randint(1000, 9999)

def get_token(email, expires=300):
    s = Serializer(app.config['SECRET_KEY'], expires)
    global code
    return s.dumps({'email': email, 'code': code}).decode('utf-8')

def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        global code
        if s.loads(token)['code'] == code:
            return s.loads(token)['email']
        else:
            raise SignatureExpired('Signature has expired.')
    except SignatureExpired:
        abort(404)

@users.route('/')
@um.access_required
def account():
    return render_template(
        'account.html',
        title='Account',
        um=um
    )

@users.route('/sign_up', methods=['GET', 'POST'])
@um.access_restricted
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed)
        user.save()
        um.set_user(user)
        verify(form.email.data)
        return redirect(url_for('gen.home'))
    return render_template(
        'sign_up.html',
        title='Sign Up',
        um=um,
        form=form
    )

def verify(email):
    token = get_token(email)
    msg = Message('Verify your account', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'''
To verify your account, click on the following link:

{url_for('users.verify2', token=token, _external=True)}'''
    mail.send(msg)
    flash('An email has been sent with a link to verify your account.')

@users.route('/verify')
@um.access_required
def verify1():
    verify(um.get_user('email'))
    return redirect(url_for('users.account'))

@users.route('/verify/<token>')
def verify2(token):
    email = verify_token(token)
    user = User.objects(email=email).first()
    user.verified = True
    user.save()
    global code
    code = randint(1000, 9999)
    if um.status():
        um.reset_user()
        um.set_user(user)
    flash('Your account has been verified.')
    return redirect(url_for('gen.home'))

@users.route('/login', methods=['GET', 'POST'])
@um.access_restricted
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=form.email.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            um.set_user(user)
            return redirect(url_for('users.account'))
        else:
            return redirect(url_for('users.login'))
    return render_template(
        'login.html',
        title='Login',
        um=um,
        form=form
    )

@users.route('/edit', methods=['GET', 'POST'])
@um.access_required
def edit_account():
    form = EditProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=um.get_user('email')).first()
        if form.email.data != user.email:
            verify(form.email.data)
        user.email = form.email.data
        user.save()
        um.reset_user()
        um.set_user(user)
        return redirect(url_for('users.account'))
    return render_template(
        'edit_account.html',
        title='Edit Account',
        um=um,
        form=form
    )

def reset_password(email):
    token = get_token(email)
    msg = Message('Reset your password', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'''
To reset your password, click on the following link:

{url_for('users.reset_password2', token=token, _external=True)}'''
    mail.send(msg)
    flash('An email has been sent with a link to reset your password.')

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password1():
    if um.status():
        reset_password(um.get_user('email'))
        return redirect(url_for('users.logout'))
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        reset_password(form.email.data)
        return redirect(url_for('users.reset_password1'))
    return render_template(
        'email.html',
        title='Reset password',
        um=um,
        form=form
    )

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password2(token):
    email = verify_token(token)
    user = User.objects(email=email).first()
    if not user:
        flash('Account does not exist in our database.')
        return redirect(url_for('users.reset_password1'))
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.save()
        um.set_user(user)
        global code
        code = randint(1000, 9999)
        flash('Password has been reset.')
        return redirect(url_for('gen.home'))
    return render_template(
        'reset_password.html',
        title='Reset password',
        um=um,
        form=form,
        token=token
    )

@users.route('/logout')
@um.access_required
def logout():
    um.reset_user()
    return redirect(url_for('gen.home'))

@users.route('/delete')
@um.access_required
def delete1():
    token = get_token(um.get_user('email'))
    msg = Message('Delete your account', sender=app.config['MAIL_USERNAME'], recipients=[um.get_user('email')])
    msg.body = f'''
To delete your account, click on the following link:

{url_for('users.delete2', token=token, _external=True)}'''
    mail.send(msg)
    flash('An email has been sent with a link to delete your account.')
    return redirect(url_for('users.logout'))

@users.route('/delete/<token>')
def delete2(token):
    email = verify_token(token)
    User.objects(email=email).first().delete()
    global code
    code = randint(1000, 9999)
    flash('Your account has been deleted.')
    return redirect(url_for('gen.home'))
