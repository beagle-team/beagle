<?php

session_start();
if (isset($_GET['payload']) &&
    !preg_match('/(.*\d.*){6,}/', $_GET['payload'])) {

    $_SESSION['payload'] = $_GET['payload'];
    //[Original]
    // assert false
    echo "<a href='welcome.php'>Welcome page</a>";
    echo "<br/>";
    echo "<a href='signup.php'>Signup page</a>";

} else {
    header("Location: signup.php");
}
