document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('orderForm');
  const submitBtn = document.getElementById('submitOrderBtn'); // Исправлено: добавлен #
  
  // Удаляем onclick из HTML, так как используем addEventListener
  submitBtn.onclick = null;
  
  createErrorElements();
  
  submitBtn.addEventListener('click', function(e) {
    e.preventDefault();
    let isValid = true;

    // Валидация ФИО
    const fullname = form.querySelector('[name="fullname"]');
    if (!fullname.value.trim() || !/^[а-яА-ЯёЁ\s-]{5,}$/.test(fullname.value.trim())) {
      showError(fullname, 'Введите корректное ФИО (минимум 5 кириллических символов)');
      isValid = false;
    } else {
      clearError(fullname);
    }

    // Валидация телефона
    const phone = form.querySelector('input[type="tel"]');
    if (!/^\+7\d{10}$/.test(phone.value)) {
      showError(phone, 'Введите корректный телефон (+7XXXXXXXXXX)');
      isValid = false;
    } else {
      clearError(phone);
    }

    // Валидация email (первого поля с type="email")
    const email = form.querySelector('input[type="email"]:not([placeholder="@никнейм"])');
    if (email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      showError(email, 'Введите корректный email');
      isValid = false;
    } else {
      clearError(email);
    }

    // Валидация Telegram
    const telegram = form.querySelector('input[placeholder="@никнейм"]');
    if (telegram.value && !/^@[a-zA-Z0-9_]{5,}$/.test(telegram.value)) {
      showError(telegram, 'Введите корректный никнейм (@username, минимум 5 символов)');
      isValid = false;
    } else {
      clearError(telegram);
    }

    if (isValid) {
      alert('Форма успешно отправлена!');
      form.reset();
    }
  });

  function createErrorElements() {
    const fields = form.querySelectorAll('.order-user-field');
    fields.forEach(field => {
      if (!field.querySelector('.error-message')) {
        const errorElement = document.createElement('span');
        errorElement.className = 'error-message';
        field.appendChild(errorElement);
      }
    });
  }

  function showError(input, message) {
    const field = input.closest('.order-user-field');
    const errorElement = field.querySelector('.error-message');
    errorElement.textContent = message;
    input.classList.add('error');
    field.classList.add('has-error');
  }

  function clearError(input) {
    const field = input.closest('.order-user-field');
    const errorElement = field.querySelector('.error-message');
    if (errorElement) {
      errorElement.textContent = '';
      input.classList.remove('error');
      field.classList.remove('has-error');
    }
  }
});