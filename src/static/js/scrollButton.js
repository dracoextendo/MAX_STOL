const btn = document.getElementById('upBtn');

window.addEventListener('scroll', () => {
  btn.classList.toggle('show', window.scrollY > 300);
});

btn.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth' 
  });
});