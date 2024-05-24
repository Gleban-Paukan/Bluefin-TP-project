// Функция для загрузки и отображения содержимого корзины
function loadCartItems() {
    const cartItemsEl = document.getElementById('cart-items');
    const totalPriceEl = document.getElementById('total-price');

    // Извлекаем данные корзины из localStorage
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    let total = 0;
    cartItemsEl.innerHTML = ''; // Очищаем текущее содержимое корзины

    cart.forEach(item => {
        // Создаем и наполняем элемент корзины
        const itemEl = document.createElement('div');
        itemEl.className = 'cart-item';
        itemEl.innerHTML = `
            <img src="../static/images/${item.imagePath}" alt="${item.name}" class="item-image">
            <div class="item-info">
                <span class="item-name">${item.name}</span>
                <span class="item-price">${item.quantity} x ${item.price} ₽</span>
            </div>
            <div class="quantity-controls">
                <button class="decrease-quantity" onclick="decreaseQuantity('${item.name}')">-</button>
                <span class="quantity">${item.quantity}</span>
                <button class="increase-quantity" onclick="increaseQuantity('${item.name}')">+</button>
                <button class="remove-item" onclick="removeFromCart('${item.name}')">Удалить</button>
            </div>
        `;
        cartItemsEl.appendChild(itemEl);

        total += item.price * item.quantity;
    });

    totalPriceEl.innerText = `Итого: ${formatNumber(total)} ₽`;
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

// Вызываем функцию при загрузке страницы
document.addEventListener('DOMContentLoaded', loadCartItems);

// Функции для управления корзиной
function removeFromCart(itemName) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart = cart.filter(item => item.name !== itemName);
    localStorage.setItem('cart', JSON.stringify(cart));
    loadCartItems();
}

function increaseQuantity(itemName) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const item = cart.find(item => item.name === itemName);
    if (item) {
        item.quantity++;
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    loadCartItems();
}

function decreaseQuantity(itemName) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const item = cart.find(item => item.name === itemName);
    if (item && item.quantity > 1) {
        item.quantity--;
    } else if (item) {
        cart = cart.filter(item => item.name !== itemName);
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    loadCartItems();
}

document.getElementById('orderButton').addEventListener('click', function () {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const telegramUserId = localStorage.getItem('UserId');

    fetch('https://glebanpaukan.pythonanywhere.com/make_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cart: cart, telegramUserId: telegramUserId }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
//        Telegram.WebApp.close(); // Закрыть окно Telegram после успешного ответа
    })
    .catch(error => console.error('Error:', error));
});