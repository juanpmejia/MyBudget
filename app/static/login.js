/* global $*/
/*
This script implements the get methods used to login users on MyBudget
*/
function setUpLogin(){
    /* Set up submit button to POSTS a JSON containing user data. 
        Assumes data is valid. */
        
    var name, birthDate, gender, password, email;
    
    
    $(document).ready(function(){
        //console.log("I've been called");
        $("form").submit(function(event){
            event.preventDefault();
            var ans = true;
            console.log("Button clicked");
            $.getJSON("/try_login", {
                "email" : $("#InputUser").val() ,
                "password" : $("#loginPassword").val()
            }, function(data){
               console.log(data);
               if(data.ans === "ok"){
                   window.location.replace("/lobby");
               }
               else if(data.ans === "Email invalido"){
                   $("#InputUser").get(0).setCustomValidity(data.ans);
                   $("#InputUser").get(0).reportValidity();
                    ans = false;
               }
               else if(data.ans === "Contraseña errada"){
                   $("#loginPassword").get(0).setCustomValidity(data.ans);
                   $("#loginPassword").get(0).reportValidity();
                   ans = false;
               }
               
            });
            return ans;
        });
    });
    
}
setUpLogin()