$(document).ready(function () {
    document.getElementById("btnModal").addEventListener("click", function(){
        $("#exampleModal").modal("show");
    });

    document.fullscreenElement.addEventListener("click", function(){
        $("#exampleModal").modal("hide");
    });
});