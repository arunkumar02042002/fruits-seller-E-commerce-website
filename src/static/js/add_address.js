const ADD_ADDRESS_URL = `${window.location.origin}/api/v1/users/address/`;

const ADD_ADDRESS_FORM = document.getElementById('add-address-form');

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


ADD_ADDRESS_FORM.addEventListener('submit', async (event) => {
    event.preventDefault();
    let url = new URL(ADD_ADDRESS_URL);
    let data = {};
    const formData = new FormData(ADD_ADDRESS_FORM);
    for (const [key, value] of formData.entries()) {
        data[key] = value;
    }

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
        console.log(response_data);

        if (!response.ok) {
            throw new Error(response_data.message || "Invalid Coupon.");
        }

        alertMessage(response_data.message, 'alert-success');
        ADD_ADDRESS_FORM.reset();
        setTimeout(() => {
            location.reload();
        }, 2000);

    } catch (error) {
        alertMessage(error.message, 'alert-danger');
    }
});
