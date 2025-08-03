///////////////////////////////////////////////////////////////////ВСЕ ПЕРЕМЕНННЫЕ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
const orderDialog = document.getElementById('orderDialog')
const orderDialogOpener = document.querySelectorAll('.openDialogBtn')
const orderDialogCloser = orderDialog.querySelector('.closeDialogBtn')
const origin = window.location.origin


//////////////////////////////////////////////////////// ОСНОВНОЙ ПОПАП (КАРТОЧКА ТОВАРА + API + JSON)////////////////////////////////////////////////////////////////////////////////
async function openModalAndLockScroll() {
  document.body.classList.add('scroll-lock');
  const apiData = await getData(this.id);
  const img1 = orderDialog.querySelector(".img1")
  const deskColorInputs = orderDialog.querySelector(".desk-color > .radio-buttons")
  const frameColorInputs = orderDialog.querySelector(".frame-color > .radio-buttons")
  const depthInputs = orderDialog.querySelector(".depth > .radio-buttons")
  const lengthInputs = orderDialog.querySelector(".length > .radio-buttons")
  const productName = orderDialog.querySelector(".product-description > h4")
  const productDescription = orderDialog.querySelector(".product-description > p")
  const productPrice = orderDialog.querySelector(".product-price > h4")

  deskColorInputs.innerHTML = '';
  frameColorInputs.innerHTML = '';
  depthInputs.innerHTML = '';
  lengthInputs.innerHTML = '';
  productName.textContent = apiData.product.name 
  productDescription.textContent = apiData.product.description 
  productPrice.textContent = apiData.product.price + " руб."

  apiData.desk_colors.forEach((deskColor, index)=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "desk-color";
    radio.value = deskColor.name;
    radio.id = `desk-color-${deskColor.id}`;

    if (index === 0) {
        radio.checked = true;
    }

    const label = document.createElement("label");
    label.htmlFor = `desk-color-${deskColor.id}`; // Связь с радио-кнопкой
    label.textContent = deskColor.name;
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    deskColorInputs.appendChild(radio);
    deskColorInputs.appendChild(label);
  });

  apiData.frame_colors.forEach((frameColor, index)=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "frame-color";
    radio.value = frameColor.name;
    radio.id = `frame-color-${frameColor.id}`;

    if (index === 0) {
        radio.checked = true;
    }

    const label = document.createElement("label");
    label.htmlFor = `frame-color-${frameColor.id}`; // Связь с радио-кнопкой
    label.textContent = frameColor.name;
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    frameColorInputs.appendChild(radio);
    frameColorInputs.appendChild(label);
  });

  apiData.depth.forEach((depth, index)=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "depth";
    radio.value = depth.value;
    radio.id = `depth-${depth.id}`;

    if (index === 0) {
        radio.checked = true;
    }

    const label = document.createElement("label");
    label.htmlFor = `depth-${depth.id}`; // Связь с радио-кнопкой
    label.textContent = depth.value + " см";
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    depthInputs.appendChild(radio);
    depthInputs.appendChild(label);
  });

  apiData.length.forEach((length, index)=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "length";
    radio.value = length.value;
    radio.id = `length-${length.id}`;

    if (index === 0) {
        radio.checked = true;
    }

    const label = document.createElement("label");
    label.htmlFor = `length-${length.id}`; // Связь с радио-кнопкой
    label.textContent = length.value + " см";
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    lengthInputs.appendChild(radio);
    lengthInputs.appendChild(label);
  });

  img1.setAttribute("src", apiData.product.first_image)
  orderDialog.showModal();
}

function returnScroll() {
  document.body.classList.remove('scroll-lock')
}

function close() {
  orderDialog.close()
  returnScroll()
}

function closeOnBackDropClick({ currentTarget, target }) {
  const dialog = currentTarget
  const isClickedOnBackDrop = target === dialog
  if (isClickedOnBackDrop) {
    close()
  }
}

orderDialogCloser.addEventListener('click', close)
orderDialogOpener.forEach(opener => {
  opener.addEventListener('click', openModalAndLockScroll);
});

orderDialog.addEventListener('click', closeOnBackDropClick)
orderDialog.addEventListener('cancel', (event) => {
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