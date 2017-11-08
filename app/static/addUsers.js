function addFields(){
            // Number of inputs to create
            var number = document.getElementById("member").value;
            // Container <div> where dynamic content will be placed
            var container = document.getElementById("container");
            // Clear previous contents of the container
            while (container.hasChildNodes()) {
                container.removeChild(container.lastChild);
            }
            for (var i=0;i<number;i++){
                // Append a node with a random text
                container.appendChild(document.createTextNode("Usuario " + (i+1)));
                // Create an <input> element, set its type and name attributes
                var input = document.createElement("input");
                input.type = "email";
                input.name = "member" + i;
                input.className = "form-control";
                input.placeholder = "Ingrese correo del usuario";
                input.required = true;
                container.appendChild(input);
                var source = ["lala","lele","lili"]
                $('[name=member'+i+']').autocomplete({source : "/getUsers" , 
                                                    });
                // Append a line break 
                container.appendChild(document.createElement("br"));
            }
        }
