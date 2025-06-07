document.addEventListener('DOMContentLoaded', function() {
  function isMobile() {
    return window.innerWidth <= 768;
  }

  const cards = document.querySelectorAll('.card');
  
  function setupSlider(card) {
    const cardPics = card.querySelector('.card-pics');
    const images = card.querySelectorAll('.cardImg');
    if (images.length <= 1) return;

    let currentIndex = 0;
    let startX = 0;
    let endX = 0;
    const threshold = 50;

    function showAllImages() {
      images.forEach(img => {
        img.style.display = 'block';
        img.style.opacity = '1';
      });
    }

    function initSlider() {
      images.forEach((img, index) => {
        img.style.display = index === 0 ? 'block' : 'none';
        img.style.transition = 'opacity 0.3s ease';
      });
    }

    function showSlide(index) {
      if (index >= images.length) index = 0;
      if (index < 0) index = images.length - 1;
      
      images.forEach(img => img.style.display = 'none');
      images[index].style.display = 'block';
      currentIndex = index;
    }

    function handleTouchStart(e) {
      startX = e.touches[0].clientX;
    }

    function handleTouchMove(e) {
      endX = e.touches[0].clientX;
      if (Math.abs(startX - endX) > 10) {
        e.preventDefault();
      }
    }

    function handleTouchEnd() {
      const diffX = startX - endX;
      if (diffX > threshold) {
        showSlide(currentIndex + 1);
      } else if (diffX < -threshold) {
        showSlide(currentIndex - 1);
      }
    }

    // Инициализация в зависимости от размера экрана
    if (isMobile()) {
      initSlider();
      cardPics.addEventListener('touchstart', handleTouchStart, {passive: true});
      cardPics.addEventListener('touchmove', handleTouchMove, {passive: false});
      cardPics.addEventListener('touchend', handleTouchEnd);
    } else {
      showAllImages();
    }
  }

  // Обработчик изменения размера окна
  function handleResize() {
    cards.forEach(card => {
      const images = card.querySelectorAll('.cardImg');
      if (isMobile()) {
        images.forEach((img, index) => {
          img.style.display = index === 0 ? 'block' : 'none';
        });
      } else {
        images.forEach(img => {
          img.style.display = 'block';
        });
      }
    });
  }

  // Инициализация всех карточек
  cards.forEach(setupSlider);
  
  // Отслеживание изменения размера окна
  window.addEventListener('resize', function() {
    clearTimeout(window.resizingTimer);
    window.resizingTimer = setTimeout(handleResize, 100);
  });
});