document.querySelectorAll('a').forEach(i => {
  i.style.textDecoration = 'none';
  i.style.color = '#000';
  i.style.fontWeight = 'bold';
});

const submit = document.querySelector('.submit');
if (submit) {
  submit.style.display = 'none';
}
const search = document.getElementById('search');
if (search) {
  search.addEventListener('mouseover', () => search.style.cursor = 'pointer');
  search.addEventListener('click', () => {
    document.querySelector('.search').style.display = 'none';
    document.querySelector('.submit').style.display = 'block';
  });
}
