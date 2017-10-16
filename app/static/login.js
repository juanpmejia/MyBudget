/* global $*/
/*
This script implements the get methods used to login users on MyBudget
*/
function setUpLogin(){
    /* Set up submit button to POSTS a JSON containing user data. 
        Assumes data is valid. */
        
    var name, birthDate, gender, password, email;
    $(document).ready(function(){
        $("form").submit(function(event){
            event.preventDefault();
            console.log("Button clicked");
            $.getJSON("/try_login", {
                "email" : $("#InputUser").val() ,
                "password" : $("#loginPassword").val()
            }, function(data){
               console.log(data);
               if(data.ans = "ok"){
                   window.location.replace("/lobby");
               }
            });
        });
    });
    
}
setUpLogin()