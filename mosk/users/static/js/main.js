function delete_user() {
  const email = document.querySelector('#delete input');

  const headers = new Headers();
  headers.append('pragma', 'no-cache');
  headers.append('cache-control', 'no-cache');

  fetch('users/static/js/user.json', {
    method: 'GET',
    headers: headers,
  })
    .then(response => response.json())
    .then(user => {
      if (email.value == user.email) {
        location.pathname = '/delete'
      } else {
        location.reload()
      }
    })
    .catch(error => console.log(error));
}

function toggle_delete(toggle) {
  const hidden =  document.getElementById('delete');
  if (toggle) {
    hidden.style.display = 'none';
    return 0;
  } else {
    hidden.style.display = 'block';
    return 1;
  }
}

const d_btn = document.getElementById('delete-btn');
let toggle = 0;
if (d_btn) {
  d_btn.addEventListener('click', () => toggle = toggle_delete(toggle));
}

const confirm =  document.getElementById('confirm');
if (confirm) {
  confirm.addEventListener('click', () => delete_user());
}