from flask import redirect, request, url_for

class LoginHandler:
    # initialise with app instance?
    def __init__(self):
        self.reset_user()

    # separate write function
    def set_user(self, user):
        if not self.status():
            del user.password
            self.user = user
            with open('mosk/static/js/user.json', 'w') as file:
                file.write(user.to_json())

    def reset_user(self):
        self.user = {}
        with open('mosk/static/js/user.json', 'w') as file:
            file.write('{}')

    def get_user(self):
        return self.user

    def status(self):
        return bool(self.user)

    def access_required(self, func):
        def wrapper(*args, **kwargs):
            if not self.status():
                return redirect(url_for('login', next=url_for(func.__name__)[1:]))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    def access_denied(self, func):
        def wrapper(*args, **kwargs):
            if self.status():
                # create custom error pages
                return redirect(url_for('home'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
