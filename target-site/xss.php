<?php

//[Derived]
//@ assert isset($_GET['payload']) && $_GET['payload'].contains("<script>.*</script>");
if (isset($_GET['payload']) && !empty($_GET['payload'])) {
    //[Derived]
    //@ assert $_GET['payload'].contains("<script>.*</script>");
    $payload = $_GET['payload'];
    //[Original]
    //@ assert arg1.contains("<script>.*</script>");
    echo "$payload";
} else {
    //[Original]
    //@ assert arg1.contains("<script>.*</script>"); 
    // == assert false;
    echo '
    <form action="xss.php" method="GET">
        <input type="text" name="payload">
        <input type="submit">
    </form>
    <a href="f.php">
    ';
}
