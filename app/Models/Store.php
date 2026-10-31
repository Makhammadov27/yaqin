<?php
declare(strict_types=1);
namespace App\Models;
use App\Core\Database;
use App\Core\HttpError;
use PDO;
final class Store {
 public PDO $db;
 public function __construct(){$this->db=Database::connection();}
 public function run(string $sql,array $values=[]):\PDOStatement{$q=$this->db->prepare($sql);$q->execute($values);return $q;}
 public function find(string $table,int $id):?array{if(!in_array($table,['users','categories','complaints','attachments'],true))throw new \LogicException('Invalid table');return $this->run("SELECT * FROM $table WHERE id=?",[$id])->fetch()?:null;}
 public function categories():array{return $this->run('SELECT c.*,COUNT(l.id) listing_count FROM categories c LEFT JOIN listings l ON l.category_id=c.id AND l.status="active" AND l.expires_at>NOW() GROUP BY c.id ORDER BY c.name')->fetchAll();}
 public function listing(int $id):?array{return $this->run('SELECT l.*,c.name category_name,u.name owner_name FROM listings l JOIN categories c ON c.id=l.category_id JOIN users u ON u.id=l.user_id WHERE l.id=?',[$id])->fetch()?:null;}
 public function filter(array $input,?array $user,bool $export=false):array{
 $where=[];$params=[];
 if($export&&$user&&$user['role']==='user'){$where[]='l.user_id=?';$params[]=$user['id'];}
 elseif(!$user){$where[]='l.status="active" AND l.expires_at>NOW()';}
 elseif($user['role']==='user'){$where[]='((l.status="active" AND l.expires_at>NOW()) OR l.user_id=?)';$params[]=$user['id'];}
 if(($input['mine']??'')==='1'&&$user){$where[]='l.user_id=?';$params[]=$user['id'];}
 $q=mb_substr(trim(is_string($input['q']??null)?$input['q']:''),0,120);if($q!==''){$where[]='(l.title LIKE ? OR l.description LIKE ?)';$params[]='%'.$q.'%';$params[]='%'.$q.'%';}
 if(filter_var($input['category']??null,FILTER_VALIDATE_INT,['options'=>['min_range'=>1]])){$where[]='l.category_id=?';$params[]=(int)$input['category'];}
 if(is_string($input['city']??null)&&$input['city']!==''){$where[]='l.city=?';$params[]=mb_substr($input['city'],0,80);}
 $state=$input['status']??'';if(in_array($state,['active','expired','blocked','archived'],true)){if($state==='expired')$where[]='(l.status="expired" OR (l.status="active" AND l.expires_at<=NOW()))';elseif($state==='active')$where[]='(l.status="active" AND l.expires_at>NOW())';else{$where[]='l.status=?';$params[]=$state;}}else{$where[]='l.status<>"archived"';}
 $sortKey=is_string($input['sort']??null)?$input['sort']:'new';$sort=['new'=>'l.id DESC','low'=>'l.price ASC,l.id DESC','high'=>'l.price DESC,l.id DESC','expiry'=>'l.expires_at ASC,l.id DESC'][$sortKey]??'l.id DESC';
 return [implode(' AND ',$where)?:'1=1',$params,$sort];
 }
 public function listings(array $input,?array $user,bool $export=false):array{[$where,$params,$sort]=$this->filter($input,$user,$export);$count=(int)$this->run("SELECT COUNT(*) FROM listings l WHERE $where",$params)->fetchColumn();$page=max(1,min((int)($input['page']??1),max(1,(int)ceil($count/8))));$sql='SELECT l.*,c.name category_name,u.name owner_name,(SELECT a.id FROM attachments a WHERE a.listing_id=l.id AND a.mime LIKE "image/%" ORDER BY a.id LIMIT 1) image_id FROM listings l JOIN categories c ON c.id=l.category_id JOIN users u ON u.id=l.user_id WHERE '.$where.' ORDER BY '.$sort;if(!$export)$sql.=' LIMIT 8 OFFSET '.(($page-1)*8);return ['items'=>$this->run($sql,$params)->fetchAll(),'total'=>$count,'page'=>$page,'pages'=>max(1,(int)ceil($count/8))];}
 public function complaints(array $user):array{$where=$user['role']==='user'?' WHERE c.user_id=? OR l.user_id=?':'';$p=$user['role']==='user'?[$user['id'],$user['id']]:[];return $this->run('SELECT c.*,l.title,u.name author,d.outcome,d.note,d.created_at decision_at,m.name moderator FROM complaints c JOIN listings l ON l.id=c.listing_id JOIN users u ON u.id=c.user_id LEFT JOIN moderation_decisions d ON d.complaint_id=c.id LEFT JOIN users m ON m.id=d.moderator_id'.$where.' ORDER BY c.id DESC',$p)->fetchAll();}
 public function decisions(array $user):array{$w=$user['role']==='user'?' WHERE c.user_id=? OR l.user_id=?':'';$p=$user['role']==='user'?[$user['id'],$user['id']]:[];return $this->run('SELECT d.*,c.listing_id,l.title,m.name moderator FROM moderation_decisions d JOIN complaints c ON c.id=d.complaint_id JOIN listings l ON l.id=c.listing_id JOIN users m ON m.id=d.moderator_id'.$w.' ORDER BY d.id DESC',$p)->fetchAll();}
 public function decide(int $id,array $user,string $outcome,string $note):void{
 $this->db->beginTransaction();try{$c=$this->run('SELECT * FROM complaints WHERE id=? FOR UPDATE',[$id])->fetch();if(!$c)throw new HttpError(404,'Shikoyat topilmadi.');$l=$this->run('SELECT * FROM listings WHERE id=? FOR UPDATE',[$c['listing_id']])->fetch();if($c['status']!=='open')throw new HttpError(409,'Bu shikoyat bo‘yicha qaror allaqachon chiqarilgan.');if((int)$c['user_id']===(int)$user['id']||(int)$l['user_id']===(int)$user['id'])throw new HttpError(403,'O‘zingizga tegishli shikoyatni ko‘rib chiqa olmaysiz.');$this->run('INSERT INTO moderation_decisions(complaint_id,moderator_id,outcome,note) VALUES(?,?,?,?)',[$id,$user['id'],$outcome,$note]);$this->run('UPDATE complaints SET status=? WHERE id=?',[$outcome,$id]);if($outcome==='approved'&&$l['status']!=='archived')$this->run('UPDATE listings SET status="blocked" WHERE id=?',[$l['id']]);$this->db->commit();}catch(\Throwable $e){$this->db->rollBack();throw $e;}
 }
 public function lifecycle(int $id,array $u,string $action,string $expected):void{
 $this->db->beginTransaction();try{$x=$this->run('SELECT * FROM listings WHERE id=? FOR UPDATE',[$id])->fetch();if(!$x)throw new HttpError(404,'E’lon topilmadi.');if($u['role']!=='admin'&&(int)$x['user_id']!==(int)$u['id'])throw new HttpError(403,'Egalik huquqi yo‘q.');
 if(!hash_equals($x['expires_at'],$expected))throw new HttpError(409,'E’lon o‘zgargan yoki so‘rov takrorlangan. Sahifani yangilang.');
 if(in_array($x['status'],['blocked','archived'],true))throw new HttpError(409,'Bloklangan yoki arxivlangan e’lon muddati o‘zgarmaydi.');
 if($action==='extend'){$expiry=new \DateTimeImmutable($x['expires_at']);$now=new \DateTimeImmutable();$new=($expiry>$now?$expiry:$now)->modify('+30 days');if($new>$now->modify('+180 days'))throw new HttpError(409,'E’lonni 180 kundan ortiq oldinga uzaytirib bo‘lmaydi.');$this->run('UPDATE listings SET expires_at=?,status="active" WHERE id=?',[$new->format('Y-m-d H:i:s'),$id]);}else{if(effective_status($x)!=='active')throw new HttpError(409,'Faqat faol e’lonni tugatish mumkin.');$this->run('UPDATE listings SET status="expired",expires_at=NOW() WHERE id=?',[$id]);}$this->db->commit();}catch(\Throwable $e){$this->db->rollBack();throw $e;}}
 public function privateListing(int $id,array $u):array{$l=$this->listing($id);if(!$l)throw new HttpError(404,'E’lon topilmadi.');if($u['role']==='user'&&(int)$l['user_id']!==(int)$u['id'])throw new HttpError(403,'Fayl faqat egasi va moderatorlar uchun.');return $l;}
}
