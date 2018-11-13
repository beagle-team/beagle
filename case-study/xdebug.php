<?php

echo "debug mode activated.";

echo "<br>";

echo "Request URI: ";
echo $_SERVER['REQUEST_URI'];
echo '<br>';

echo "Query string: ";
echo $_SERVER['QUERY_STRING'];
echo '<br>';

echo "Clean path";
$path = str_replace("?".$_SERVER['QUERY_STRING'], '', $_SERVER['REQUEST_URI']);
echo $path;
echo '<br>';

$file = __DIR__.$path;
echo $file;

echo "<hr/>";

$file = (!empty($path)&&$path!=="/")?$file:__DIR__.'/index.php';

require $file;
