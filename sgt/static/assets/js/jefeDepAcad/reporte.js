$(document).ready(function () {
    $('#reporte').DataTable({
        responsive: true,   
        pagingType: 'numbers',
        autoWidth: true,
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
                    text: 'Guardar',
                    className: 'btn btn-outline-success',
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
                          cells: ['A1:G-0'],
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
                            cells: ['A3'],
                            content: 'NOMBRE DEL COORDINADOR DE TUTORÍA DEL DEPARTAMENTO ACADÉMICO: Amaury Coria',
                            pushRow: true
                        },
                        {
                            cells: ['F3'],
                            content: 'Fecha: 23/10/2022'
                        },
                        {
                            cells: ['A4'],
                            content: 'Programa Educativo: 2022',
                            pushRow: true
                        },
                        {
                            cells: ['F4'],
                            content: 'Hora: 23:13',
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
                            cells: ['E5'],
                            content: 'Estudiantes canalizados en el semestre',
                        },
                        {
                            cells: ['F5'],
                            content: 'Área Canalizada',
                        },

                    ],
                    pageStyle: {
                        mergeCells: {                   // Merge Cells
                            mergeCell: [
                                'A2:F2',
                                'A3:E3',
                                'A4:E4',
                                'A5:A6',
                                'B5:B6',
                                'C5:D5',
                                'E5:E6',
                                'F5:F6'
                            ]
                        }
                    }
                }
            ]
        }
    });


});