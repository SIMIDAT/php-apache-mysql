<?php
	$servername = "mariadb";
	$username = "root";
	$database = "predicciones";
	$delimiter = ";";

	$conn = new mysqli($servername, $username, $password, $database);

	$variables = "fechaPrediccion, periodoPredicho";
	$fields = array("fechaPrediccion", "periodoPredicho");
	foreach ($_GET['vars'] as $var){
		$variables = $variables.", ".$var;
	}

	$filename = $_GET['fuente'].str_replace("-", "", $_GET['fechaInicio']).str_replace("-", "", $_GET['fechaFin']).".csv";
	date_default_timezone_set('Europe/Madrid');
	$fechaFin = date('Y-m-d H:i:s', strtotime($_GET['fechaFin'].' +1 day'));

	$f = fopen($filename, 'w');

	$result = $conn->query("SELECT $variables 
							FROM ".$_GET['fuente']." 
							WHERE periodoPredicho >='".$_GET['fechaInicio']."' AND periodoPredicho <'".$fechaFin."'
							AND HOUR(TIMEDIFF(periodoPredicho, STR_TO_DATE(fechaPrediccion, '%Y%m%d %H'))) < ".$_GET['horizonte'].
							" ORDER BY periodoPredicho, fechaPrediccion");

	foreach ($_GET['vars'] as $var){
		array_push($fields, $var);
	}
	fputcsv($f, $fields, $delimiter);

	while ($row = $result->fetch_row()){
		$lineData = array();
		for ($i = 0; $i <= count($_GET['vars']) + 1; $i++){
			array_push($lineData, $row[$i]);
		}
		fputcsv($f, $lineData, $delimiter);
	}

	$result->close();	

    fseek($f, 0);
    fpassthru($f);
    fclose($f);

	header("Content-Disposition: attachment; filename=$filename");
 
	readfile($filename);
	unlink($filename);
?>






         

  


