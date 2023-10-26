document.write('<script src="/static/assets/js/TUTOR/sweetalert.js"></script>');
document.write('<script src="/static/assets/js/TUTOR/read-excel-file.js"></script>');



function nueva_eval(){
    const archivo = document.getElementById('nva_eval').innerHTML= 
    '<div class="card justify-content-center align-items-center my-5 shadow-none border border-light" id="fileZone" style="width: 60%; margin-left:20%;">'+
        '<span class="text-center my-3 text-dark">Nueva evaluacion diagnostica</span>'+
        '<div class="custom-file my-1">'+
            '<input type="file" class="custom-file-input d-none" id="doc" lang="es">'+
            '<label class="custom-file-label mx-6" for="doc">Selecciona el archivo</label>'+
        '</div>'+
        '<div class="row my-1 mx-2">'+
            '<input type="text" class="form-control my-1" value="Nombe de la actividad" readonly>'+
            '<input type="text" class="form-control my-1" value="Añade una descripción" readonly>'+
            '<input type="date" class="form-control my-1" value="Fecha de cierre" readonly>'+
            '<input type="text" class="form-control my-1" value="Selecciona el grupo" readonly>'+
        '</div>'+
        '<button type="submit" class="btn btn-success my-2">Crear</button>'+
    '</div>'
}
