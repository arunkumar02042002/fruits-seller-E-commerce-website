const ADD_TO_CART_URL = `${window.location.origin}/api/v1/users/cart/add/`;
const ADD_TO_CART_BUTTON = document.getElementById('add-to-cart');
const QUANTITY_INPUT = document.getElementById('quantity-input');
const ADD_REVIEW_FORM = document.getElementById('add-review-form');
const ADD_REVIEW_BUTTON = document.getElementById('add-review-button');
const ReviewTab = document.getElementById('review-container');

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

function addReviewToTab(review){

    let reviewCard = document.createElement('div');
    reviewCard.classList.add('d-flex');
    let img = document.createElement('img');
    img.classList.add('img-fluid', 'rounded-circle', 'p-3');
    img.style.width = '100px';
    img.style.height = '100px';
    img.alt = '';
    img.src = review.profile.profile_picture ? review.profile.profile_picture : '/static/users/profile_pictures/default_profile.png';

    let reviewDiv = document.createElement('div');
    let date = document.createElement('p');
    date.classList.add('mb-2');
    date.style.fontSize = '14px';
    date.textContent = review.created_at.date;

    let reviewContent = document.createElement('div');
    reviewContent.classList.add('d-flex', 'justify-content-between');
    let name = document.createElement('h5');
    name.textContent = review.profile.user.first_name + review.profile.user.last_name
    let stars = document.createElement('div');
    stars.classList.add('d-flex', 'mb-3');
    for (let i = 0; i < 5; i++){
        let star = document.createElement('i');
        star.classList.add('fa', 'fa-star');
        if (i < review.rating){
            star.classList.add('text-secondary');
        }
        stars.appendChild(star);
    }

    let reviewText = document.createElement('p');
    reviewText.textContent = review.review;

    let created_at = document.createElement('p');
    created_at.classList.add('mb-2');
    created_at.style.fontSize = '14px';
    created_at.textContent = review.created_at.date;


    reviewContent.appendChild(name);
    reviewContent.appendChild(stars);
    reviewDiv.appendChild(created_at);
    reviewDiv.appendChild(reviewContent);
    reviewDiv.appendChild(reviewText);
    reviewCard.appendChild(img);
    reviewCard.appendChild(reviewDiv);
    ReviewTab.appendChild(reviewCard);

    return reviewCard;
}

if (ADD_REVIEW_FORM){
    ADD_REVIEW_FORM.addEventListener('submit', async (e) => {
        e.preventDefault();
        ADD_REVIEW_BUTTON.setAttribute('disabled', 'disabled');
        ADD_REVIEW_BUTTON.innerHTML = 'Adding Review...';
        let formData = new FormData(ADD_REVIEW_FORM);
        ADD_REVIEW_FORM.reset();
        
        setTimeout(async () => {
            let response = await fetch(ADD_REVIEW_FORM.action, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                method: ADD_REVIEW_FORM.method,
                body: formData,
            });

           let data = await response.json();

           let reviewCard = addReviewToTab(data.payload);
    
            if (response.ok) {
                alertMessage(data.message, 'alert-success');
            } else {
                reviewCard.remove();
                alertMessage(data.message, 'alert-danger');
            }
        
            ADD_REVIEW_BUTTON.removeAttribute('disabled');
            ADD_REVIEW_BUTTON.innerHTML = 'Add Review';
        }, 1000);
    });
}
