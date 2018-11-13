<?php

session_start();

include 'library.php';

$payload = $_SESSION['payload'];

welcome($payload);
