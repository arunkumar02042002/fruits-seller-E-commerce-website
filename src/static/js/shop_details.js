const ADD_TO_CART_URL = `${window.location.origin}/api/v1/users/cart/add/`;
const ADD_TO_CART_BUTTON = document.getElementById('add-to-cart');
const QUANTITY_INPUT = document.getElementById('quantity-input');

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function alertMessage(message='', messageClass='alert-success') {
    document.querySelectorAll('.alert').forEach(alert => alert.remove());

    let alertDiv = document.createElement('div');
    alertDiv.classList.add('alert', 'alert-dismissible', 'fade', 'show', messageClass);
    alertDiv.setAttribute('role', 'alert');
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '0';
    alertDiv.style.zIndex = '9999999';
    alertDiv.style.width = '100%';
    alertDiv.textContent = message;

    let closeButton = document.createElement('button');
    closeButton.classList.add('btn-close');
    closeButton.setAttribute('data-bs-dismiss', 'alert');
    closeButton.setAttribute('aria-label', "Close")

    alertDiv.appendChild(closeButton);
    document.body.appendChild(alertDiv);
}

ADD_TO_CART_BUTTON.addEventListener('click', async (e) => {
    let product_id = ADD_TO_CART_BUTTON.getAttribute('data-product_id');
    let quantity = QUANTITY_INPUT.value;
    let i = document.createElement('i');
    i.classList.add('fas', 'fa-check', 'text-primary');
    e.target.innerHTML = 'Added to Cart';
    e.target.classList.add('disabled');
    e.target.prepend(i);
    
    try{
        let csrftoken = getCookie('csrftoken');
        const response = await fetch(ADD_TO_CART_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                product_uuid: product_id,
                quantity: quantity,
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message);
        }
    } catch (error) {
        if (error.message == "Product already exists in cart."){
            e.target.innerHTML = 'Item already in Cart';
            e.target.classList.add('disabled');
            e.target.classList.add('text-danger');
        }
        alertMessage(error.message, 'alert-danger');
    }
});
