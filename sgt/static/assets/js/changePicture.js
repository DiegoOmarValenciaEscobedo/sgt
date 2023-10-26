$(document).ready(function () {
    $("#imagenSubida").change(function (event) {
        var files = event.target.files;
        var file = files[0];

        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                document.getElementById("preview-img").src = e.target.result;
                document.getElementById("preview-img").style.height = 256 + "px";
                document.getElementById("preview-img").style.width = 256 + "px";
            };
            reader.readAsDataURL(file);
        }
    });
});