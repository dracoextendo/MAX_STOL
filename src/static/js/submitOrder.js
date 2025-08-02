async function submitForm(event) {

  // Собираем данные формы
  const formData = new FormData();
  const form = document.getElementById('orderForm')

  formData.append('username', form.querySelector('input[name="fullname"]').value);
  formData.append('phone', form.querySelector('input[name="phone"]').value);
  formData.append('email', form.querySelector('input[name="email"]').value || null);
  formData.append('telegram', form.querySelector('input[name="telegram"]').value || null);
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
        modal.style.display = 'block';

        setTimeout(() => {
        modal.style.display = 'none';
        }, 3000);

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

