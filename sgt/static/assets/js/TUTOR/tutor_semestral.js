$(document).ready(function () {
    var name = 'NOMBRE DEL TUTOR: '+ document.getElementById('nombre').value.toString();
    var group = 'Grupo: '+ document.getElementById('grupo').value.toString();
    var fecha = Date.now();
    var fecha1 = new Date();
    var hoy = new Date(fecha).toLocaleDateString();
    var now = 'Fecha: ' + hoy;
    var descarga = 'Reporte - ' + document.getElementById('nombre').value.toString() + ' - ' + document.getElementById('grupo').value.toString();

    var table = $('#reporte').DataTable({
        responsive: true,   
        pagingType: 'numbers',
        autoWidth: true,
        select: true,
        scrollX: true,
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.12.1/i18n/es-MX.json"
        },
        //Excel
        dom: "Bfrtip",
        buttons: {
            dom: {
                button: {
                    className: 'btn'
                }
            },
            buttons:[
                {
                    extend: "excel",
                    text: 'Descargar Reporte',
                    className: 'btn btn-success',
                    title: descarga,
                    excelStyles: [
                        {
                        cells:'1',
                        style: {
                            font: {
                                name: "Calibri",
                                size: "11",
                                color: "FFFFFF",
                                b: true
                            },
                            fill: {
                                pattern: {
                                    color: "000000"
                                }
                            }
                        }
                        },
                        {
                        cells: ['A2:F2', 'A3:G3', 'A4:G4', 'A5:G6'],
                        style: {
                            font: {
                                name: "Calibri",
                                size: "11",
                                color: "000000",
                                b: true
                            },
                            alignment: {
                                vertical: "center",
                                horizontal: "center",
                            },
                            fill: {
                                pattern: {
                                    color: "DDD9C4"
                                }
                            },
                        }
                        },
                        {
                          cells: ['A7:G-0'],
                          style: {
                            border: {
                                top: {
                                    style: 'thin'
                                },
                                bottom: {
                                    style: 'thin'
                                },
                                left: {
                                    style: 'thin'
                                },
                                right: {
                                    style: 'thin'
                                },
                            }
                          } 
                        },
                    ],
                    insertCells: [
                        {
                            cells: ['A2'],
                            content: 'INSTITUTO TECNOLÓGICO DE MORELIA:',
                            pushRow: true
                        },
                        {
                            cells: ['G2'],
                            content: document.getElementById('dep').value.toString(),
                        },
                        {
                            cells: ['A3'],
                            content: name,
                            pushRow: true
                        },
                        {
                            cells: ['F3'],
                            content: now,
                        },
                        {
                            cells: ['A4'],
                            content: 'Programa Educativo: 2022',
                            pushRow: true
                        },
                        {
                            cells: ['C4'],
                            content: group,
                        },
                        {
                            cells: ['F4'],
                            content: 'Hora: ' +fecha1.getHours() +':'+ fecha1.getMinutes(),
                        },
                        {
                            cells: ['A6'],
                            content: '',
                            pushRow: true
                        },
                        {
                            cells: ['C5'],
                            content: 'Estudiantes atendidos en el semestre',
                        },
                        {
                            cells: ['C6'],
                            content: 'Tutoria Grupal',
                        },
                        {
                            cells: ['D6'],
                            content: 'Tutoría individual',
                        },
                        {
                            cells: ['F6'],
                            content: 'Observaciones',
                        },
                        {
                            cells: ['G6'],
                            content: '% Asistencia',
                        },
                        {
                            cells: ['F5'],
                            content: 'Área Canalizada',
                        },
                        // {
                        //     cells: ['C7'],
                        //     content:  
                        // },

                    ],
                    pageStyle: {
                        mergeCells: {                   // Merge Cells
                            mergeCell: [
                                'A2:F2',
                                'A3:E3',
                                'F3:G3',
                                'A4:B4',
                                'C4:E4',
                                'F4:G4',
                                'A5:A6',
                                'B5:B6',
                                'C5:D5',
                                'E5:E6',
                                'F5:G5'
                            ]
                        }
                    }
                },
            ]
        }
    });
    
    $('#btnsave').click(function () {
        var row = table.cell(0).data();
        var data = row.toString();
        alert(row)
    });
    // var aux;
    $('#reporte tbody').on( 'click', 'td', function () {
        var control = table.cell(this,0).data();
        var nombre = table.cell(this,1).data();
        var aux = table.row(this).index();
        document.getElementById('id_noControl').value = control;
        document.getElementById('id_nombre').value = nombre;
        $("#exampleModal").modal("show");
        // var rowModal = table.row(this).index();
        // alert(aux)
    } );
    // rowModal = aux;
    // alert(rowModal)
    // document.getElementsByClassName("btnModal")[].addEventListener("click", function(){
    //     $("#exampleModal").modal("show");
    // });


});