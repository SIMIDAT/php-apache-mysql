document.querySelector("#descarga").addEventListener("click", function(e){
	var selected = validacionCampos(e);
	var validacionNativa = document.getElementById("consulta").reportValidity();
	document.getElementById('consulta').action = "descarga.php";
	if(selected && validacionNativa){
		var formulario = document.querySelector("#consulta");
		var element = document.createElement('a');
  		element.setAttribute('download', filename);
    	e.preventDefault();
    }
});


document.querySelector("#visualiza").addEventListener("click", function(e){
	var selected = validacionCampos(e);
	var validacionNativa = document.getElementById("consulta").reportValidity();
	document.getElementById('consulta').action = "visualizacion.php";
	if(selected && validacionNativa){
		var formulario = document.querySelector("#consulta");
		ajaxPostTabla(formulario,function(ex,ex2){
		});

    	e.preventDefault();
    }
});

function mejorarTabla(){
	$('#resultados').DataTable({
		scrollX: 500,
		scrollY: 700,
		scrollCollapse: true,
		paging: false,
		//overflow: auto,
		language: {
			"sProcessing":     "Procesando...",
			"sLengthMenu":     "Mostrar _MENU_ registros",
			"sZeroRecords":    "No se encontraron resultados",
			"sEmptyTable":     "Ningún dato disponible en esta tabla",
			"sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
			"sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
			"sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
			"sInfoPostFix":    "",
			"sSearch":         "Buscar:",
			"sUrl":            "",
			"sInfoThousands":  ",",
			"sLoadingRecords": "Cargando...",
			"oPaginate": {
				"sFirst":    "Primero",
				"sLast":     "Último",
				"sNext":     "Siguiente",
				"sPrevious": "Anterior"
			},
			"oAria": {
				"sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
				"sSortDescending": ": Activar para ordenar la columna de manera descendente"
			}
		}
	});
}


function ajaxPostTabla (form, callback) {
    var url = form.action,
        xhr = new XMLHttpRequest();
    var params = [].filter.call(form.elements, function(el) {
        return el.type != "checkbox" || el.checked;
    })
    .filter(function(el){
        return el.type != "radio" || el.checked;
    })
    .map(function(el) {
        return encodeURIComponent(el.name) + '=' + encodeURIComponent(el.value);
    }).join('&');
    var url2 = url +"?"+ params;
    xhr.open("GET", url2);
    xhr.setRequestHeader("Content-type", "application/x-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        	document.getElementById("tabla").style="display: none;";
           	document.getElementById("tabla").innerHTML = this.responseText;
           	document.getElementById("tabla").style="display: initial;";
           	mejorarTabla();
           	document.getElementById("tabla").scrollIntoView();	
        }
    };
    xhr.send(null);
}


function cambiarFormulario(){
	var form = document.forms[0];
	selectAll(this);
	form.selectall.checked = false;
	document.getElementById('fechaInicio').value = '';
	document.getElementById('fechaFin').value = '';
	document.getElementById('fechaFin').disabled = true;
	var radios = document.getElementsByName('horizonte');
	for(var i in radios){
		radios[i].checked = false;
	}
	deshabilitarHabilitarCampos();
	var fecha = new Date();
	fecha.setDate(fecha.getDate());
	var fechaMax = convierteFecha(fecha);
	document.getElementById('fechaInicio').max = fechaMax;	
}


function selectAll(source) {
	var checkboxes = document.getElementsByName('vars[]');
	for(var i in checkboxes){
		if(checkboxes[i].disabled == false){
			checkboxes[i].checked = source.checked;
		}
	}
}


function validacionCampos(e) {
	var checkboxes = document.getElementsByName('vars[]');
	var selected = false;
	for(var i in checkboxes){
		if(checkboxes[i].checked){
			selected = true;
		}
	}
	if (!selected){
		new Noty({
			theme: 'relax',
		    type: 'error',
		    layout: 'topRight',
		    text: 'Selecciona al menos una variable',
		    timeout: 5000,
		    animation: {
		        open: 'animated bounceInRight',
		        close: 'animated bounceOutRight'
   			 }
		}).show();
		e.preventDefault();
	}
	return(selected);
}


function deshabilitarHabilitarCampos(){
	form = document.forms[0];
	switch(form.fuente.selectedIndex){
		case 0:
			for (var i = 1, len = form.elements.length; i < len; ++i){
				form[i].disabled = true;
			}
			break;
		case 1:
			activos = ["codEstadoTiempo", "descEstadoTiempo", "temperatura", "dirViento", "velViento", "humedadRel", "precipitacion", "nieve", "sensTermica", "velRachaMax", "salidaSol", "puestaSol", "minLuz", "probPrecipitacion", "probNieve", "probTormenta", "visualiza", "fechaInicio", "selectall", "descarga", "seis", "doce", "veinticuatro", "cuarentayocho", "todos"]; 
			for (i in activos){
				s = "form." + activos[i] + ".disabled=false";
				eval(s);
			}
			inactivos = ["porcNubosidad", "lluvia", "presion", "cenitSol", "esDeDia", "granizo", "probLluvia", "probGranizo", "cotaNieve", "tempMax", "tempMin", "tempEPC", "puntoRocio", "altitudNubes", "visibilidad", "presionNivMar", "indiceUV", "catUV"];
			for (i in inactivos){
				s = "form." + inactivos[i] + ".disabled=true";
				eval(s);
			}
			break;
		case 2: 
			activos = ["codEstadoTiempo", "descEstadoTiempo", "temperatura", "dirViento", "velViento", "humedadRel", "precipitacion", "nieve", "sensTermica", "velRachaMax", "probPrecipitacion", "probNieve", "porcNubosidad", "lluvia", "esDeDia", "granizo", "probLluvia", "probGranizo", "tempEPC", "puntoRocio", "altitudNubes", "visibilidad", "indiceUV", "catUV", "visualiza", "fechaInicio", "selectall", "descarga", "seis", "doce", "todos"]; 
			for (i in activos){
				s = "form." + activos[i] + ".disabled=false";
				eval(s);
			}
			inactivos = ["presion", "cenitSol", "salidaSol", "puestaSol", "minLuz", "probTormenta",  "cotaNieve", "tempMax", "tempMin", "presionNivMar", "veinticuatro", "cuarentayocho"];
			for (i in inactivos){
				s = "form." + inactivos[i] + ".disabled=true";
				eval(s);
			}
			break;
		case 3: 
			activos = ["codEstadoTiempo", "descEstadoTiempo", "temperatura", "dirViento", "velViento", "humedadRel", "nieve","porcNubosidad", "lluvia", "presion", "tempMax", "tempMin", "presionNivMar", "visualiza", "fechaInicio", "selectall", "descarga", "seis", "doce", "veinticuatro", "cuarentayocho", "todos"]; 
			for (i in activos){
				s = "form." + activos[i] + ".disabled=false";
				eval(s);
			}
			inactivos = ["cenitSol", "esDeDia", "granizo", "probLluvia", "probGranizo", "cotaNieve", "tempEPC", "puntoRocio", "altitudNubes", "visibilidad", "indiceUV", "catUV", "precipitacion", "sensTermica", "velRachaMax", "salidaSol", "puestaSol", "minLuz", "probPrecipitacion", "probNieve", "probTormenta"];
			for (i in inactivos){
				s = "form." + inactivos[i] + ".disabled=true";
				eval(s);
			}
			break;
		case 4: 
			activos = ["codEstadoTiempo", "descEstadoTiempo", "temperatura", "dirViento", "velViento", "humedadRel", "precipitacion", "porcNubosidad", "presion", "sensTermica", "velRachaMax", "salidaSol", "puestaSol", "minLuz", "cenitSol", "cotaNieve", "visualiza", "fechaInicio", "selectall", "descarga", "seis", "doce", "veinticuatro", "cuarentayocho", "todos"]; 
			for (i in activos){
				s = "form." + activos[i] + ".disabled=false";
				eval(s);
			}
			inactivos = [ "lluvia", "esDeDia", "granizo", "probLluvia", "probGranizo", "tempMax", "tempMin", "tempEPC", "puntoRocio", "altitudNubes", "visibilidad", "presionNivMar", "indiceUV", "catUV", "nieve", "probPrecipitacion", "probNieve", "probTormenta"];
			for (i in inactivos){
				s = "form." + inactivos[i] + ".disabled=true";
				eval(s);
			}
			break;
	}
}


function convierteFecha(fecha){
	var dia = fecha.getDate();
	var mes = fecha.getMonth() + 1;
	var anho = fecha.getFullYear();
	if(dia < 10) {
    	dia = '0' + dia;
	} 

	if(mes < 10) {
    	mes = '0' + mes;
	}
	var fechaMax = anho + '-' + mes + '-' + dia;
	return(fechaMax)
}


function activaFin(e) {
	var fechaInicio = document.getElementById('fechaInicio').value;
	document.getElementById('fechaFin').disabled = false;
	document.getElementById('fechaFin').min = fechaInicio;
	var fecha = new Date();
	horaAct = fecha.getHours();
	form = document.forms[0];
	switch(form.fuente.selectedIndex){
		case 1:		
			if(horaAct  < 9){
				fecha.setDate(fecha.getDate() + 1);
			}else{
				fecha.setDate(fecha.getDate() + 2);
			}
			var fechaMax = convierteFecha(fecha);
			document.getElementById('fechaFin').max = fechaMax;
			break;
		case 2:
			if(horaAct  < 12){
				fecha.setDate(fecha.getDate());
			}else{
				fecha.setDate(fecha.getDate() + 1);
			}
			var fechaMax = convierteFecha(fecha);
			document.getElementById('fechaFin').max = fechaMax;
			break;
		case 3:
			if(horaAct  < 12){
				fecha.setDate(fecha.getDate() + 4);
			}else{
				fecha.setDate(fecha.getDate() + 5);
			}
			var fechaMax = convierteFecha(fecha);
			document.getElementById('fechaFin').max = fechaMax;
			break;
		case 4:
			fecha.setDate(fecha.getDate() + 2);
			var fechaMax = convierteFecha(fecha);
			document.getElementById('fechaFin').max = fechaMax;
			break;
	}
}