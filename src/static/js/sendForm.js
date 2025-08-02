///////////////////////////////////////ВСПЛЫВАШКА НА ОТПРАВКУ ФОРМЫ//////////////////////////////////////////////
const modal = document.getElementById('modal');
const openBtn = document.getElementById('openModal');
const closeBtn = document.getElementById('closeModal');

openBtn.addEventListener('click', () => {
  modal.classList.add('show');
});

closeBtn.addEventListener('click', () => {
  modal.classList.remove('show');
});

///////////////////////////////////////////////////////////////////////////////////////////////////////