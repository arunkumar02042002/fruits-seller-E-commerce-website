const CART_TABLE = document.getElementById('cart-table');
const CART_ITEM_URL = `${window.location.origin}/api/v1/users/cart`;
const CART_TOTAL_URL = `${window.location.origin}/api/v1/users/cart/total`;
const APPLY_COUPON_URL = `${window.location.origin}/api/v1/products/check-coupon/`;

const COUPON_DIV = document.getElementById('coupon-div');
const COUPON_FORM = document.getElementById('coupon-form');
const COUPON_INPUT = document.getElementById('coupon-input');

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function disableNode(node){
    node.classList.add('disabled');
}

function enableNode(node){
    node.classList.remove('disabled');
}

function noCursor(node){
    node.classList.add('no-cursor');
}

function cursor(node, type){
    node.classList.remove('no-cursor');
    node.style.cursor = type;
}

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
    row.setAttribute('id', `row-${item.uuid}`);
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
    name.classList.add('mb-0', 'mt-4', 'font-weight-bold');
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
    quantityMinusButton.setAttribute('id', `minus-${item.uuid}`);
    quantityMinusButton.setAttribute('data-cartitem_id', item.uuid);
    if (item.quantity === 1) {
        disableNode(quantityMinusButton);
    }

    let quantityMinusIcon = document.createElement('i');
    quantityMinusIcon.classList.add('fa', 'fa-minus');
    quantityMinusButton.appendChild(quantityMinusIcon);
    quantityMinusDiv.appendChild(quantityMinusButton);
    quantityDiv.appendChild(quantityMinusDiv);

    let quantityInput = document.createElement('input');
    quantityInput.setAttribute('type', 'text');
    quantityInput.classList.add(
        'form-control', 'form-control-sm',
        'text-center', 'border-0',
        'quanity-input'
    );
    quantityInput.setAttribute('value', item.quantity);
    quantityInput.setAttribute('id', `quantity-${item.uuid}`);
    quantityInput.setAttribute('data-cartitem_id', item.uuid);
    quantityDiv.appendChild(quantityInput);

    let quantityPlusDiv = document.createElement('div');
    quantityPlusDiv.classList.add('input-group-btn');

    let quantityPlusButton = document.createElement('button');
    quantityPlusButton.classList.add('btn', 'btn-sm', 'btn-plus', 'rounded-circle', 'bg-light', 'border');
    quantityPlusButton.setAttribute('id', `plus-${item.uuid}`);
    quantityPlusButton.setAttribute('data-cartitem_id', item.uuid);

    let quantityPlusIcon = document.createElement('i');
    quantityPlusIcon.classList.add('fa', 'fa-plus');
    quantityPlusButton.appendChild(quantityPlusIcon);
    quantityPlusDiv.appendChild(quantityPlusButton);
    quantityDiv.appendChild(quantityPlusDiv);

    quantityCell.appendChild(quantityDiv);
    row.appendChild(quantityCell);

    let totalCell = document.createElement('td');
    let total = document.createElement('p');
    total.classList.add('mb-0', 'mt-4', 'font-weight-bold');
    total.textContent = `${item.product.discounted_price} * ${item.quantity} = ${item.total_price}`;
    total.setAttribute('id', `total-${item.uuid}`);
    totalCell.appendChild(total);
    row.appendChild(totalCell);

    let actionCell = document.createElement('td');
    let actionButton = document.createElement('button');
    actionButton.classList.add(
        'btn', 'btn-md', 'rounded-circle',
        'bg-light', 'border', 'mt-4',
        'delete-button'
    );
    actionButton.setAttribute('id', `delete-${item.uuid}`);
    actionButton.setAttribute('data-cartitem_id', item.uuid);
    let actionIcon = document.createElement('i');
    actionIcon.classList.add('fa', 'fa-times', 'text-danger');
    actionButton.appendChild(actionIcon);
    actionCell.appendChild(actionButton);
    row.appendChild(actionCell);
    
    CART_TABLE.childNodes[3].appendChild(row);
}

async function processCartItems(){
    let data = await fetchCartItems();

    if (data.payload.cart_items.length > 0) {
        data.payload.cart_items.forEach(item => {
            addCartItemToTable(item);
        });
    }
    else{
        CART_TABLE.childNodes[3].innerHTML = '<tr><td colspan="6"><p class="text-center">No items in cart</p></td></tr>';
    }
    processCartTotal();
}

// Fetch Cart Items
processCartItems()


// Update Cart Items
async function updateCartItem(uuid, quantity) {
    const url = `${window.location.origin}/api/v1/users/cart/${uuid}/`;

    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ quantity: quantity })
        });

        const data = await response.json();
        updateTableRow(data.payload);
        processCartTotal();

        if (!response.ok) {
            throw new Error(data.message);
        }
    } catch (error) {
        alertMessage(error.message);
        return;
    }   
}

function debounce(func, delay) {
    let timeout;
    let lastUuid;
    return function(uuid, ...args) {
        if (lastUuid !== uuid) {
            clearTimeout(timeout);
            lastUuid = uuid;
        }
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, [uuid, ...args]), delay);
    };
}

const debouncedUpdateCartItem = debounce(updateCartItem, 300);

function updateTableRow(item){
    let total = document.getElementById(`total-${item.uuid}`);
    total.textContent = `${item.product_discounted_price} * ${item.quantity} = ${item.total_price}`;
}

CART_TABLE.addEventListener('click', async (e) => {
    let targetElement = e.target;
    if (targetElement.tagName === 'I') {
        targetElement = targetElement.parentElement;
    }

    let quantity;
    let cartitem_id;

    if (targetElement.classList.contains('btn-plus')){
        cartitem_id = targetElement.getAttribute('data-cartitem_id');
        const quantityInput = document.getElementById(`quantity-${cartitem_id}`);
        quantity = parseInt(quantityInput.value);

        quantity += 1;
        quantityInput.value = quantity;        
        enableNode(document.getElementById(`minus-${cartitem_id}`));;
    }

    else if (targetElement.classList.contains('btn-minus')){
        cartitem_id = targetElement.getAttribute('data-cartitem_id');
        const quantityInput = document.getElementById(`quantity-${cartitem_id}`);
        quantity = parseInt(quantityInput.value);

        quantity -= 1;
        quantityInput.value = quantity;
        
        if (quantity < 1){
            quantity = 1;
            quantityInput.value = quantity;
            disableNode(targetElement)
        };
    }

    else if (targetElement.classList.contains('quanity-input')){
        cartitem_id = targetElement.getAttribute('data-cartitem_id');
        quantity = parseInt(targetElement.value);

        if (quantity < 1){
            quantity = 1;
            targetElement.value = quantity;
            disableNode(document.getElementById(`minus-${cartitem_id}`));
        };
    }

    else if (targetElement.classList.contains('delete-button') ){
        cartitem_id = targetElement.getAttribute('data-cartitem_id');
        deleteCartItemModal(cartitem_id);       
    }

    if (cartitem_id && quantity) {
        debouncedUpdateCartItem(cartitem_id, quantity);
    }
});

// Remove Table Row
function removeTableRow(cartitem_id){
    let tableRow = document.getElementById(`row-${cartitem_id}`);
    tableRow.remove();
}

// Delete Cart Item
async function deleteCartItem(cartitem_id){
    const url = `${window.location.origin}/api/v1/users/cart/${cartitem_id}/`;

    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        if (!response.ok) {
            throw new Error(data.message);
        }

    } catch (error) {
        alertMessage(error.message);
        return;
    }
}

function deleteCartItemModal(cartitem_id){

    let modal = document.createElement('div');
    modal.classList.add('modal', 'fade', 'show');
    modal.setAttribute('id', cartitem_id);
    modal.setAttribute('tabindex', '-1');
    modal.setAttribute('role', 'dialog');
    modal.style.display = 'block';

    // <div class="modal-dialog modal-dialog-centered" role="document">
    let modalDialog = document.createElement('div');
    modalDialog.classList.add('modal-dialog', 'modal-dialog-centered');
    modalDialog.setAttribute('role', 'document');

    // <div class="modal-content">
    let modalContent = document.createElement('div');
    modalContent.classList.add('modal-content');

    // <div class="modal-header">
    let modalHeader = document.createElement('div');
    modalHeader.classList.add('modal-header');

    // <h5 class="modal-title" id="exampleModalLongTitle">Modal title</h5>
    let modalTitle = document.createElement('h5');
    modalTitle.classList.add('modal-title');
    modalTitle.textContent = 'Delete Cart Item';

    modalHeader.appendChild(modalTitle);

    // <div class="modal-body">
    let modalBody = document.createElement('div');
    modalBody.classList.add('modal-body');
    modalBody.textContent = 'Are you sure you want to delete this item?';
    
    // <div class="modal-footer">
    let modalFooter = document.createElement('div');
    modalFooter.classList.add('modal-footer');

    // <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
    let modalCloseButton = document.createElement('button');
    modalCloseButton.classList.add('btn', 'btn-secondary');
    modalCloseButton.setAttribute('data-dismiss', 'modal');
    modalCloseButton.textContent = 'Close';

    modalCloseButton.addEventListener('click', () => {
        document.body.removeChild(modal);
    });

    // <button type="button" class="btn btn-danger">Delete</button>
    let deleteButton = document.createElement('button');
    deleteButton.classList.add('btn', 'btn-danger');
    deleteButton.textContent = 'Delete';
    deleteButton.setAttribute('id', `delete-${cartitem_id}`);
    deleteButton.setAttribute('data-cartitem_id', cartitem_id);

    // Delete Cart Item
    deleteButton.addEventListener('click', async (e) => {
        let cartitem_id = e.target.getAttribute('data-cartitem_id');
        deleteCartItem(cartitem_id);
        removeTableRow(cartitem_id);
        document.body.removeChild(modal);
    });

    modalFooter.appendChild(modalCloseButton);
    modalFooter.appendChild(deleteButton);

    modalContent.appendChild(modalHeader);
    modalContent.appendChild(modalBody);
    modalContent.appendChild(modalFooter);

    modalDialog.appendChild(modalContent);
    modal.appendChild(modalDialog);

    document.body.appendChild(modal);
}

// Fetch Cart Total
async function fetchCartTotal() {
    try {
        const response = await fetch(CART_TOTAL_URL, {
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
        alertMessage(error.message);
    }
}

// Process Cart Total
async function processCartTotal(){
    let data = await fetchCartTotal();
    updateCartTotal(data.payload);
}

// Update Cart Total
function updateCartTotal(data){
    let subTotal = document.getElementById('subtotal-price');
    let shippingPrice = document.getElementById('shipping-price');
    let totalPrice = document.getElementById('total-price');

    subTotal.textContent = data.sub_total;
    shippingPrice.textContent = data.delivery_fee;
    totalPrice.textContent = data.total;
}


COUPON_INPUT.addEventListener('input', () => {
    let coupon = COUPON_INPUT.value;
    if (coupon.length > 0) {
        COUPON_FORM.children[1].disabled = false;
    } else {
        COUPON_FORM.children[1].disabled = true;
    }
});


COUPON_FORM.addEventListener('submit', async (e) => {
    e.preventDefault();
    let code = document.getElementById('coupon-input').value;
    let url = new URL(APPLY_COUPON_URL);

    COUPON_FORM.children[1].disabled = true;

    // Remove all p elements with class 'text-danger' from COUPON_DIV
    let errorMessages = COUPON_DIV.querySelectorAll('p.text-danger');
    errorMessages.forEach(message => message.remove());
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error("Invalid Coupon.");
        }

        COUPON_FORM.children[1].disabled = true;
        let coupon = document.createElement('p');
        coupon.textContent = data.payload.code;
        coupon.classList.add('text-dark', 'bg-secondary', 'rounded-pill', 'p-2', 'd-inline-block', 'mt-3', 'me-3');

        let closeBtn = document.createElement('i');
        closeBtn.classList.add("fa-regular", "fa-circle-xmark", "text-danger", "cursor-pointer");
        coupon.appendChild(closeBtn);

        updateCartTotal(data.payload);
        let cartTotal = document.getElementById('total-price');
        cartTotal.innerHTML = data.payload.discounted_total;

        let span = document.createElement('span');
        span.classList.add('text-decoration-line-through', 'text-danger', 'ms-3');
        span.innerText = data.payload.total;

        cartTotal.appendChild(span);

        closeBtn.addEventListener('click', () => {
            COUPON_DIV.removeChild(coupon);
            COUPON_FORM.children[1].disabled = false;
            updateCartTotal(data.payload);
        });

        COUPON_DIV.appendChild(coupon);
    } catch (error) {
        let p = document.createElement('p');
        p.textContent = error.message;
        p.classList.add('text-danger');
        COUPON_DIV.appendChild(p);
    }
});