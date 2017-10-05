/* global $*/
/*
This script implements the post methods used to register users on MyBudget
*/
function setUpSubmit(){
    /* Set up submit button to POSTS a JSON containing user data. 
        Assumes data is valid. */
        
    var name, birthDate, gender, password, email;
    $(document).ready(function(){
        $("#submit").click(function(){
            name = $("#InputName").val();
            birthDate = $("#InputDate").val();
            if($("#M").val()){
                gender = "M";    
            }
            else{
                gender = "F";
            }
            email = $("#InputEmail").val();
            password = $("#InputPassword").val();
            console.log(name);
            console.log(birthDate);
            console.log(gender);
            console.log(email);
            console.log(password);
        });
    });
    
}
setUpSubmit()