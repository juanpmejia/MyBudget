var password = document.getElementById("InputPassword")
  , confirmPassword = document.getElementById("InputConPassword"),
  date = document.getElementById("InputDateFirst");
  

function validatePassword(){
  var pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
  console.log(pattern.test(password.value));
  if(!pattern.test(password.value)){
    password.setCustomValidity("Contraseña invalida");
  }else{
    password.setCustomValidity('');
  }
  
}

function validatePasswordSame(){
  if(password.value != confirmPassword.value) {
    confirmPassword.setCustomValidity("Las contraseñas no coinciden");
  } else {
    confirmPassword.setCustomValidity('');
  }
}

function dateAge(date){
  var today = new Date();
  var birthDate = new Date(date);
  var age = Math.abs(today.getFullYear()-birthDate.getFullYear());
  return age;
}

function validDate(){
  if(dateAge(date.value) >= 15){
    date.setCustomValidity('');
  }else{
    date.setCustomValidity("Tiene que ser mayor o igual a 15 años de edad");
  }
}



date.onchange = validDate;
date.onkeyup = validDate;
password.onkeyup = validatePassword;
password.onchange= validatePasswordSame;
confirmPassword.onkeyup = validatePasswordSame;