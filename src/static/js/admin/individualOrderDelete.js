function deleteIndividualOrder(deleteButton) {
    const orderId = deleteButton.id;
    // Проверяем, точно ли мы хотим удалить заказ
    if (!confirm(`Вы уверены, что хотите удалить заказ #${orderId}?`)) {
        return;
    }

    // Отправляем DELETE запрос на сервер
    fetch(`/individual-orders/${orderId}`, {
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