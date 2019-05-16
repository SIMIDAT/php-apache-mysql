<?php
	$servername = "mariadb";
	$username = "root";
	$database = "predicciones";

	$conn = new mysqli($servername, $username, $password, $database);
	$conn->set_charset("utf8");

	$variables = "STR_TO_DATE(fechaPrediccion, '%Y%m%d %H'), periodoPredicho";
	foreach ($_GET['vars'] as $var){
		$variables = $variables.", ".$var;
	}
	
	date_default_timezone_set('Europe/Madrid');
	$fechaFin = date('Y-m-d H:i:s', strtotime($_GET['fechaFin'].' +1 day'));

	$result = $conn->query("SELECT $variables 
							FROM ".$_GET['fuente']." 
							WHERE periodoPredicho >='".$_GET['fechaInicio']."' AND periodoPredicho <'".$fechaFin."'
							AND HOUR(TIMEDIFF(periodoPredicho, STR_TO_DATE(fechaPrediccion, '%Y%m%d %H'))) < ".$_GET['horizonte'].
							" ORDER BY periodoPredicho, fechaPrediccion");
?>

<div class="row justify-content-md-center">
	<div class="col-md-10 col">
		<table class='table rayada' id='resultados' style="width:100%">
			<thead>
				<tr>
					<th scope='col'>FechaPredicción</th>
					<th scope='col'>FechaPredicha</th>
					<?php foreach ($_GET['vars'] as $var): ?>
							<th scope='col'><?=$var; ?></th>
					<?php endforeach; 
					?>
				</tr>
			</thead>
			<tbody>
			<?php while ($row = $result->fetch_row()): ?>
				<tr>
					<?php for ($i = 0; $i <= count($_GET['vars']) + 1; $i++): ?>
							<td><?=$row[$i]; ?></td>
					<?php endfor; ?>
				</tr>
			<?php endwhile;
			$result->close();
			?>
			</tbody>
		</table>
	</div>
</div>
