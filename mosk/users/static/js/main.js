const getUser = () =>
  fetch('/account/users/static/js/user.json', {cache: 'no-cache'})
    .then(response => response.json());

const sign_up = document.forms['sign-up'];
if (sign_up) {
  validate(sign_up, [
    ['email', 5, 254, /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$/],
    ['password', 8, 20, /^[a-zA-Z0-9_]+$/],
    ['confirm_password', 8, 20, /^[a-zA-Z0-9_]+$/]
  ]);
}

const edit_account = document.forms['edit-account'];
if (edit_account) {
  getUser().then(user => {
    edit_account['email'].value = user.email;
  });
  validate(edit_account, [
    ['email', 5, 254, /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$/]
  ], [0]);
  document.getElementById('reset').addEventListener('click', () => {
    getUser().then(user => {
      edit_account['email'].value = user.email;
    });
  });
}

const reset_password = document.forms['reset-password'];
if (reset_password) {
  validate(reset_password, [
    ['password', 8, 20, /^[a-zA-Z0-9_]+$/],
    ['confirm_password', 8, 20, /^[a-zA-Z0-9_]+$/]
  ]);
}
