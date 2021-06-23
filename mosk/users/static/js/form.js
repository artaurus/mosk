function _length(field, min, max) {
  if (field.value.length < min || field.value.length > max) {
    return false;
  } else {
    return true;
  }
}

function _fail(field) {
  var red = '#d11a2a';
  field.style.border = `${red} solid 1px`;
  field.style.boxShadow = `0 0 2px ${red}`;
  return false;
}

function _pass(field) {
  var green = '#00ab66';
  field.style.border = `${green} solid 1px`;
  field.style.boxShadow = `0 0 2px ${green}`;
  document.getElementById(`${field.name}-error`).innerText = '';
  return true;
}

function validate(form, field_validators, ind=[]) {
  var flags = [];
  for (var i=0; i < field_validators.length; i++) {
    if (ind.includes(i)) {
      flags[i] = true;
    } else {
      flags[i] = false;
    }
  }

  field_validators.forEach((fv, i) => {
    var field = form[fv[0]];
    field.addEventListener('change', () => {
      var subflag1 = _length(field, fv[1], fv[2]);
      var subflag2 = fv[3].test(field.value);
      if (subflag1 && subflag2) {
        flags[i] = _pass(field);
      } else if (field.value) {
        flags[i] = _fail(field);
        switch (field.name) {
          case 'email':
            document.getElementById('email-error').innerText = 'Invalid email address.';
            break;
          case 'password':
            document.getElementById('password-error').innerText = 'Allowed characters: a-z, A-Z, 0-9, and _.';
            break;
          default:
            document.getElementById(`${field.name}-error`).innerText = `Invalid characters in ${field.name}.`;
        }
        if (subflag2) {
          document.getElementById(`${field.name}-error`).innerText = `Has to be between ${fv[1]} and ${fv[2]} characters.`;
        }
      } else if (!ind.includes(i)) {
        flags[i] = _fail(field);
      } else {
        flags[i] = _pass(field);
      }
      var confirm = field.name.split('_');
      if (confirm[0] == 'confirm') {
        if (field.value == form[confirm[1]].value) {
          flags[i] = _pass(field);
        } else {
          flags[i] = _fail(field);
          document.getElementById(`${field.name}-error`).innerText = `Does not match ${confirm[1]}.`;
        }
      }
    });
  });

  form.addEventListener('submit', event => {
    field_validators.forEach((fv, i) => {
      var field = form[fv[0]];
      if (!field.value.trim().length) {
        flags[i] = _fail(field);
      }
    });
    if (flags.includes(false)) {
      event.preventDefault();
    }
  });
}
