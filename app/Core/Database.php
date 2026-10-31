<?php
declare(strict_types=1);
namespace App\Core;
use PDO;
final class Database {
 private static ?PDO $pdo=null;
 public static function connection():PDO { if(self::$pdo)return self::$pdo;$c=(require dirname(__DIR__,2).'/config/config.php')['db'];return self::$pdo=new PDO("mysql:host={$c['host']};port={$c['port']};dbname={$c['name']};charset=utf8mb4",$c['user'],$c['pass'],[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC,PDO::ATTR_EMULATE_PREPARES=>false]); }
}
