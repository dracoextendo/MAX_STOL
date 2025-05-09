const dialog = document.getElementById('orderDialog')
const dialogOpener = document.querySelectorAll('.openDialogBtn')
const dialogCloser = dialog.querySelector('.closeDialogBtn')
const origin = window.location.origin 

async function openModalAndLockScroll() {
  const apiData = await getData(this.id);
  const img1 = dialog.querySelector(".img1")
  const img2 = dialog.querySelector(".img2")
  const img3 = dialog.querySelector(".img3")
  const deskColorInputs = dialog.querySelector(".desk-color > .radio-buttons")
  deskColorInputs.innerHTML = '';
  apiData.desk_colors.forEach(deskColor=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "desk-color";
    radio.value = deskColor;
    radio.id = `color-${deskColor}`; //нужна доработка api

    const label = document.createElement("label");
    label.htmlFor = `color-${deskColor}`; // Связь с радио-кнопкой
    label.textContent = deskColor;
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    deskColorInputs.appendChild(radio);
    deskColorInputs.appendChild(label);
  });    
  





  const frameColorInputs = dialog.querySelector(".frame-color > .radio-buttons")
  const depthInputs = dialog.querySelector(".depth > .radio-buttons")
  const lenghtInputs = dialog.querySelector(".lenght > .radio-buttons")
   // Ждём загрузки данных
  console.log(apiData); // Теперь данные будут здесь
  img1.setAttribute("src", apiData.product.first_image)
  img2.setAttribute("src", apiData.product.second_image)
  img3.setAttribute("src", apiData.product.third_image)
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


async function getData(productId) {
   // 2. Делаем запрос к API и ждем ответ (await)
   const response = await fetch(`${origin}/product/${productId}`);
  
   // 3. Преобразуем ответ в JSON-формат (если API возвращает JSON)
   const data = await response.json();
   
   // 4. Возвращаем полученные данные
   return data;
  
}