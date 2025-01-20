const CURR_LOCATION = window.location.href;
const DOMAIN = CURR_LOCATION.split("/")[2];
const NAVBAR = document.getElementById("navbarMain");
const NAVBAR_ITEMS = NAVBAR.getElementsByClassName("nav-item nav-link");


// Function to remove active class from all buttons
function removeActive(){
    for (let i = 0; i < NAVBAR_ITEMS.length; i++) {
        NAVBAR_ITEMS[i].classList.remove("active");
    }
}
removeActive();

// Add active class to the current button (highlight it)
if (CURR_LOCATION.includes("about")){
    document.getElementById("about-us-link").classList.add("active");
}
else if (CURR_LOCATION.includes("contact")){
    document.getElementById("contact-us-link").classList.add("active");
}
else if (CURR_LOCATION.includes("products")){
    document.getElementById("shop-link").classList.add("active");
}
else{
    document.getElementById("home-link").classList.add("active");
}