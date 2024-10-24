let validatePasswordURL = "/api/v1/authentication/validate_password/";
let validateEmailURL = "/api/v1/authentication/validate_email/";
let emailInput = document.getElementById("id_email");
let password1Input = document.getElementById("id_password1");
let password2Input = document.getElementById("id_password2");
let submitButton = document.getElementById("signUpBtn");
let password1ErrorList = document.getElementById("password1-errorlist");
let password2ErrorList = document.getElementById("password2-errorlist");
let emailErrorList = document.getElementById("email-errorlist");
let signUpForm = document.getElementById("signUpForm");

let validEmail = false;
let validPassword = false;
let passwordSame = false;

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function debounce(func, delay) {
  let timeoutId;

  return function (...args) {
    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

function createErrorListItem(innerText) {
  let listItem = document.createElement("li");
  listItem.innerHTML = innerText;
  return listItem;
}

function ValidateEmail(value) {
  const validRegex =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

  if (value.match(validRegex)) {
    return true;
  } else {
    return false;
  }
}

function ValidatePassword(value) {
  console.log("I was called!")
  var validRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  if (value.match(validRegex)) {
    return true;
  } else {
    return false;
  }
}

function enableSubmitButton() {
  if (validEmail && validPassword && passwordSame) {
    submitButton.removeAttribute("disabled");
  } else {
    submitButton.setAttribute("disabled", true);
  }
}

async function validatePasswordApi(password) {
  // Your API call logic
  const response = await fetch(validatePasswordURL, {
    method: "POST",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ password: password }),
  });
  const data = await response.json();
  if (response.status != 200){
    password2ErrorList.innerHTML = "";
    password1ErrorList.appendChild(createErrorListItem(data.message));
    validPassword = false;
  }
  else {
    password1ErrorList.innerHTML = "";
    validPassword = true
  }
}

async function validateEmailApi(email) {
  // Your API call logic
  const response = await fetch(validateEmailURL, {
    method: "POST",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email: email }),
  });
  const data = await response.json();

  if (response.status != 200){
    validEmail = false;
    emailErrorList.innerHTML = "";
    emailErrorList.appendChild(createErrorListItem(data.message));
  }
  else{
    emailErrorList.innerHTML = "";
    validEmail = true;
  }
  // Process the data
  console.log(response, data);
}

const debounceValidatePasswordApiCall = debounce(validatePasswordApi, 500);
const debounceValidateEmailApiCall = debounce(validateEmailApi, 500);


// Example usage with an input field
password1Input.addEventListener("keyup", (event) => {
  // console.log(event.target.value);
  let isvalidPassword = ValidatePassword(event.target.value);
  if (isvalidPassword){
    validPassword = true;
    debounceValidatePasswordApiCall(event.target.value);
  }
  if (event.target.value == password2Input.value) {
    passwordSame = true;
    password2ErrorList.innerHTML = "";
  }
  enableSubmitButton();
});


emailInput.addEventListener("keyup", (event) => {
  let isvalidEmail = ValidateEmail(event.target.value);
  if (isvalidEmail){
    validEmail = true;
    debounceValidateEmailApiCall(event.target.value);
  }
  enableSubmitButton();
});

password2Input.addEventListener("keyup", (event) => {
  if (event.target.value == password1Input.value) {
    passwordSame = true;
    password2ErrorList.innerHTML = "";
  } else {
    password2ErrorList.innerHTML = "";
    password2ErrorList.appendChild(
      createErrorListItem("Password didn't match!")
    );
  }
  enableSubmitButton();
});

signUpForm.addEventListener("submit", (event) => {
  // Disable the submit button to prevent multiple clicks
  submitButton.setAttribute("disabled", true);
});
