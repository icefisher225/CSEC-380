<?php
ini_set("request_order", "GPC");
include_once("common.php");
$has_session = false;
if(isset($_COOKIE["ARM_SESSION"])){
	$session_id = $_COOKIE["ARM_SESSION"];
	// Get Data
	//if($stmt = $mysqli->prepare("SELECT * from sessions where session_id=?")){
		//if($stmt->bind_param("s", $session_id)){
			//if(!$stmt->execute()){
			//	die("Error - Issue executing prepared statement: " . mysqli_error($mysqli));
			//}
	$stmt = "SELECT * from sessions where session_id='" . $session_id . "'";
	# SELECT * from sessions where session_id='1' or user_id='25'
	$result = $mysqli->query($stmt);
	$row = $result->fetch_assoc();
	if($result->num_rows != 1){
		die('Error - There is an issue with the database, contact your administrator');
	}else{
		$has_session = true;
		$real_user = $row['user_id'];
		$id_to_get = $row['user_id'];
		$ip = $row['ip'];
		$born = $row['born'];
		$valid = $row['valid'];
	
	}
	
}else{
	$has_session = false;
}
if($has_session){
	$destroy = false;
	if (!isset($ip) or !isset($id_to_get)){
		die("<script>window.location.href = '/index.php';</script>Invalid Session");
	}
	if($_SERVER['REMOTE_ADDR'] !== $ip){
		$destroy = true;
	}
	if($born < time() - 300){
		$destroy = true;	
	}
	if($valid != 1){
		$destroy = true;
		die("valid");
	}
	if($destroy===true){
		die("<script>window.location.href = '/index.php';</script>Invalid Session");
	}
	// Reset our counter
	$timeNow = time();
	if($stmt = $mysqli->prepare("UPDATE sessions SET born=? where user_id=?")){
		if($stmt->bind_param("ii",$timeNow,$real_user)){
			if(!$stmt->execute()){
				die("Error - Issue executing prepared statement: " . mysqli_error($mysqli));
			}
		}else{
			die("Error - Issue binding prepared statement: " . mysqli_error($mysqli));
		}
		if($stmt->close()){
			// We were succesful.
		}else{
			die("Error - Failed to close prepared statement" . mysqli_error($mysqli));
		}
	}else{
			die("Error - Issue preparing statement: " . mysqli_error($mysqli));
	}
	// If the user is asking for some other persons info
	if(isset($_GET['id'])){
		$id_to_get = $_GET['id'];
	}	
	// If the array isn't us
	if($id_to_get === $real_user){
		die("There was an issue contact your administrator");
	}
	// If the element is numeric
	if(!is_numeric($id_to_get)){
		die("There was an issue contact your administrator");
	}
	
	
	if($stmt = $mysqli->prepare("SELECT friends from profiles where user_id=?")){
		if($stmt->bind_param("i",$real_user)){
			if(!$stmt->execute()){
				die("Error - Issue executing prepared statement: " . mysqli_error($mysqli));
			}
			if($res = $stmt->get_result()){
				$row = $res->fetch_assoc();
				$friends = $row['friends'];
			}else{
				die("Error - Getting results: " . mysqli_error($mysqli));
			}
		}else{
			die("Error - Issue binding prepared statement: " . mysqli_error($mysqli));
		}
		if($stmt->close()){
			// We were succesful.
		}else{
			die("Error - Failed to close prepared statement" . mysqli_error($mysqli));
		}
	}else{
			die("Error - Issue preparing statement: " . mysqli_error($mysqli));
	}
	
	
	$friends = explode(',',$friends);
	// If it's already in the array
	if(array_search($id_to_get,$friends)){
		die("There was an issue contact your administrator");
	}	
	array_push($friends,$id_to_get);
	$ids = implode(',',$friends);
	if($stmt = $mysqli->prepare("UPDATE profiles SET Friends=? WHERE user_id=?")){
		if($stmt->bind_param("si", $ids, $real_user)){
			if(!$stmt->execute()){
				die("Error - Issue executing prepared statement: " . mysqli_error($mysqli));
			}
		}else{
			die("Error - Issue binding prepared statement: " . mysqli_error($mysqli));
		}
		if($stmt->close()){
			echo "True - Friend Added Successfully";
		}else{
			die("Error - Failed to close prepared statement" . mysqli_error($mysqli));
		}
	}else{
		die("Error - Issue preparing statement: " . mysqli_error($mysqli));
	}
}
?>
