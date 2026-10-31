<?php
declare(strict_types=1);
namespace App\Core;
use App\Models\Store;
class HttpError extends \RuntimeException {public function __construct(public int $status,string $message){parent::__construct($message);}}
abstract class Controller {
 protected Store $store;protected ?array $user;
 public function __construct(){ $this->store=new Store();$this->user=isset($_SESSION['uid'])?$this->store->find('users',(int)$_SESSION['uid']):null; }
 protected function auth(array $roles=[]):array{if(!$this->user)throw new HttpError(401,'Davom etish uchun tizimga kiring.');if($roles&&!in_array($this->user['role'],$roles,true))throw new HttpError(403,'Bu amal uchun huquqingiz yetarli emas.');return $this->user;}
 protected function post():void{if($_SERVER['REQUEST_METHOD']!=='POST')throw new HttpError(405,'Faqat POST so‘rovi qabul qilinadi.');if(!is_string($_POST['csrf']??null)||!hash_equals($_SESSION['csrf'],$_POST['csrf']))throw new HttpError(403,'CSRF token noto‘g‘ri. Sahifani yangilab qayta urinib ko‘ring.');}
 protected function text(string $key,int $min,int $max):string{$v=trim(is_string($_POST[$key]??null)?$_POST[$key]:'');$length=mb_strlen($v);if($length<$min||$length>$max)throw new HttpError(422,"{$key}: uzunligi {$min}–{$max} belgi bo‘lishi kerak.");return $v;}
 protected function id(string $key='id',bool $post=false):int{$v=filter_var(($post?$_POST:$_GET)[$key]??null,FILTER_VALIDATE_INT,['options'=>['min_range'=>1]]);if(!$v)throw new HttpError(422,'Yozuv identifikatori noto‘g‘ri.');return $v;}
 protected function listingAccess(int $id,bool $write=false):array{$x=$this->store->listing($id);if(!$x)throw new HttpError(404,'E’lon topilmadi.');if($write){$u=$this->auth();if($u['role']!=='admin'&&(int)$x['user_id']!==(int)$u['id'])throw new HttpError(403,'Faqat o‘zingizning e’loningizni boshqarishingiz mumkin.');}elseif(!($this->user&&($this->user['role']!=='user'||(int)$x['user_id']===(int)$this->user['id']))&&effective_status($x)!=='active')throw new HttpError(403,'Bu e’lon hozir ochiq emas.');return $x;}
 protected function view(string $view,array $data=[]):void{extract($data,EXTR_SKIP);$user=$this->user;$title=$data['title']??'Yaqin — e’lonlar va xizmatlar';ob_start();require dirname(__DIR__).'/Views/'.$view.'.php';$content=ob_get_clean();require dirname(__DIR__).'/Views/layout.php';}
}
