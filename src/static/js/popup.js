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
  const frameColorInputs = dialog.querySelector(".frame-color > .radio-buttons")
  const depthInputs = dialog.querySelector(".depth > .radio-buttons")
  const lengthInputs = dialog.querySelector(".length > .radio-buttons")
  deskColorInputs.innerHTML = '';
  frameColorInputs.innerHTML = '';
  depthInputs.innerHTML = '';
  lengthInputs.innerHTML = '';

  apiData.desk_colors.forEach(deskColor=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "desk-color";
    radio.value = deskColor.color;
    radio.id = `desk-color-${deskColor.id}`;

    const label = document.createElement("label");
    label.htmlFor = `desk-color-${deskColor.id}`; // Связь с радио-кнопкой
    label.textContent = deskColor.color;
    label.className = "checkbox-button"
    // Добавляем radio и label в контейнер (на одном уровне)
    deskColorInputs.appendChild(radio);
    deskColorInputs.appendChild(label);
  });

  apiData.frame_colors.forEach(frameColor=> {
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "frame-color";
    radio.value = frameColor.color;
    radio.id = `frame-color-${frameColor.id}`;

    const label = document.createElement("label");
    label.htmlFor = `frame-color-${frameColor.id}`; // Связь с радио-кнопкой
    label.textContent = frameColor.color;
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
   const response = await fetch(`${origin}/product/${productId}`);
  
   // 3. Преобразуем ответ в JSON-формат (если API возвращает JSON)
   const data = await response.json();
   
   // 4. Возвращаем полученные данные
   return data;
  }


  
// слайдер - баннер 567-768
document.addEventListener('DOMContentLoaded', function() {
  function isMobile() {
    return window.innerWidth <= 768;
  }

  if (isMobile()) {
    const banner = document.querySelector('.banner');
    const slides = document.querySelectorAll('.banner-block');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    let currentSlide = 0;
    let startX = 0;
    let endX = 0;
    const swipeThreshold = 50;

    // Инициализация слайдов
    function initSlides() {
      slides.forEach((slide, index) => {
        slide.style.transition = 'opacity 0.3s ease';
        if (index === 0) {
          slide.style.display = 'flex';
          slide.style.opacity = '1';
          slide.style.zIndex = '1';
        } else {
          slide.style.display = 'none';
          slide.style.opacity = '0';
          slide.style.zIndex = '0';
        }
      });
    }

    // Показать конкретный слайд
    function showSlide(index) {
      if (index >= slides.length) index = 0;
      if (index < 0) index = slides.length - 1;
      
      slides.forEach((slide, i) => {
        if (i === index) {
          slide.style.display = 'flex';
          setTimeout(() => {
            slide.style.opacity = '1';
            slide.style.zIndex = '2'; // Активный слайд выше остальных
          }, 10);
        } else {
          slide.style.opacity = '0';
          slide.style.zIndex = '1';
          setTimeout(() => {
            slide.style.display = 'none';
          }, 300);
        }
      });
      
      dots.forEach(dot => dot.classList.remove('active'));
      dots[index].classList.add('active');
      
      currentSlide = index;
    }

    // Обработчики свайпа (улучшенные)
    banner.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
      endX = startX; // Инициализируем endX
    }, { passive: true });

    banner.addEventListener('touchmove', (e) => {
      endX = e.touches[0].clientX;
      // Блокируем скролл страницы при горизонтальном свайпе
      if (Math.abs(startX - endX) > 10) {
        e.preventDefault();
      }
    }, { passive: false });

    banner.addEventListener('touchend', () => {
      const diffX = startX - endX;
      
      if (diffX > swipeThreshold) {
        showSlide(currentSlide + 1);
      } else if (diffX < -swipeThreshold) {
        showSlide(currentSlide - 1);
      }
    });

    // Остальные обработчики...
    dots.forEach(dot => {
      dot.addEventListener('click', function() {
        const slideIndex = parseInt(this.getAttribute('data-slide'));
        showSlide(slideIndex);
      });
    });

    prevBtn.addEventListener('click', () => showSlide(currentSlide - 1));
    nextBtn.addEventListener('click', () => showSlide(currentSlide + 1));

    // Инициализация
    initSlides();

    // Реакция на изменение размера окна
    window.addEventListener('resize', function() {
      if (!isMobile()) {
        slides[0].style.display = 'flex';
        slides[0].style.opacity = '1';
        slides[1].style.display = 'none';
      } else {
        initSlides();
      }
    });
  }
});