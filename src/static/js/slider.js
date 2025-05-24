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