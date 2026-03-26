let cart = JSON.parse(localStorage.getItem('cart')) || [];

function updateCartCount() {
    const countElement = document.querySelector('.cart-count');
    const totalCount = cart.reduce((acc, item) => acc + item.quantity, 0);
    if (countElement) countElement.textContent = totalCount;
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('add-to-cart')) {
        const btn = e.target;
        const id = btn.dataset.id;
        const name = btn.dataset.name;
        const price = parseFloat(btn.dataset.price);

        const existingItem = cart.find(item => item.id === id);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({ id, name, price, quantity: 1 });
        }

        saveCart();

        saveCart();

        // If it's the inline add button, re-render it
        if (btn.classList.contains('inline-add-btn')) {
            renderInlineControls(btn.parentElement, id, name, price);
        } else {
            // Simple feedback for non-inline buttons
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i> Added';
            setTimeout(() => {
                btn.innerHTML = originalText;
            }, 1000);
        }
    } else if (e.target.classList.contains('inline-qty-minus')) {
        const id = e.target.dataset.id;
        window.cartManager.updateQuantity(id, -1, false);
        const container = e.target.closest('.inline-controls-container');
        const item = cart.find(i => i.id === id);
        if (item) {
            container.querySelector('.inline-qty-val').textContent = item.quantity;
        } else {
            // Revert to add button
            const name = container.dataset.name;
            const price = container.dataset.price;
            container.innerHTML = `<button class="add-to-cart inline-add-btn" data-id="${id}" data-name="${name}" data-price="${price}"
                style="background: var(--text-primary); color: var(--bg-primary); border: none; padding: 0.7rem 1.2rem; border-radius: 8px; cursor: pointer; font-weight: 600;"><i
                    class="fas fa-plus"></i> Add</button>`;
        }
    } else if (e.target.classList.contains('inline-qty-plus')) {
        const id = e.target.dataset.id;
        window.cartManager.updateQuantity(id, 1, false);
        const container = e.target.closest('.inline-controls-container');
        const item = cart.find(i => i.id === id);
        container.querySelector('.inline-qty-val').textContent = item.quantity;
    }
});

function renderInlineControls(container, id, name, price) {
    const item = cart.find(i => i.id === id);
    if (item) {
        container.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.8rem; border: 2px solid var(--accent-color); border-radius: 8px; padding: 0.5rem 1rem; background: var(--bg-secondary);">
                <i class="fas fa-minus inline-qty-minus" data-id="${id}" style="cursor: pointer; font-size: 0.9rem; color: var(--text-primary);"></i>
                <span class="inline-qty-val" style="font-weight: 700; width: 20px; text-align: center;">${item.quantity}</span>
                <i class="fas fa-plus inline-qty-plus" data-id="${id}" style="cursor: pointer; font-size: 0.9rem; color: var(--text-primary);"></i>
            </div>
        `;
    }
}

// Function to initialize active controls on page load
window.initInlineCartControls = function() {
    document.querySelectorAll('.add-to-cart').forEach(btn => {
        // Wrap element to support inline rendering seamlessly
        if (!btn.parentElement.classList.contains('inline-controls-container')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'inline-controls-container';
            wrapper.dataset.name = btn.dataset.name;
            wrapper.dataset.price = btn.dataset.price;
            btn.parentNode.insertBefore(wrapper, btn);
            wrapper.appendChild(btn);
            btn.classList.add('inline-add-btn');
        }
        
        const id = btn.dataset.id;
        const name = btn.dataset.name;
        const price = btn.dataset.price;
        if (cart.find(i => i.id === id)) {
            renderInlineControls(btn.parentElement, id, name, price);
        }
    });
}
document.addEventListener('DOMContentLoaded', window.initInlineCartControls);

// Initialization
updateCartCount();

// Export for cart page usage
window.cartManager = {
    getCart: () => cart,
    removeItem: (id) => {
        cart = cart.filter(item => item.id !== id);
        saveCart();
        location.reload();
    },
    updateQuantity: (id, change, reload = true) => {
        const item = cart.find(item => item.id === id);
        if (item) {
            item.quantity += change;
            if (item.quantity <= 0) {
                cart = cart.filter(i => i.id !== id);
            }
        }
        saveCart();
        if (reload) location.reload();
    },
    getTotal: () => cart.reduce((acc, item) => acc + (item.price * item.quantity), 0),
    clearCart: () => {
        cart = [];
        saveCart();
    }
};
