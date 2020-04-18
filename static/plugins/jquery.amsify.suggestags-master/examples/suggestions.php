<?php

//$post 		= json_decode(file_get_contents('php://input'), true);

$suggestions 	= ['India', 'Pakistan', 'Nepal', 'UAE', 'Iran', 'Bangladesh'];
$data 			= [];
foreach($suggestions as $suggestion)
{
	if(strpos(strtolower($suggestion), strtolower($_GET['term'])) !== false)
	{
		$data[] = $suggestion;	
	}
}

header('Content-Type: application/json');
echo json_encode(['suggestions' => $data]);