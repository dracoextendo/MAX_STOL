  const formValidation = {
    fullname: false,
    phone: false,
    email: true, // email необязательное, по умолчанию валидно
    telegram: true // telegram не проверяем
  };

  $(document).ready(function() {
    $('input[name="phone"]').inputmask("+7 (999) 999-99-99", {
      placeholder: "_", // символ-заполнитель
    });
  });

  
  function validateFullName(input) {
    const title = input.closest('.order-user-field').querySelector('.field-title');
    const value = input.value.trim();
    const isValid = value.length >= 2 && value.length <= 255;
    
    input.classList.toggle('invalid', !isValid);
    title.classList.toggle('invalid', !isValid);
    formValidation.fullname = isValid;
    checkFormValidity();
  }

  function validatePhone(input) {
    const title = input.closest('.order-user-field').querySelector('.field-title');
    const digits = input.value.replace(/\D/g, '');
    const isValid = digits.length === 11;
    
    input.classList.toggle('invalid', !isValid);
    title.classList.toggle('invalid', !isValid);
    formValidation.phone = isValid;
    checkFormValidity();
  }

  function validateEmail(input) {
    const title = input.closest('.order-user-field').querySelector('.field-title');
    const value = input.value.trim();
    const isValid = value === '' || /^[^@]+@[^@]+\.[^@]+$/.test(value);
    
    input.classList.toggle('invalid', !isValid);
    title.classList.toggle('invalid', !isValid);
    formValidation.email = isValid;
    checkFormValidity();
  }

  // Функция проверки всей формы
  function checkFormValidity() {
    const submitBtn = document.getElementById('submitOrderBtn');
    const isValid = Object.values(formValidation).every(Boolean);
    submitBtn.disabled = !isValid;
  }

  function checkFormValidity() {
    const submitBtn = document.getElementById('submitOrderBtn');
    const isValid = Object.values(formValidation).every(Boolean);
    submitBtn.disabled = !isValid;
  }
