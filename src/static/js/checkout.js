const CREATE_ORDER_FORM = document.getElementById('create-order-form');
const CREATE_ORDER_URL = `${window.location.origin}/api/v1/orders/create-order/`;
const ORDER_SUCCESS_URL = `${window.location.origin}/orders/success/`;

function alertMessage(message='', messageClass='alert-success') {
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


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

const PAYMENT_METHOD = {
    "COD": 1,
    "Razorpay": 2,
}

CREATE_ORDER_FORM.addEventListener('submit', async (event) => {
    event.preventDefault();
    let url = new URL(CREATE_ORDER_URL);
    let data = {
        'address_data': {},
        'user_data': {}
    };
    const formData = new FormData(CREATE_ORDER_FORM);
    let address_keys = ['address_line_1', 'city', 'state', 'country', 'pincode'];
    let users_key = ['first_name', 'last_name', 'email', 'mobile_number'];

    for (const [key, value] of formData.entries()) {
        if (address_keys.includes(key)) {
            data['address_data'][key] = value
        }
        else if (users_key.includes(key)) {
            data['user_data'][key] = value
        }
        else if (key === 'payment_method') {
            data['payment_method'] = parseInt(value);
        }
        else {
            data[key] = value;
        }
    }
    console.log(data);

    // Make API call to create order
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(data)
        });

        const response_data = await response.json();

        if (!response.ok) {
            throw new Error(response_data.message || "Invalid Coupon.");
        }
        alertMessage(response_data.message, 'alert-success');
        CREATE_ORDER_FORM.reset();

        let payment_method = response_data['payload']['payment_method'];

        if (payment_method === PAYMENT_METHOD['COD']) {
            setTimeout(() => {
                window.location.href = ORDER_SUCCESS_URL;
            }, 1000);
        }   
    } catch (error) {
        alertMessage(error.message, 'alert-danger');
    }
});