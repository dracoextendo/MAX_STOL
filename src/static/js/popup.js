///////////////////////////////////////////////////////////////////ВСЕ ПЕРЕМЕНННЫЕ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
const dialog = document.getElementById('orderDialog')
const dialogOpener = document.querySelectorAll('.openDialogBtn')
const dialogCloser = dialog.querySelector('.closeDialogBtn')
const origin = window.location.origin
let open_modal = document.querySelectorAll('.open_modal');
let close_modal = document.getElementById('close_modal');
let modal = document.getElementById('modal');
let body = document.getElementsByTagName('body')[0]; 


//////////////////////////////////////////////////////// ОСНОВНОЙ ПОПАП (КАРТОЧКА ТОВАРА + API + JSON)////////////////////////////////////////////////////////////////////////////////

async function openModalAndLockScroll() {
  const apiData = await getData(this.id);
  const img1 = dialog.querySelector(".img1")
  const img2 = dialog.querySelector(".img2")
  const img3 = dialog.querySelector(".img3")
  const deskColorInputs = dialog.querySelector(".desk-color > .radio-buttons")
  const frameColorInputs = dialog.querySelector(".frame-color > .radio-buttons")
  const depthInputs = dialog.querySelector(".depth > .radio-buttons")
  const lengthInputs = dialog.querySelector(".length > .radio-buttons")
  const productInput = dialog.querySelector("input[type=text]")

  deskColorInputs.innerHTML = '';
  frameColorInputs.innerHTML = '';
  depthInputs.innerHTML = '';
  lengthInputs.innerHTML = '';
  productInput.value = apiData.product.name

  apiData.desk_colors.forEach(deskColor=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "desk-color";
    radio.value = deskColor.name;
    radio.id = `desk-color-${deskColor.id}`;

    const label = document.createElement("label");
    label.htmlFor = `desk-color-${deskColor.id}`; // Связь с радио-кнопкой
    label.textContent = deskColor.name;
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    deskColorInputs.appendChild(radio);
    deskColorInputs.appendChild(label);
  });

  apiData.frame_colors.forEach(frameColor=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "frame-color";
    radio.value = frameColor.name;
    radio.id = `frame-color-${frameColor.id}`;

    const label = document.createElement("label");
    label.htmlFor = `frame-color-${frameColor.id}`; // Связь с радио-кнопкой
    label.textContent = frameColor.name;
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    frameColorInputs.appendChild(radio);
    frameColorInputs.appendChild(label);
  });

  apiData.depth.forEach(depth=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "depth";
    radio.value = depth.value;
    radio.id = `depth-${depth.id}`;

    const label = document.createElement("label");
    label.htmlFor = `depth-${depth.id}`; // Связь с радио-кнопкой
    label.textContent = depth.value + " см";
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    depthInputs.appendChild(radio);
    depthInputs.appendChild(label);
  });

  apiData.length.forEach(length=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "length";
    radio.value = length.value;
    radio.id = `length-${length.id}`;

    const label = document.createElement("label");
    label.htmlFor = `length-${length.id}`; // Связь с радио-кнопкой
    label.textContent = length.value + " см";
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    lengthInputs.appendChild(radio);
    lengthInputs.appendChild(label);
  });

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
   const response = await fetch(`${origin}/products/${productId}`);
  
   // 3. Преобразуем ответ в JSON-формат (если API возвращает JSON)
   const data = await response.json();
   
   // 4. Возвращаем полученные данные
   return data;
  }
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////