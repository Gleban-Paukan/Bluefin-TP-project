
document.addEventListener('DOMContentLoaded', function() {
    const telegram = window.Telegram.WebApp;

    if (telegram.initDataUnsafe && telegram.initDataUnsafe.user) {
        const userId = telegram.initDataUnsafe.user.id;
        localStorage.setItem('UserId', userId.toString());
    }

    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    function createCartIcon() {
        const cartContainer = document.getElementById('cart-container');

        if (!cartContainer) {
            console.error('Cart container not found!');
            return;
        }

        const cartIcon = document.createElement('div');
        cartIcon.id = 'cart-icon';
        cartIcon.onclick = function() {
            window.location.href = 'templates/cart.html';
        };

        // const cartImage = document.createElement('img');
        // cartImage.src = 'static/images/cart-icon.png'; // Укажите путь к новой иконке
        // cartImage.alt = 'Корзина';
        // cartImage.style.borderRadius = '15px'; // Применяем закругленные края
        // cartIcon.appendChild(cartImage);

        const cartTotal = document.createElement('span');
        cartTotal.id = 'cart-total';
        cartIcon.appendChild(cartTotal);

        cartContainer.appendChild(cartIcon);
    }

    function updateLocalStorage() {
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartTotal();
    }

    function addItemToCart(element) {
        const name = element.getAttribute('data-name');
        const price = Number(element.getAttribute('data-price'));
        const imagePath = element.getAttribute('data-image-path');
        addToCart({ name, price, imagePath });
    }

    function addToCart(item) {
        const existingItem = cart.find(cartItem => cartItem.name === item.name);
        if (existingItem) {
            existingItem.quantity++;
        } else {
            cart.push({
                name: item.name,
                price: item.price,
                imagePath: item.imagePath,
                quantity: 1
            });
        }
        updateLocalStorage();
    }

    function updateCartTotal() {
        let total = 0;
        cart.forEach(item => {
            total += item.price * item.quantity;
        });
        document.getElementById('cart-total').textContent = formatNumber(total) + ' ₽';
    }

    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    }

    createCartIcon(); // Создаем иконку корзины при загрузке страницы
    document.querySelectorAll('.add-to-cart-button').forEach(button => {
        button.addEventListener('click', () => addItemToCart(button));
    });

    updateCartTotal(); // Обновляем сумму в корзине при загрузке страницы
});
