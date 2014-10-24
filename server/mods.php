<?php
function get_allfiles($path,&$files) {
    if(is_dir($path)){
        $dp = dir($path);
        while ($file = $dp ->read()){
            if($file !="." && $file !=".."){
                get_allfiles($path."/".$file, $files);
            }
        }
        $dp ->close();
    }
    if(is_file($path)){
        $files[] =  $path;
    }
}

function get_filenamesbydir($dir){
    $files =  array();
    get_allfiles($dir,$files);
    return $files;
}

$versions = json_decode(file_get_contents("version.conf"), true);
$currentversion = $versions[$_GET["version"]];
if ($_GET["source"] == "server")
    {$path = $currentversion["server_path"];}
else if ($_GET["source"] == "client")
    {$path = $currentversion["client_path"];}
chdir("$path/mods");
$filenames = get_filenamesbydir(".");

print_r(json_encode($filenames));
