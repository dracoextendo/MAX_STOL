async function submitForm(event) {

  // Собираем данные формы
  const formData = new FormData();
  const form = document.getElementById('orderForm')

  formData.append('username', form.querySelector('input[name="fullname"]').value);
  formData.append('phone', form.querySelector('input[name="phone"]').value);
  if (form.querySelector('input[name="email"]').value != '') {
    formData.append('email', form.querySelector('input[name="email"]').value);
  }
  if (form.querySelector('input[name="telegram"]').value != '') {
    formData.append('telegram', form.querySelector('input[name="telegram"]').value);
  }
  formData.append('product_name', document.querySelector('.product-description > h4').textContent);
  formData.append('desk_color', form.querySelector('input[name="desk-color"]:checked').value);
  formData.append('frame_color', form.querySelector('input[name="frame-color"]:checked').value);
  formData.append('depth', form.querySelector('input[name="depth"]:checked').value);
  formData.append('length', form.querySelector('input[name="length"]:checked').value);

  try {
    const response = await fetch(`${origin}/orders/add`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`);
    }

    const result = await response.json();

    const modal = document.getElementById('modal');
    const closeModalBtn = modal.querySelector('#closeModal');

    // Убираем старые классы анимации
    modal.classList.remove('animate__fadeOutRight');
    modal.classList.add('animate__animated', 'animate__fadeInRight');
    modal.style.display = 'block';

    const closeModal = () => {
        modal.classList.remove('animate__fadeInRight');
        modal.classList.add('animate__fadeOutRight');

        // Ждём завершения анимации, затем скрываем
        modal.addEventListener('animationend', function handler() {
            modal.style.display = 'none';
            modal.classList.remove('animate__animated', 'animate__fadeOutRight');
            modal.removeEventListener('animationend', handler);
        });
    };

    closeModalBtn.addEventListener('click', closeModal);

    // Автоматическое закрытие через 3 секунды
    setTimeout(closeModal, 5000);

    form.reset();
    formValidation.email = true;
    formValidation.fullname = false;
    formValidation.phone = false;
    checkFormValidity();
    close();

} catch (error) {
    console.error('Ошибка:', error);
    alert('Произошла ошибка при отправке заказа: ' + error.message);
}

}

