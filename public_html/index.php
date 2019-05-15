<!doctype html>
<html>

	<head>
		<meta charset="utf-8">
		<title>Descarga de datos meteorológicos</title>
		<link href="/assets/css/bootstrap-grid.min.css" rel="stylesheet" />
		<link href="/assets/css/micss.css?<?=rand(0,9999)?>" rel="stylesheet" />
		<link href="/assets/css/bootstrap.min.css" rel="stylesheet" />
		<link href="/assets/noty/noty.css" rel="stylesheet" />
		<link href="/assets/noty/animate.css" rel="stylesheet" />
		<link rel="stylesheet"  href="/assets/noty/themes/relax.css" />
		<link rel="stylesheet"  href="/assets/datatable/jquery.dataTables.min.css" />
		<link rel="shortcut icon" href="/assets/images/umbrella.ico" type="image/x-icon">
	</head>
	
	<body background="/assets/images/nubes.jpg">
		<div class="espacio30"></div>	
		<div class="container">
		<div class="container-background">
		<h1 class="text-center">Descarga de datos meteorológicos</h1>
		<form name="consulta" id="consulta" class="form-padding">
			<div class="row justify-content-md-center">
				<div class="col-md-3 col">
					<label class="mr-sm-2" for="fuente"><b>Fuente de datos</b></label>
				</div>
				<div class="col-md-7 col"></div>
			</div>
			<div class="row justify-content-md-center">
				<div class="col-md-3 col">
					<select class="custom-select mr-sm-2" name="fuente" id="fuente" onChange="cambiarFormulario()">
						<option select value="0">Elija una fuente </option>
					    <option value="aemet">AEMET</option> 
				    	<option value="accuweather">Accuweather</option> 
				    	<option value="open">OpenWeatherMap</option> 
				    	<option value="tiempo">Tiempo.com</option> 
					</select>
				</div>
				<div class="col-md-7 col"></div>
			</div>
			<div class="espacio10"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2 col">
				<b>Variables</b>
			</div>
			<div class="col-md-8 col"></div>
		</div>
		<div class="espacio5"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-3 col">		
				<div class="form-check">
					<input type="checkbox" class="form-check-input" id="selectall" onClick="selectAll(this)" unchecked disabled/>
					<label class="form-check-label" for="selectall">Seleccionar/Borrar todas</label>
				</div>
			</div>
			<div class="col-md-7 col"></div>
		</div>				
		<div class="espacio10"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2 col">
				<b>Estado del Tiempo</b>
			</div>
			<div class="col-md-8 col"></div>
		</div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2 col">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="codEstadoTiempo" value="codEstadoTiempo" disabled>
    				<label class="form-check-label" for="codEstadoTiempo">Código Tiempo</label>
    			</div>
    		</div>	
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="descEstadoTiempo" value="descEstadoTiempo" disabled>
    				<label class="form-check-label" for="descEstadoTiempo">Descrip. Tiempo</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="visibilidad" value="visibilidad" disabled>
    				<label class="form-check-label" for="visibilidad">Visibilidad</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="altitudNubes" value="altitudNubes" disabled>
    				<label class="form-check-label" for="altitudNubes">Altitud Nubes</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="porcNubosidad" value="porcNubosidad" disabled>
    				<label class="form-check-label" for="porcNubosidad">Porc. Nubosidad</label>
    			</div>
    		</div>
    	</div>
    	<div class="espacio10"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2 col">
				<b>Sol</b>
			</div>
			<div class="col-md-8 col"></div>
		</div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2">
				<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="salidaSol" value="salidaSol" disabled> 
    				<label class="form-check-label" for="salidaSol">Salida Sol</label>
    			</div>
    		</div>
    		<div class="col-md-2">
				<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="puestaSol" value="puestaSol" disabled> 
    				<label class="form-check-label" for="puestaSol">Puesta Sol</label>
    			</div>
    		</div>
    		<div class="col-md-2">
				<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="cenitSol" value="cenitSol" disabled>
    				<label class="form-check-label" for="cenitSol">Cénit Sol</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="esDeDia" value="esDeDia" disabled>
    				<label class="form-check-label" for="esDeDia">Día o Noche</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="minLuz" value="minLuz" disabled>
    				<label class="form-check-label" for="minLuz">Minutos Luz</label>
    			</div>
    		</div>
    	</div>
    	<div class="espacio10"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2 col">
				<b>Precipitación</b>
			</div>
			<div class="col-md-8 col"></div>
		</div>
    	<div class="row justify-content-md-center">
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="precipitacion" value="precipitacion" disabled>
    				<label class="form-check-label" for="precipitacion">Precipitación</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="lluvia" value="lluvia" disabled>
    				<label class="form-check-label" for="lluvia">Lluvia</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="nieve" value="nieve" disabled>
    				<label class="form-check-label" for="nieve">Nieve</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="granizo" value="granizo" disabled> 
    				<label class="form-check-label" for="granizo">Granizo</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="cotaNieve" value="cotaNieve" disabled>
    				<label class="form-check-label" for="cotaNieve">Cota Nieve</label>
    			</div>
    		</div>
    	</div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="probPrecipitacion" value="probPrecipitacion" disabled>
    				<label class="form-check-label" for="probPrecipitacion">Prob. Precipit.</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="probLluvia" value="probLluvia" disabled>
    				<label class="form-check-label" for="probLluvia">Prob. Lluvia</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="probTormenta" value="probTormenta" disabled>
    				<label class="form-check-label" for="probTormenta">Prob. Tormenta</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="probNieve" value="probNieve" disabled>
    				<label class="form-check-label" for="probNieve">Prob. Nieve</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="probGranizo" value="probGranizo" disabled>
    				<label class="form-check-label" for="probGranizo">Prob. Granizo</label>
    			</div>
    		</div>
    	</div>
		<div class="espacio10"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-3 col">
				<b>Temperatura y Humedad</b>
			</div>
			<div class="col-md-7 col"></div>
		</div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="temperatura" value="temperatura" disabled>
    				<label class="form-check-label" for="temperatura">Temperatura</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="sensTermica" value="sensTermica" disabled>
    				<label class="form-check-label" for="sensTermica">Sensación Térmica</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="tempMax" value="tempMax" disabled> 
    				<label class="form-check-label" for="tempMax">Temperatura Máx.</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="tempMin" value="tempMin" disabled>
    				<label class="form-check-label" for="tempMin">Temperatura Mín.</label>
    			</div>
    		</div>
    		<div class="col-md-2"></div>
    	</div>
    	<div class="row justify-content-md-center">	
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="puntoRocio" value="puntoRocio" disabled>
    				<label class="form-check-label" for="puntoRocio">Punto Rocío</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="tempEPC" value="tempEPC" disabled> 
    				<label class="form-check-label" for="tempEPC">Temp. Hum. Aire</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="humedadRel" value="humedadRel" disabled>
    				<label class="form-check-label" for="humedadRel">Humedad Relativa</label>
    			</div>
    		</div>
    		<div class="col-md-4"></div>
    	</div>
		<div class="espacio10"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2 col">
				<b>Viento</b>
			</div>
			<div class="col-md-8 col"></div>
		</div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="dirViento" value="dirViento" disabled>
    				<label class="form-check-label" for="dirViento">Dirección Viento</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="velViento" value="velViento" disabled>
    				<label class="form-check-label" for="velViento">Velocidad Viento</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="velRachaMax" value="velRachaMax" disabled>
    				<label class="form-check-label" for="velRachaMax">Racha Máxima</label>
    			</div>
    		</div>
    		<div class="col-md-4"></div>
    	</div>		
		<div class="espacio10"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2 col">
				<b>Otros</b>
			</div>
			<div class="col-md-8 col"></div>
		</div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="presion" value="presion" disabled>
    				<label class="form-check-label" for="presion">Presión</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="presionNivMar" value="presionNivMar" disabled>
    				<label class="form-check-label" for="presionNivMar">Presión Nivel Mar</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="indiceUV" value="indiceUV" disabled>
    				<label class="form-check-label" for="indiceUV">Índice UV</label>
    			</div>
    		</div>
    		<div class="col-md-2">
    			<div class="form-check">
    				<input type="checkbox" class="form-check-input" name="vars[]" id="catUV" value="catUV" disabled>
    				<label class="form-check-label" for="catUV">Intensidad UV</label>
    			</div>
    		</div>
    		<div class="col-md-2"></div>
    	</div>			
		
		<div class="espacio20"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-3 col">
				<b>Intervalo de predicción</b>
			</div>
			<div class="col-md-7 col"></div>
		</div>
		<div class="espacio10"></div>
			<div class="row justify-content-md-center">
				<div class="col-md-1"> 
					<label for="example-date-input" class="col-form-label">Inicio:</label>
				</div>
				<div class="col-md-3">  
					<input class="form-control" id="fechaInicio" name="fechaInicio" type="date" min="2018-12-22" onChange="activaFin()" disabled required>
				</div>
				<div class="col-md-1">				
				</div>
				<div class="col-md-1">
				<label for="example-date-input" class="col-form-label">Fin:</label>
				</div>
				<div class="col-md-3">
					<input class="form-control" id="fechaFin" name="fechaFin" type="date" disabled required>
				</div>
				<div class="col-md-1"></div>
			</div>

		<div class="espacio20"></div>
		<div class="row justify-content-md-center">
    		<div class="col-md-3 col">
				<b>Horizonte de predicción</b>
			</div>
			<div class="col-md-7 col"></div>
		</div>
		<div class="row justify-content-md-center">
    		<div class="col-md-2">
    			<input type="radio" name="horizonte" id="seis" value="06" disabled required>
    			<label class="form-check-label" for="seis">6h</label>
    		</div>
    		<div class="col-md-2">
    			<input type="radio" name="horizonte" id="doce" value="12" disabled> 
    			<label class="form-check-label" for="doce">12h</label>
    		</div>
    		<div class="col-md-2">
    			<input type="radio" name="horizonte" id="veinticuatro" value="24" disabled>
    			<label class="form-check-label" for="veinticuatro">24h</label>
    		</div>
    		<div class="col-md-2">
    			<input type="radio" name="horizonte" id="cuarentayocho" value="48" disabled>
    			<label class="form-check-label" for="cuarentayocho">48h</label>
    		</div>
    		<div class="col-md-2">
    			<input type="radio" name="horizonte" id="todos" value="120" disabled>
    			<label class="form-check-label" for="todos">Todos</label>
    		</div>
    	</div>
		<div class="espacio20"></div>
		<div class="row">
			<div class="col-md-3"></div>
			<div class="col-md-2"><button class="btn btn-secondary" name="visualiza" id= "visualiza" disabled>Visualizar</button></div>
			<div class="col-md-2"></div>
			<div class="col-md-2"><button class="btn btn-secondary" name="descarga" id= "descarga" disabled>Descargar</button></div>
		</div>
		</form>
		<div class="espacio30"></div>
		<div id="tabla"></div>
		<div class="espacio30"></div>
		<script src="/assets/js/funciones.js?<?=rand(0,9999)?>" type="text/javascript"></script>
		<script src="/assets/noty/noty.min.js" type="text/javascript"></script>
		<script src="/assets/lib/js/jquery-1.8.2.min.js" type="text/javascript"></script>
		<script src="/assets/datatable/jquery.dataTables.min.js" type="text/javascript"></script>
	</div>
</div>
	</body>
</html>
