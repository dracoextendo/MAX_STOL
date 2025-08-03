document.addEventListener('DOMContentLoaded', function() {
  // Получаем модальное окно
  const modal = document.getElementById("orderModal");

  // Получаем элемент span, который закрывает модальное окно
  const span = document.getElementsByClassName("close")[0];

  // Когда пользователь нажимает на кнопку закрытия - закрываем модальное окно
  span.onclick = function() {
    modal.style.display = "none";
  }

  // Когда пользователь кликает вне модального окна - закрываем его
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

  // Обработчики для всех кнопок просмотра
  document.querySelectorAll('[id^="look-btn-"]').forEach(button => {
    button.addEventListener('click', function() {
      const orderId = this.id.replace('look-btn-', '');

      const orderData = getOrderData(orderId); // Эта функция должна возвращать данные заказа

      if (orderData) {
        // Заполняем модальное окно данными
        document.getElementById('modal-order-id').textContent = orderData.id;
        document.getElementById('modal-username').textContent = orderData.username;
        document.getElementById('modal-phone').textContent = orderData.phone;
        document.getElementById('modal-email').textContent = orderData.email || 'не указан';
        document.getElementById('modal-telegram').textContent = orderData.telegram || 'не указан';
        document.getElementById('modal-product-name').textContent = orderData.product_name;
        document.getElementById('modal-desk-color').textContent = orderData.desk_color;
        document.getElementById('modal-frame-color').textContent = orderData.frame_color;
        document.getElementById('modal-depth').textContent = orderData.depth;
        document.getElementById('modal-length').textContent = orderData.length;
        document.getElementById('modal-created-at').textContent = orderData.created_at;
        document.querySelector('button.del-btn').id = orderData.id;

        // Показываем модальное окно
        modal.style.display = "block";
      }
    });
  });

  // Функция для получения данных заказа (замените на реальную реализацию)
  function getOrderData(orderId) {
    const row = document.querySelector(`tr:has(#look-btn-${orderId})`);
    if (!row) return null;

    // В реальном приложении лучше использовать AJAX или хранить данные в JS объекте
    return {
      id: orderId,
      username: row.cells[1].textContent,
      phone: row.cells[2].textContent,
      email: row.cells[3].textContent,
      telegram: row.cells[4].textContent,
      product_name: row.cells[5].textContent,
      desk_color: row.cells[7].textContent,
      frame_color: row.cells[8].textContent,
      depth: row.cells[9].textContent,
      length: row.cells[10].textContent,
      created_at: row.cells[6].textContent,
    };
  }
});

function deleteOrder(deleteButton) {
    const orderId = deleteButton.id;
    // Проверяем, точно ли мы хотим удалить заказ
    if (!confirm(`Вы уверены, что хотите удалить заказ #${orderId}?`)) {
        return;
    }

    // Отправляем DELETE запрос на сервер
    fetch(`/orders/${orderId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            // Добавьте другие заголовки, если нужно (например, для авторизации)
            // 'Authorization': 'Bearer YOUR_TOKEN'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при удалении заказа');
        }
        return response.json();
    })
    .then(data => {
        // Если запрос выполнен успешно, перезагружаем страницу
        alert(`Заказ #${orderId} успешно удален`);
        window.location.reload();
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при удалении заказа');
        window.location.reload();
    });
}