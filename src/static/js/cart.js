const CART_TABLE = document.getElementById('cart-table');
const CART_ITEM_URL = `${window.location.origin}/api/v1/users/cart`;

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

// Fetch Products
const fetchCartItems = async () => {
    let url = new URL(CART_ITEM_URL);

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message);
        }
        return data;
    } catch (error) {
        alert(error.message);
    }
};

function addCartItemToTable(item) {
    let row = document.createElement('tr');
    let imageCell = document.createElement('th');
    imageCell.setAttribute('scope', 'row');

    let imageDiv = document.createElement('div');
    imageDiv.classList.add('d-flex', 'align-items-center');

    let image = document.createElement('img');
    image.setAttribute('src', item.product.image);
    image.classList.add('img-fluid', 'me-5', 'rounded-circle');
    image.style.width = '80px';
    image.style.height = '80px';
    image.setAttribute('alt', item.product.name);
    imageDiv.appendChild(image);
    imageCell.appendChild(imageDiv);
    row.appendChild(imageCell);

    let nameCell = document.createElement('td');
    let name = document.createElement('p');
    name.classList.add('mb-0', 'mt-4');
    name.textContent = item.product.name;
    nameCell.appendChild(name);
    row.appendChild(nameCell);

    let priceCell = document.createElement('td');
    let price = document.createElement('p');
    price.classList.add('mb-0', 'mt-4');
    price.textContent = item.product.discounted_price;
    priceCell.appendChild(price);
    row.appendChild(priceCell);

    let quantityCell = document.createElement('td');
    let quantityDiv = document.createElement('div');
    quantityDiv.classList.add('input-group', 'quantity', 'mt-4');
    quantityDiv.style.width = '100px';

    let quantityMinusDiv = document.createElement('div');
    quantityMinusDiv.classList.add('input-group-btn');
    let quantityMinusButton = document.createElement('button');
    quantityMinusButton.classList.add('btn', 'btn-sm', 'btn-minus', 'rounded-circle', 'bg-light', 'border');
    quantityMinusButton.setAttribute('id', `minus-${item.product.id}`);
    quantityMinusButton.setAttribute('data-product_id', item.product.uuid);
    let quantityMinusIcon = document.createElement('i');
    quantityMinusIcon.classList.add('fa', 'fa-minus');
    quantityMinusButton.appendChild(quantityMinusIcon);
    quantityMinusDiv.appendChild(quantityMinusButton);
    quantityDiv.appendChild(quantityMinusDiv);

    let quantityInput = document.createElement('input');
    quantityInput.setAttribute('type', 'text');
    quantityInput.classList.add('form-control', 'form-control-sm', 'text-center', 'border-0');
    quantityInput.setAttribute('value', item.quantity);
    quantityInput.setAttribute('id', `quantity-${item.product.uuid}`);
    quantityDiv.appendChild(quantityInput);

    let quantityPlusDiv = document.createElement('div');
    quantityPlusDiv.classList.add('input-group-btn');
    let quantityPlusButton = document.createElement('button');
    quantityPlusButton.classList.add('btn', 'btn-sm', 'btn-plus', 'rounded-circle', 'bg-light', 'border');
    quantityPlusButton.setAttribute('id', `plus-${item.product.uuid}`);
    quantityPlusButton.setAttribute('data-product_id', item.product.uuid);
    let quantityPlusIcon = document.createElement('i');
    quantityPlusIcon.classList.add('fa', 'fa-plus');
    quantityPlusButton.appendChild(quantityPlusIcon);
    quantityPlusDiv.appendChild(quantityPlusButton);
    quantityDiv.appendChild(quantityPlusDiv);

    quantityCell.appendChild(quantityDiv);
    row.appendChild(quantityCell);

    let totalCell = document.createElement('td');
    let total = document.createElement('p');
    total.classList.add('mb-0', 'mt-4');
    total.textContent = item.total_price;
    totalCell.appendChild(total);
    row.appendChild(totalCell);

    let actionCell = document.createElement('td');
    let actionButton = document.createElement('button');
    actionButton.classList.add('btn', 'btn-md', 'rounded-circle', 'bg-light', 'border', 'mt-4');
    actionButton.setAttribute('id', `remove-${item.product.uuid}`);
    actionButton.setAttribute('data-product_id', item.product.uuid);
    let actionIcon = document.createElement('i');
    actionIcon.classList.add('fa', 'fa-times', 'text-danger');
    actionButton.appendChild(actionIcon);
    actionCell.appendChild(actionButton);
    row.appendChild(actionCell);

    console.log(row);
    
    CART_TABLE.childNodes[3].appendChild(row);
}

async function processCartItems(){
    let data = await fetchCartItems();
    console.table(data);

    if (data.payload.cart_items.length > 0) {
        data.payload.cart_items.forEach(item => {
            addCartItemToTable(item);
        });
    }
    else{
        CART_TABLE.childNodes[3].innerHTML = '<tr><td colspan="6"><p class="text-center">No items in cart</p></td></tr>';
    }
}

// Fetch Cart Items
processCartItems()