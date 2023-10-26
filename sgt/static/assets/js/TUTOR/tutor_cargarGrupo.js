const archivoSubido = document.getElementById('lista_alumnos');

class listaExcel{
    constructor(content){
        this.content = content
    }
    header(){
        return this.content[0]
    }
    rows(){
        return this.content.slice(1,this.content.length)
    }
}

async function validarArchivo(){
    var ruta = archivoSubido.value
    var extPer = /(.xls|.xlsx|.csv)$/i
    if(!extPer.exec(ruta)){
        Swal.fire({
            icon: 'error',
            title: 'Tipo de archivo no admitido',
            text: 'No has seleccionado un archivo con la extension requerida',
            confirmButtonText: 'Reintentar',
            confirmButtonColor: '#7c3030'
        })
        archivoSubido.value=''
        return false
    }else{
        const contenido = await readXlsxFile(archivoSubido.files[0])
        const lista = new listaExcel(contenido)
        filax = lista.header()
        if(filax && filax.length!=3){
            Swal.fire({
                icon: 'error',
                title: 'Ingrese la lista de archivos',
                text: 'Ingresaste un archivo con contenido diferente',
                confirmButtonText: 'Reintentar',
                confirmButtonColor: '#7c3030'
            })
            archivoSubido.value=''
            return false
        }else if(archivoSubido.files && archivoSubido.files[0]){
            document.getElementById('extra').style.display='none'
            nombre = archivoSubido.value
            document.getElementById('botones').innerHTML=
            '<span class="text-center mb-4"><br>Cargar Archivo<br>Lista de Alumnos</span>'+
            '<div class="row align-items-center justify-content-center text-center">'+
                '<a class="col-xs-2 nav-link active active-pro mt-1 text-center" href="">'+
                    '<span class="material-icons text-danger" title="Reintentar">replay</span>'+
                '</a>'+
                '<button class="material-icons text-success border " title="Subir grupo" type="submit">post_add</button>'+
            '</div>'

            const table = document.getElementById('example')
            lista.header().forEach(titulo=>{
                table.querySelector("thead>tr").innerHTML+='<td>'+titulo+'</td>'
            })
            lista.rows().forEach(fila=>{
                table.querySelector("tbody").innerHTML+='<tr>'
                +'<td>'+fila[0]+'</td>'
                +'<td>'+fila[1]+'</td>'
                +'<td>'+fila[2]+'</td>'
                +'</tr>'
            })

        }
    }
}

