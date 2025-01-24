const CATEGORY_LIST = document.getElementById('category-list');
const ORDERING = document.getElementById('ordering');
const MIN_PRICE = document.getElementById('minPrice');
const MAX_PRICE = document.getElementById('maxPrice');
const minPriceAmount = document.getElementById('minPriceAmount');
const maxPriceAmount = document.getElementById('maxPriceAmount');
const SEARCH_KEYWORD = document.getElementById('search-keyword');
const TAG_INPUT = document.getElementById('tag-input');
const LOADER = document.getElementById('loader');
const ADD_TAG_BUTTON = document.getElementById('add-tag-btn');
const TAG_LIST = document.getElementById('tags-list');
const SELECTED_TAGS_LIST = document.getElementById('selected-tags-list');

const CLEAR_FILTERS_BTN = document.getElementById('clear-filters-btn');
const FETCH_PRODUCTS_BTN = document.getElementById('fetch-products-btn');
const PRODUCT_CONTAINER = document.getElementById('product-container');

const PRODUCT_URL = `${window.location.origin}/api/v1/products/`;
const TAG_URL = `${window.location.origin}/api/v1/products/tags/`;
const ADD_TO_CART_URL = `${window.location.origin}/api/v1/users/cart/add/`;

// Pagination Buttons
const PAGINATION_DIV = document.getElementById('pagination-div');
const START = document.getElementById('start-page');
const PREVIOUS = document.getElementById('previous-page');
const CURR = document.getElementById('curr-page');
const NEXT = document.getElementById('next-page');
const END = document.getElementById('end-page');

// Filter data
const FILTER_DATA = {
    tags: [],
    page: 1,
};

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
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


// Category filter
CATEGORY_LIST.addEventListener('click', (e) => {
    let item = document.querySelector('input[name="category"]:checked');
    if (item) {
        FILTER_DATA.category = item.value;
    } else {
        delete FILTER_DATA.category;
    }
});

// Order products based on the selected option
ORDERING.addEventListener('change', (e) => {
    FILTER_DATA.ordering = e.target.value;
    processProduct();
});


// Update max price min value based on min price
MIN_PRICE.addEventListener('input', (e) => {
    FILTER_DATA.min_price = e.target.value;

    // If max price is lower than min price, update max price to be equal to min price
    if (parseInt(MAX_PRICE.value) < parseInt(e.target.value)) {
        MAX_PRICE.value = e.target.value;
        maxPriceAmount.value = e.target.value;
        FILTER_DATA.max_price = MAX_PRICE.value;
    }
});

// Update min price max value based on max price
MAX_PRICE.addEventListener('input', (e) => {
    FILTER_DATA.max_price = e.target.value;

    // If max price becomes less than min price, adjust max price
    if (parseInt(MIN_PRICE.value) > parseInt(e.target.value)) {
        MIN_PRICE.value = e.target.value;
        minPriceAmount.value = e.target.value;
        FILTER_DATA.min_price = MAX_PRICE.value;
    }

});

SEARCH_KEYWORD.addEventListener('input', (e) => {
    FILTER_DATA.search = e.target.value;
});

// Fetch tags based on the input and display them in the tags list
let debounceTimeout;
TAG_INPUT.addEventListener('input', (e) => {
    TAG_LIST.innerHTML = '';
    TAG_LIST.classList.add('d-none');
    LOADER.classList.remove('d-none');
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(async () => {
        let query = e.target.value;
        if (query.length > 0) {
            try {
                let url = new URL(TAG_URL);
                url.search = new URLSearchParams({ title: query }).toString();
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.message);
                }
                LOADER.classList.add('d-none');
                TAG_LIST.classList.remove('d-none');

                let closeBtn = document.createElement('button');
                closeBtn.classList.add('btn-close');
                closeBtn.setAttribute('type', 'button');
                closeBtn.setAttribute('aria-label', 'Close');
                closeBtn.setAttribute('id', 'tags-list-btn-close');
                TAG_LIST.appendChild(closeBtn);
                
                closeBtn.addEventListener('click', (e) => {
                    TAG_LIST.innerHTML = '';
                    TAG_LIST.classList.add('d-none');
                });

                // Process the fetched tags (e.g., display them in a dropdown)
                if (data.payload.tags.length === 0) {
                    let li = document.createElement('li');
                    li.classList.add('tag-list-item');
                    li.textContent = 'No tags found';
                    TAG_LIST.appendChild(li);
                    return;
                }
                else{
                    data.payload.tags.forEach(tag => {
                        let li = document.createElement('li');
                        li.classList.add('tag-list-item');
                        li.innerHTML = tag.title;
                        li.setAttribute('title', tag.title);
                        TAG_LIST.appendChild(li);
                    });
                }
            } catch (error) {
                console.error('Error fetching tags:', error);
            }
        }
    }, 300); // Delay of 300ms
    if (e.target.value === '') {
        LOADER.classList.add('d-none');
        TAG_LIST.classList.add('d-none');
    }
});

// Add tags to the filter data
TAG_LIST.addEventListener('click', (e) => {
    let tag = e.target.getAttribute('title');
    if (tag) {
        if (FILTER_DATA.tags.length >= 5){
            if (!document.querySelector('#max-tag-warning')) {
                let warning = document.createElement('p');
                warning.classList.add('text-danger');
                warning.setAttribute('id', 'max-tag-warning');
                warning.textContent = 'You can only add 5 tags!';
                SELECTED_TAGS_LIST.insertAdjacentElement('beforebegin', warning);
            }
            return;
        }

        // Check if the tag already exists
        if (!FILTER_DATA.tags.includes(tag)) {
            let tagElement = document.createElement('span');
            let removeButton = document.createElement('i');
            removeButton.classList.add("fa-regular", "fa-circle-xmark", "text-danger");
            tagElement.classList.add("tags", "p-1", "m-1", "rounded", "pointer");
            tagElement.setAttribute('data-tag', tag);
            tagElement.textContent = '#'.concat(tag, ' ');
            tagElement.appendChild(removeButton);
            SELECTED_TAGS_LIST.appendChild(tagElement);
            FILTER_DATA.tags.push(tag);
        }
    }
});

// Add tags to the filter data
SELECTED_TAGS_LIST.addEventListener('click', (e) => {
    if (e.target.classList.contains('fa-circle-xmark')) {
        let tag = e.target.parentElement.getAttribute('data-tag');
        FILTER_DATA.tags = FILTER_DATA.tags.filter(item => item !== tag);
        e.target.parentElement.remove();
        
        // Remove the warning paragraph if it exists
        let warning = document.querySelector('#max-tag-warning');
        if (warning) {
            warning.remove();
        }
    }
});

// Fetch Products
const fetchProducts = async () => {
    let url = new URL(PRODUCT_URL);
    let data = JSON.parse(JSON.stringify(FILTER_DATA));
    let tags = data.tags;

    delete data.tags;
    let tagString = "";
    if (tags.length > 0) {
        tags.forEach(tag => {
            tagString += `&tags=${tag}`;
        });
    }
    url.search = new URLSearchParams(data).toString();
    url.search += tagString;
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
        window.scrollTo(0, 0);
        return data;
    } catch (error) {
        alert(error.message);
    } finally {
        FETCH_PRODUCTS_BTN.removeAttribute('disabled');
    }
};

// Function to create an element
function createElement(name){
    return document.createElement(name);
}

// Add product item to the DOM
function addProductItem(item) {

    let productDiv = createElement('div');
    productDiv.classList.add('col-md-6', 'col-lg-6', 'col-xl-4');

    let productCard = createElement('div');
    productCard.classList.add('rounded', 'position-relative', 'fruite-item');
    productDiv.appendChild(productCard);

    let productImageDiv = createElement('div');
    productImageDiv.classList.add('fruite-img');

    let productImage = createElement('img');
    productImage.src = item.image;
    productImage.alt = item.name;
    productImage.classList.add('img-fluid', 'w-100', 'rounded-top');
    productImageDiv.appendChild(productImage);
    productCard.appendChild(productImageDiv);

    let categoryBadge = createElement('div');
    categoryBadge.classList.add('text-white', 'bg-secondary', 'px-3', 'py-1', 'rounded', 'position-absolute');
    categoryBadge.style.top = '10px';
    categoryBadge.style.left = '10px';
    categoryBadge.textContent = item.category;
    productCard.appendChild(categoryBadge);

    let productRatingBadge = createElement('div');
    productRatingBadge.classList.add('text-white', 'px-3', 'py-1', 'rounded', 'position-absolute');
    productRatingBadge.style.top = '10px';
    productRatingBadge.style.right = '10px';
    for (let i = 0; i < 5; i++) {
        let star = createElement('i');
        star.classList.add('fa', 'fa-star');
        if (i < item.rating) {
            star.classList.add('text-secondary');
        }
        productRatingBadge.appendChild(star);
    }
    productCard.appendChild(productRatingBadge);

    let productContent = createElement('div');
    productContent.classList.add('p-4', 'border', 'border-secondary', 'border-top-0', 'rounded-bottom');

    let heading = createElement('h4');
    heading.innerText = item.name;
    productContent.appendChild(heading);

    let priceDiv = createElement('div');
    priceDiv.classList.add('d-flex', 'flex-lg-wrap', 'justify-content-between');
    let price = createElement('p');
    price.classList.add('text-dark', 'fs-5', 'fw-bold', 'mb-0');
    price.innerText = '₹'.concat(item.discounted_price);
    priceDiv.appendChild(price);

    let originalPrice = createElement('p');
    originalPrice.classList.add('text-danger', 'text-decoration-line-through');
    originalPrice.innerText = '₹'.concat(item.price);
    priceDiv.appendChild(originalPrice);

    let discount = createElement('p');
    discount.classList.add('text-success', 'fw-bold', 'mb-0');
    discount.innerText = item.discount.concat('% off');
    priceDiv.appendChild(discount);
    productContent.appendChild(priceDiv);

    let description = createElement('p');
    description.innerText = item.description;
    productContent.appendChild(description);

    let addToCartButton = createElement('button');
    addToCartButton.classList.add('btn', 'border', 'border-secondary', 'rounded-pill', 'px-3', 'text-primary');
    addToCartButton.setAttribute('data-product_uuid', item.uuid);
    addToCartButton.innerHTML = '<i class="fas fa-shopping-bag me-2 text-primary"></i> Add to Cart';
    productContent.appendChild(addToCartButton);

    productCard.appendChild(productContent);

    PRODUCT_CONTAINER.appendChild(productDiv);
}

// Process the fetched products
let processProduct = async (e) => {
    FETCH_PRODUCTS_BTN.setAttribute('disabled', 'disabled');
    let data = await fetchProducts();
    
    if (data.payload.results.length > 0) {
        PRODUCT_CONTAINER.innerHTML = '';
        data.payload.results.forEach(item => {
            addProductItem(item);
        });
    } else {
        PRODUCT_CONTAINER.innerHTML = '<h3 class="text-center">No products found!</h3>';
    }
    
    let previous = data.payload.previous;
    let current = data.payload.current;
    let next = data.payload.next;
    let last = data.payload.last;
    let start = data.payload.start;

    if (current){
        CURR.innerText = current;
        CURR.setAttribute('data-page', current);
        CURR.setAttribute('disabled', 'disabled');
        CURR.classList.add('active');
        CURR.classList.add('no-cursor');
    }

    if (next){
        NEXT.removeAttribute('disabled');
        NEXT.classList.remove('no-cursor');
        NEXT.setAttribute('data-page', next);
    }
    else{
        NEXT.setAttribute('disabled', 'disabled');
        NEXT.classList.add('no-cursor');
    }
    if (previous){
        PREVIOUS.removeAttribute('disabled');
        PREVIOUS.classList.remove('no-cursor');
        PREVIOUS.setAttribute('data-page', previous);
    }
    else{
        PREVIOUS.setAttribute('disabled', 'disabled');
        PREVIOUS.classList.add('no-cursor');
    }
    if (next){
        END.setAttribute('data-page', last);
        END.removeAttribute('disabled');
        END.classList.remove('no-cursor');
    }
    else{
        END.setAttribute('disabled', 'disabled');
        END.classList.add('no-cursor');
    }

    if (previous){
        START.setAttribute('data-page', 1);
        START.removeAttribute('disabled');
        START.classList.remove('no-cursor');
    }
    else{
        START.setAttribute('disabled', 'disabled');
        START.classList.add('no-cursor');
    }
}

// Fetch Products on pagination click
PAGINATION_DIV.addEventListener('click', (e) => {
    let page = e.target.getAttribute('data-page');
    if (page){
        FILTER_DATA.page = page;
        processProduct();
    }
    window.scrollTo(0, 0);
});

// Fetch Products on button click
FETCH_PRODUCTS_BTN.addEventListener('click', async (e) => {
    if (FILTER_DATA.page > 1) {
        FILTER_DATA.page = 1;
    }
    processProduct();
});

// Fetch Products on page load
processProduct();

CLEAR_FILTERS_BTN.addEventListener('click', (e) => {
    let item = document.querySelector('input[name="category"]:checked');
    if (item) {
        item.checked = false;
    }
    ORDERING.selectedIndex = 0;
    MIN_PRICE.value = MIN_PRICE.defaultValue;
    MAX_PRICE.value = MAX_PRICE.defaultValue;
    minPriceAmount.value = '';
    maxPriceAmount.value = '500';
    SEARCH_KEYWORD.value = '';
    TAG_INPUT.value = '';
    TAG_LIST.innerHTML = '';
    SELECTED_TAGS_LIST.innerHTML = '';
    FILTER_DATA = {};
    FILTER_DATA.tags = [];
    FILTER_DATA.page = 1;
    
    processProduct();
});

// Add to cart feature
PRODUCT_CONTAINER.addEventListener('click', async (e) => {
    if (e.target.tagName === 'BUTTON') {
        let i = createElement('i');
        i.classList.add('fas', 'fa-check', 'text-primary');
        e.target.innerHTML = 'Added to Cart';
        e.target.classList.add('disabled');
        e.target.prepend(i);
        let product_uuid = e.target.getAttribute('data-product_uuid');
        let quantity = 1;
        try {
            let csrftoken = getCookie('csrftoken');
            const response = await fetch(ADD_TO_CART_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    product_uuid: product_uuid,
                    quantity: quantity
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message);
            }
            alertMessage(data.message);
        } catch (error) {
            if (error.message == "Product already exists in cart."){
                e.target.innerHTML = 'Item already in Cart';
                e.target.classList.add('disabled');
                e.target.classList.add('text-danger');
            }
            alertMessage(error.message, 'alert-danger');
        }
    }
});
