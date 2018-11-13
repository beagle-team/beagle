<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Landing page</title>
    <script
        src="https://code.jquery.com/jquery-3.3.1.min.js"
        integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
        crossorigin="anonymous"></script>
    <script>
        function load_page() {
            $("#content").load("loaded_page.html");
        }
    </script>
</head>
<body>
    <div>
        <ul>
            <li><a href="#">Nothing here</a></li>
            <li><a href="#">Nothing here either</a></li>
            <li><a href="xss.php">XSS page</a></li>
            <li><a onclick="load_page()" href="#">Load more stuff</a></li>
        </ul>
    </div>
    <div id="content"></div>
</body>
</html>
