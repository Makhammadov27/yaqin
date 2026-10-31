<?php
declare(strict_types=1);
if(PHP_SAPI!=='cli'){http_response_code(404);exit;}
$c=(require dirname(__DIR__).'/config/config.php')['db'];if(!preg_match('/^[a-zA-Z0-9_]+$/D',$c['name']))throw new RuntimeException('Invalid database name');
$pdo=new PDO("mysql:host={$c['host']};port={$c['port']};charset=utf8mb4",$c['user'],$c['pass'],[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
$pdo->exec('CREATE DATABASE IF NOT EXISTS `'.$c['name'].'` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci');$pdo->exec('USE `'.$c['name'].'`');$pdo->exec(file_get_contents(dirname(__DIR__).'/database/schema.sql'));
if((int)$pdo->query('SELECT COUNT(*) FROM users')->fetchColumn()===0){$pdo->exec(file_get_contents(dirname(__DIR__).'/database/seed.sql'));echo "Schema and sample records installed.\n";}else echo "Schema exists; seeding skipped (users already exist).\n";
