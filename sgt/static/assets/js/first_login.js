$(document).ready(function () {
    var today = new Date(); //Dia de hoy
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //Enero es 0
    var yyyy = today.getFullYear() - 10; //Minimo 10 años
    if (dd < 10) {
        dd = '0' + dd
    }
    if (mm < 10) {
        mm = '0' + mm
    }

    today = yyyy + '-' + mm + '-' + dd;
    document.getElementById("id_fechaDeNacimiento").setAttribute("max", today);

    var today = new Date();
    var yyyy = today.getFullYear() - 100;
    today = yyyy + '-' + mm + '-' + dd;
    document.getElementById("id_fechaDeNacimiento").setAttribute("min", today);
});