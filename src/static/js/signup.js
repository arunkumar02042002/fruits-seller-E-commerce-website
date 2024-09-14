// let validatePasswordUrl = '/authentication/validate-password/'
let emailInput = document.getElementById("id_email");
let password1Input = document.getElementById("id_password1");
let password2Input = document.getElementById("id_password2");
let submitButton = document.getElementById("signUpBtn");
let passwordStrength = document.getElementById("password-strength");
let lowUpperCase = document.querySelector(".low-upper-case i");
let number = document.querySelector(".one-number i");
let specialChar = document.querySelector(".one-special-char i");
let eightChar = document.querySelector(".eight-character i");
let password2ErrorList = document.getElementById("password2-errorlist");
let signUpForm = document.getElementById("signUpForm");

let validEmail = false;
let validPassword= false;
let passwordSame = false;
// let state = false;

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== "") {
//       const cookies = document.cookie.split(";");
//       for (let i = 0; i < cookies.length; i++) {
//         const cookie = cookies[i].trim();
//         // Does this cookie string begin with the name we want?
//         if (cookie.substring(0, name.length + 1) === (name + "=")) {
//           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//           break;
//         }
//       }
//     }
//     return cookieValue;
// }

// function debounce(func, delay) {
//     let timeoutId;
  
//     return function(...args) {
//       clearTimeout(timeoutId);
  
//       timeoutId = setTimeout(() => {
//         func.apply(this, args);
//       }, delay);
//     };
//   }

  
//   async function validatePasswordApi(password) {
//     // Your API call logic 
//     console.log(validatePasswordUrl);
//     const response = await fetch(validatePasswordUrl, {
//         method:'POST',
//         headers: {
//             "X-Requested-With": "XMLHttpRequest",
//             "X-CSRFToken": getCookie("csrftoken"),
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ password: password })
//     });
//     const data = await response.json();
//     // Process the data
//     console.log(data);
//   }
  
//   const debouncedApiCall = debounce(validatePasswordApi, 500);
  
// Example usage with an input field
password1Input.addEventListener('keyup', (event) => {
    validPassword = ValidatePassword(event.target.value);
	checkStrength(event.target.value);
	if (event.target.value == password2Input.value){
		passwordSame = true;
        password2ErrorList.innerHTML = '';
	}
	enableSubmitButton();
});

function checkStrength(password) {
    let strength = 0;

    //If password contains both lower and uppercase characters
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) {
        strength += 1;
        lowUpperCase.classList.remove('fa-circle');
        lowUpperCase.classList.add('fa-check');
    } else {
        lowUpperCase.classList.add('fa-circle');
        lowUpperCase.classList.remove('fa-check');
    }
    //If it has numbers and characters
    if (password.match(/([0-9])/)) {
        strength += 1;
        number.classList.remove('fa-circle');
        number.classList.add('fa-check');
    } else {
        number.classList.add('fa-circle');
        number.classList.remove('fa-check');
    }
    //If it has one special character
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) {
        strength += 1;
        specialChar.classList.remove('fa-circle');
        specialChar.classList.add('fa-check');
    } else {
        specialChar.classList.add('fa-circle');
        specialChar.classList.remove('fa-check');
    }
    //If password is greater than 7
    if (password.length > 7) {
        strength += 1;
        eightChar.classList.remove('fa-circle');
        eightChar.classList.add('fa-check');
    } else {
        eightChar.classList.add('fa-circle');
        eightChar.classList.remove('fa-check');   
    }

    // If value is less than 2
    if (strength < 2) {
        passwordStrength.classList.remove('progress-bar-warning');
        passwordStrength.classList.remove('progress-bar-success');
        passwordStrength.classList.add('progress-bar-danger');
        passwordStrength.style = 'width: 10%';
    } else if (strength == 3) {
        passwordStrength.classList.remove('progress-bar-success');
        passwordStrength.classList.remove('progress-bar-danger');
        passwordStrength.classList.add('progress-bar-warning');
        passwordStrength.style = 'width: 60%';
    } else if (strength == 4) {
        passwordStrength.classList.remove('progress-bar-warning');
        passwordStrength.classList.remove('progress-bar-danger');
        passwordStrength.classList.add('progress-bar-success');
        passwordStrength.style = 'width: 100%';
    }
}

function createErrorListItem(innerText){
    let listItem = document.createElement('li');
    listItem.innerHTML = innerText;
    return listItem
}

function ValidateEmail(value) {
	const validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  
	if (value.match(validRegex)) {  
	  	return true;
	} else {
	  	return false;
	}
}

function ValidatePassword(value){
	var validRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
	if (value.match(validRegex)) {  
		return true;
	} else {
		return false;
	}
	
}

function enableSubmitButton(){
	if (validEmail && validPassword && passwordSame) {
		submitButton.removeAttribute("disabled");
	}
    else{
        submitButton.setAttribute('disabled', true);
    }
}

emailInput.addEventListener('keyup', (event) => {
	validEmail = ValidateEmail(event.target.value);
	enableSubmitButton();
})

password2Input.addEventListener('keyup', event => {
	if (event.target.value == password1Input.value){
		passwordSame = true;
        password2ErrorList.innerHTML = '';
	}
    else{
        password2ErrorList.innerHTML = '';
        password2ErrorList.appendChild(createErrorListItem("Password didn't match!"));
    }
	enableSubmitButton();
})

signUpForm.addEventListener('submit', (event) => {
    // Disable the submit button to prevent multiple clicks
    submitButton.setAttribute('disabled', true);
});