<?php
declare(strict_types=1);
namespace App\Core;
final class Mailer {
 public static function send(string $name,string $email,string $message):bool{
 $c=(require dirname(__DIR__,2).'/config/config.php')['smtp'];$socket=null;try{
 foreach(['from','to']as $k)if(!filter_var($c[$k],FILTER_VALIDATE_EMAIL)||preg_match('/[\r\n]/',$c[$k]))return false;
 $socket=@stream_socket_client('tcp://'.$c['host'].':'.$c['port'],$errno,$errstr,3);if(!$socket)return false;stream_set_timeout($socket,3);
 $read=function(array $codes)use($socket):void{$line='';do{$part=fgets($socket,1024);if($part===false)throw new \RuntimeException('SMTP no response');$line=$part;}while(isset($part[3])&&$part[3]==='-');if(!in_array((int)substr($line,0,3),$codes,true))throw new \RuntimeException('SMTP rejected');};
 $cmd=function(string $s,array $codes)use($socket,$read):void{fwrite($socket,$s."\r\n");$read($codes);};$read([220]);$cmd('EHLO yaqin.local',[250]);$cmd('MAIL FROM:<'.$c['from'].'>',[250]);$cmd('RCPT TO:<'.$c['to'].'>',[250,251]);$cmd('DATA',[354]);
 $body="Ism: $name\nEmail: $email\n\n$message";$body=str_replace(["\r\n","\r"],"\n",$body);$body=preg_replace('/^\./m','..',$body);$body=str_replace("\n","\r\n",$body);fwrite($socket,'From: '.$c['from']."\r\nTo: ".$c['to']."\r\nSubject: Yaqin - aloqa xabari\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n".$body."\r\n.\r\n");$read([250]);fwrite($socket,"QUIT\r\n");return true;
 }catch(\Throwable){return false;}finally{if(is_resource($socket))fclose($socket);}
 }
}
