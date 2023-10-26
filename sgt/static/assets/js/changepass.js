$(document).ready(function () {
    var pass = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[ -/:-@\[-`{-~]).{8,16}$/;
    var contraa = document.getElementById("id_actual");
    var contra1 = document.getElementById("id_nueva");
    var contra2 = document.getElementById("id_repetirNueva");
    var msg = document.getElementById("msg");

    contra1.addEventListener('change', function(){
        if (contraa.value == contra1.value) {
            msg.textContent= "La nueva contraseña no puede ser igual a la actual";
            msg.style.color = "red"
            setTimeout(function(){
                msg.style.display = 'none';
            },7000);
        }

        else if (!contra1.value.match(pass)) {
            msg.textContent= "La nueva contraseña debe de contener mínimo 8 caracteres, 1 mayúscula, 1 número y un cáracter especial";
            msg.style.color = "red"
            setTimeout(function(){
                msg.style.display = 'none';
            },7000);
        }
        else if(contra1.value != contra2.value){
            msg.textContent= "La nueva contraseña no coincide con la repetición";
            msg.style.color = "red"
            setTimeout(function(){
                msg.style.display = 'none';
            },7000);
        }
        else{
            msg.style.display = 'none'
        }
    });

    contra2.addEventListener('change', function(){
        if(contra1.value != contra2.value){
            msg.textContent= "La nueva contraseña no coincide con la repetición";
            msg.style.color = "red"
            setTimeout(function(){
                msg.style.display = 'none';
            },7000);
        }
        else{
            msg.style.display = 'none';
        }
    });
    
});