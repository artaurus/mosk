const getUser = () =>
  fetch('/account/users/static/js/user.json', {cache: 'no-cache'})
    .then(response => response.json());

var email = {
  'name': 'email',
  'length': [4, 254],
  'regex': /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+$/,
  'required': true,
  'default': null
}
var password = {
  'name': 'password',
  'length': [8, 20],
  'regex': /^[a-zA-Z0-9_]+$/,
  'required': true,
  'default': null
}
var confirm_password = {
  'name': 'confirm_password',
  'length': [8, 20],
  'regex': /^[a-zA-Z0-9_]+$/,
  'required': true,
  'default': null
};

const sign_up = document.forms['sign-up'];
if (sign_up) {
  new Form(sign_up).validate([email, password, confirm_password]);
}

const edit_account = document.forms['edit-account'];
if (edit_account) {
  getUser().then(user => {
    email.default = user.email;
    new Form(edit_account).validate([email]);
  });
}

const reset_password = document.forms['reset-password'];
if (reset_password) {
  new Form(reset_password).validate([password, confirm_password]);
}
