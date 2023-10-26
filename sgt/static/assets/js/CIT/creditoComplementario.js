document.write('<script src="/static/assets/js/CIT/html2pdf.js"></script>');

function gen_cons(nombre) {

    const $doc = 
        '<!DOCTYPE html>'+
        '<html lang="es">'+
        '<body background="/static/assets/img/icons/Bgg.jpg" style="">'+
            '<img src="/static/assets/img/icons/logoEducacion.jpg" style="width:500px; margin-left:50px;">'+
            '<img src="/static/assets/img/icons/logoTNM.png" style="width:220px; margin-left:100px;">'+
            '<div align="right" style="margin-right:140px; margin-top:20px;">'+
                '<b>Instituto Tecnológico de Morelia</b><br>'+
                'Subdirección Académica<br>'+
                'Departamento de Desarrollo Académico'+
            '</div>'+
            '<div align="center" style=" margin-top:20px;">'+
                '<b>"2020, Año de Leona Vicario, Benemérita Madre de la patria"</b>'+
            '</div>'+
            '<div align="right" style="margin-right:140px; margin-top:20px;">'+
                'DEPENDENCIA:    SUBD. ACADÉMICA<br>'+
                'SECCION:        DESARROLLO ACADEMICO<br>'+
                'OFICIO:         D.A.009.554/2022<br><br>'+
                'Morelia, Mich., 07/Noviembre/2022<br><br>'+
                'ASUNTO: Liberación de créditos complementarios'+
            '</div>'+
            '<div style="margin-left:120px; margin-right:120px; margin-top:20px;">'+
                '<b>A QUIEN CORRESPONDA</b><br><br><br>'+
                'La que suscribe Jefa del Departamento de Desarrollo Académico por medio del '+
                'presente, hago constar que el (la) C. <b>Valencia Escobedo Diego Omar</b> alumno(a) de '+
                'nuestro Instituto con el número de control <b>19121086</b> de la carrera <b>Ingeniería en '+
                'sistemas computacionales</b>, asistió a tutorias durante el semestre <b>Agosto - '+
                'diciembre 2019</b>, siendo su tutor el (la) C. Profesor(a) <b>J. Guadalupe Ramos Díaz.</b>'+
            '</div>'+
            '<div style="margin-left:120px; margin-right:120px; margin-top:20px;">'+
                'Se extiende la presente con la finalidad de que le sea acreditado un créditos'+
                'complementario en base a acuerdo con el Comité Académico. Sin mas por el momento'+
                'quedo a sus ordenes para cualquier aclaración.'+
            '</div>'+
            '<div style="margin-left:120px; margin-top:50px;">'+
                '<b>ATENTAMENTE</b><br>'+
                '<b>Técnica, Progreso de México</b>'+
            '</div>'+
            '<div style="margin-left:120px; margin-top:80px;">'+
                '<b>C. Liliana Patricia Ferreyra Herrera</b><br>'+
                '<b>Jefa del Departamento de Desarrollo Académico</b>'+
            '</div>'+
            '<hr size="2px" color="black" style="margin-left:120px; margin-right:120px; margin-top:200px;"/>'+
            '<div style="margin-left:120px; margin-right:120px; margin-top:20px; display:inline;">'+
                '<img src="/static/assets/img/icons/logoITM.png" style="width:50px; margin-left:0px;">'+
                '<img src="/static/assets/img/icons/logoANFEI.png" style="width:53px; margin-left:0px;">'+
                '<img src="/static/assets/img/icons/logoPony.png" style="width:57px; margin-left:0px;">'+
                '<div align="center" style="display:inline-block; margin-left:0px; margin-right:0px;">'+
                    'Av. Tecnológico 1500, Col. Lomas de Santiaguito,<br>'+
                    'C. P. 58120, Morelia, Michoacán. Tel. (443) 312 15 70,<br>'+
                    'Ext. 218, E-mail: desarrollo@morelia.tecnm.mx<br>'+
                    '<b>www.tecnm.mx | www.morelia.tecnm.mx</b>'+
                '</div>'+
                '<img src="/static/assets/img/icons/logoPlastico.png" style="width:100px; margin-left:0px;">'+
                '<img src="/static/assets/img/icons/logoISO.png" style="width:55px;">'+
            '</div>'+
        '</body>'+
        '</html>'
    const $elementoParaConvertir = $doc; // <-- Aquí puedes elegir cualquier elemento del DOM
    html2pdf().set({
        margin: 1,
        filename: 'documento.pdf',
        image: {
            type: 'jpeg',
            quality: 0.98
        },
        html2canvas: {
            scale: 3, // A mayor escala, mejores gráficos, pero más peso
            letterRendering: true,
        },
        jsPDF: {
            unit: "in",
            format: "a3",
            orientation: 'portrait' // landscape o portrait
        }
    })
        .from($elementoParaConvertir)
        .save()
        .catch(err => console.log(err));
}