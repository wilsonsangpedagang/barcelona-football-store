function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');

    if (!toastComponent) return;

    // Reset all
    toastComponent.classList.remove(
        'bg-barca-blue', 'bg-barca-red', 'bg-barca-gold',
        'text-white', 'text-barca-gold', 'border-barca-red', 'border-barca-blue'
    );

    // Custom Barcelona palette
    const colors = {
        blue: "#004D98",   // Barça Blue
        red: "#A50044",    // Barça Red
        gold: "#EDBB00"    // Barça Gold
    };

    // Apply styles by type
    if (type === 'success') {
        toastComponent.style.backgroundColor = colors.blue;
        toastComponent.style.color = "white";
    } else if (type === 'error') {
        toastComponent.style.backgroundColor = colors.red;
        toastComponent.style.color = "white";
    } else {
        toastComponent.style.backgroundColor = colors.gold;
        toastComponent.style.color = "black";
    }

    // Set text
    toastTitle.textContent = title;
    toastMessage.textContent = message;

    // Animate in
    toastComponent.classList.remove('opacity-0', 'translate-y-64');
    toastComponent.classList.add('opacity-100', 'translate-y-0');

    // Hide after duration
    setTimeout(() => {
        toastComponent.classList.add('opacity-0', 'translate-y-64');
    }, duration);
}

// Authentication toasts
function showLoginToast(username) {
    showToast('Login Successful', `Welcome back, ${username}!`, 'success');
}

function showLogoutToast() {
    showToast('Logged Out', 'See you soon!', 'normal');
}

function showRegisterToast() {
    showToast('Registration Successful', 'Welcome to Barcelona Football Store!', 'success');
}

// Product toasts
function showProductCreatedToast() {
    showToast('Product Created', 'Your product has been added successfully!', 'success');
}

function showProductUpdatedToast() {
    showToast('Product Updated', 'Your changes have been saved successfully!', 'success');
}

function showProductDeletedToast() {
    showToast('Product Deleted', 'The product has been removed successfully!', 'normal');
}

// Error toasts
function showErrorToast(message) {
    showToast('Error', message, 'error');
}