$(document).ready(function () {
    $('.dataGrupo').DataTable({
        responsive: true,   
        pagingType: 'numbers',
        "autoWidth": false,
        scrollX: true,
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.12.1/i18n/es-MX.json"
        },
    });
});