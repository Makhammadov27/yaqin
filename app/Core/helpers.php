<?php
declare(strict_types=1);
function e(mixed $s):string{return htmlspecialchars((string)($s??''),ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function url(string $route='listings',array $args=[]):string{return 'index.php?'.http_build_query(['route'=>$route]+$args);}
function csrf():string {return '<input type="hidden" name="csrf" value="'.e($_SESSION['csrf']).'">';}
function redirect(string $route='listings',array $args=[]):never{header('Location: '.url($route,$args));exit;}
function flash(string $message):void{$_SESSION['flash']=$message;}
function money(mixed $p):string{return (float)$p===0.0?'Kelishiladi':number_format((float)$p,0,'.',' ').' so‘m';}
function status_label(string $s):string{return ['active'=>'Faol','expired'=>'Muddati tugagan','blocked'=>'Bloklangan','archived'=>'Arxivlangan','open'=>'Ko‘rib chiqilmoqda','approved'=>'Tasdiqlangan','rejected'=>'Rad etilgan'][$s]??$s;}
function effective_status(array $x):string{return $x['status']==='active'&&strtotime($x['expires_at'])<time()?'expired':$x['status'];}
function icon(string $n):string{$p=['search'=>'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>','plus'=>'<path d="M12 4v16M4 12h16"/>','pin'=>'<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2"/>','arrow'=>'<path d="M4 12h16m-6-6 6 6-6 6"/>','home'=>'<path d="m3 11 9-8 9 8v10h-7v-7h-4v7H3Z"/>','tool'=>'<path d="M14 6a5 5 0 0 0-6 6l-6 6 4 4 6-6a5 5 0 0 0 6-6l-3 3-4-4 3-3Z"/>','grid'=>'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>'];return '<svg viewBox="0 0 24 24" aria-hidden="true">'.($p[$n]??$p['grid']).'</svg>';}
