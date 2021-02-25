const search = document.getElementById('search');
if (search) {
  search.addEventListener('mouseover', () => search.style.cursor = 'pointer');
  search.addEventListener('click', () => {
    document.querySelector('.search').style.display = 'none';
    document.querySelector('.submit').style.display = 'block';
  });
}
