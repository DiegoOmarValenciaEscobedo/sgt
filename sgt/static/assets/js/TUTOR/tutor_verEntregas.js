$(document).ready(function () {
    $('#entregas').DataTable({
        responsive: true,   
        pagingType: 'numbers',
        
        scrollX: true,
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.12.1/i18n/es-MX.json"
        },
    });
});