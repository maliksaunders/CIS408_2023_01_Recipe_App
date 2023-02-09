<?php

include("connect.php");

if(isset($_POST['submit'])) {
	$query = mysqli_query($conn,
	"INSERT INTO REGISTER SET firstname='". $_POST["firstname"] . "',lastname ='". $_POST["lastname"]. "',
		username ='". $_POST["username"] . "',password ='". $_POST["pwd"] . "'");	
	
	echo "alert('You Registered Successfully, Login now')";
}
?>

<html>

	<head>
		<meta charset="utf-8">
		<title>Register Page</title>
		<style>
			th {text-align: left;}
			td {text-align: center;}
			a {text-decoration: none;}
		</style>
	</head>

	<body>
		<a href="login.php" style="font-size:30px; float:right;">Login</a>
		<form method="post" action="index.php" name="frm1">

			<fieldset>
				<legend align="center"><h1>Register Here</h1></legend>
				<table align="center" border="1"width="40%" style="border:thick;">
					<tr>
						<th height="40"><label for="firstname">First Name</label></th>
						<td><input type="text" name="firstname" id="firstname" required></td>
					</tr>
					<tr>
						<th height="40"><label for="lastname">Last Name</label></th>
						<td><input type="text" name="lastname" id="lastname" required></td>
					</tr>
					<tr>
						<th height="40"><label for="username">Username</label></th>
						<td><input type="text" name="username" id="username" required></td>
					</tr>
						<th height="40"><label for="pwd">Password</label></th>
						<td><input type="password" name="pwd" id="pwd" required></td>
					</tr>
					<tr>
						<td height="40" colspan="2"><input type="submit" name="submit" value="Register"> </td>
					</tr>
				</table>
			</fieldset>
		</form>
	</body>
</html>
