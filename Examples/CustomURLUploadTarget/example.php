<?php

// Select Custom URL and include the following URL: http://your_domain.com/path/to/this/example.php

	// Device will automatically include the following GET parameters in request. No need to add these parameters onto end of URL
	$user=$_GET["user"];
	$device=$_GET["device"];
	$file=$_GET["file"];
	$boxName=$_GET["boxname"];
	

	// A passing line will be in the POST body
	$postdata=trim(file_get_contents('php://input'));
	// $postdata == "6;100135;0000-00-00;1874.975;0;1;0;;;ba6ebc;0"
	// This is a race|result Passing file line. More information can be found here: https://www.raceresult.com/fw/support/documents/online-storage-api.pdf
	
	
	// As an example, this PHP will write the passing line POSTed to this server to a file 
	$file = fopen($boxName."/passings_".$file.".txt", "w");
	fwrite($file, $postdata);
	fclose($file);

	// Server must respond with body "OK", to confirm passing upload.
	echo "OK";
	
?>
