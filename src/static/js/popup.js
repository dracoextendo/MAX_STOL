const dialog = document.getElementById('orderDialog')
const dialogOpener = document.querySelectorAll('.openDialogBtn')
const dialogCloser = dialog.querySelector('.closeDialogBtn')
const img1 = dialog.querySelector(".img1")

async function openModalAndLockScroll() {
  const apiData = await getData(); // Ждём загрузки данных
  console.log(apiData.message); // Теперь данные будут здесь
  img1.setAttribute("src",apiData.message)
  dialog.showModal();
  document.body.classList.add('scroll-lock');
}

function returnScroll() {
  document.body.classList.remove('scroll-lock')
}

function close() {
  dialog.close()
  returnScroll()
}

function closeOnBackDropClick({ currentTarget, target }) {
  const dialog = currentTarget
  const isClickedOnBackDrop = target === dialog
  if (isClickedOnBackDrop) {
    close()
  }
}

dialogCloser.addEventListener('click', close)
dialogOpener.forEach(opener => {
  opener.addEventListener('click', openModalAndLockScroll);
});

dialog.addEventListener('click', closeOnBackDropClick)
dialog.addEventListener('cancel', (event) => {
  returnScroll()
});


async function getData() {
   // 2. Делаем запрос к API и ждем ответ (await)
   const response = await fetch("https://dog.ceo/api/breeds/image/random");
  
   // 3. Преобразуем ответ в JSON-формат (если API возвращает JSON)
   const data = await response.json();
   
   // 4. Возвращаем полученные данные
   return data;
  
}