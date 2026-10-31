<?php
declare(strict_types=1);
return ['db'=>['host'=>getenv('DB_HOST')?:'127.0.0.1','port'=>getenv('DB_PORT')?:'3306','name'=>getenv('DB_NAME')?:'yaqin_course','user'=>getenv('DB_USER')?:'root','pass'=>getenv('DB_PASS')?:''], 'smtp'=>['host'=>getenv('SMTP_HOST')?:'127.0.0.1','port'=>(int)(getenv('SMTP_PORT')?:1025),'from'=>getenv('SMTP_FROM')?:'noreply@yaqin.test','to'=>getenv('SMTP_TO')?:'admin@yaqin.test']];
