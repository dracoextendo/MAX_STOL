const upBtn = document.getElementById('upBtn');

window.addEventListener('scroll', () => {
  upBtn.classList.toggle('show', window.scrollY > 300);
});

upBtn.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth' 
  });
});