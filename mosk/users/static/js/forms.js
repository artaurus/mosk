class Form {
  constructor(form) {
    this.form = form;
  }

  _length(field, min, max) {
    if (field.value.trim().length < min || field.value.trim().length > max) {
      return false;
    } else {
      return true;
    }
  }

  _pass(field) {
    var green = '#00ab66';
    field.style.border = `${green} solid 1px`;
    field.style.boxShadow = `0 0 2px ${green}`;
    document.getElementById(`${field.name}-error`).innerText = '';
    return true;
  }

  _fail(field) {
    var red = '#d11a2a';
    field.style.border = `${red} solid 1px`;
    field.style.boxShadow = `0 0 2px ${red}`;
    return false;
  }

  validate(validators) {
    var flags = [];
    for (var i=0; i < validators.length; i++) {
      flags[i] = !validators[i]['required'];
    }

    validators.forEach((fv, i) => {
      var field = this.form[fv['name']];
      if (fv['default']) {
        field.value = fv['default'];
        flags[i] = this._pass(field);
      }
      field.addEventListener('change', () => {
        var subflag1 = this._length(field, fv['length'][0], fv['length'][1]);
        var subflag2 = fv['regex'].test(field.value);
        if (subflag1 && subflag2) {
          flags[i] = this._pass(field);
        } else if (field.value.trim().length) {
          flags[i] = this._fail(field);
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
          if (!subflag1) {
            document.getElementById(`${field.name}-error`).innerText = `Has to be between ${fv['length'][0]} and ${fv['length'][1]} characters.`;
          }
        } else {
          if (fv['required']) {
            flags[i] = this._fail(field);
          } else {
            flags[i] = this._pass(field);
          }
        }
        var confirm = field.name.split('_');
        if (confirm[0] == 'confirm') {
          if (field.value == this.form[confirm[1]].value) {
            flags[i] = this._pass(field);
          } else {
            flags[i] = this._fail(field);
            document.getElementById(`${field.name}-error`).innerText = `Does not match ${confirm[1]}.`;
          }
        }
        confirm = this.form[`confirm_${field.name}`];
        if (confirm && confirm.value) {
          if (field.value == confirm.value) {
            flags[i+1] = this._pass(confirm);
          } else {
            flags[i+1] = this._fail(confirm);
            document.getElementById(`confirm_${field.name}-error`).innerText = `Does not match ${field.name}.`;
          }
        }
      });
    });

    this.form.addEventListener('submit', event => {
      validators.forEach((fv, i) => {
        var field = this.form[fv['name']];
        if (flags[i]) {
          flags[i] = this._pass(field);
        } else {
          flags[i] = this._fail(field);
        }
      });
      if (flags.includes(false)) {
        event.preventDefault();
      }
    });
  }
}
