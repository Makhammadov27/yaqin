# Yaqin — PHP MVC va MySQL

“Web dasturlashga kirish” uslubiy ko‘rsatmasi, 48-mavzu uchun o‘quv loyiha. Dinamik bo‘limlar: e’lonlar, toifalar, shikoyatlar, tekshirish qarorlari. Sof PHP, HTML, CSS, JavaScript va PDO ishlatiladi.

## Muhit va sozlash

XAMPP PHP 8.3.36 va MariaDB 10.11.16 aniqlangan. MariaDB MySQL bilan mos server; aynan Oracle MySQL talab qilinsa MySQL 8 muhitida import va sinov qayta bajariladi. PHP kengaytmalari: PDO, pdo_mysql, mbstring, fileinfo, session. `storage` PHP uchun yoziladigan bo‘lsin.

`config/config.php` muhit o‘zgaruvchilarini o‘qiydi. `.env` avtomatik o‘qiladi deb taxmin qilmang.

| O‘zgaruvchi | Lokal standart |
|---|---|
| DB_HOST / DB_PORT | 127.0.0.1 / 3306 |
| DB_NAME | yaqin_course |
| DB_USER / DB_PASS | root / bo‘sh |
| SMTP_HOST / SMTP_PORT | 127.0.0.1 / 1025 |
| SMTP_FROM | noreply@yaqin.test |
| SMTP_TO | admin@yaqin.test |

Bo‘sh root paroli faqat lokal o‘quv muhiti uchun. Hostingda cheklangan baza foydalanuvchisi va maxfiy muhit qiymatlarini ishlating. Maxfiy qiymatlarni kod yoki topshirish arxiviga yozmang.

## Ishga tushirish

XAMPP Control Paneldan MySQLni yoqing. Loyiha papkasida PowerShell ochib o‘rnatuvchini bajaring:

```powershell
& 'C:\xampp\php\php.exe' bin/install.php
```

O‘rnatuvchi bazani va tuzilmani yaratadi; `users` bo‘sh bo‘lsagina namunaviy yozuvlarni kiritadi. Ushbu o‘rnatuvchi mavjud lokal muhitda muvaffaqiyatli bajarildi. Mavjud jadval ustunlarini o‘zgartiradigan migratsiya vositasi emas.

Qo‘lda import qilish muqobili uchun SQL mijozga kiring:

```powershell
& 'C:\xampp\mysql\bin\mysql.exe' -h 127.0.0.1 -P 3306 -u root
```

Yangi bazani yarating va SQLlarni tartib bilan import qiling. Mavjud ma’lumotli bazaga seedni ko‘r-ko‘rona qayta import qilmang.

```sql
CREATE DATABASE IF NOT EXISTS yaqin_course CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE yaqin_course;
SOURCE database/schema.sql;
SOURCE database/seed.sql;
```

Loyiha tarkibidagi `start.ps1` lokal serverni 127.0.0.1:4180da ishga tushiradi; `-Lan` parametri 0.0.0.0ga bog‘laydi. Muqobil ravishda alohida PowerShell oynasida server:

```powershell
& 'C:\xampp\php\php.exe' -d upload_max_filesize=20M -d post_max_size=25M -S 127.0.0.1:4180 -t public
```

Brauzer: **http://127.0.0.1:4180/**. Apache uchun DocumentRoot aynan `public` bo‘lsin. Loyiha ildizi, config, storage va SQL fayllari ommaviy web ildizida bo‘lmasin.

## Namuna hisoblari

| Rol | Email | Parol |
|---|---|---|
| Administrator | admin@yaqin.test | Admin123! |
| Moderator | moderator@yaqin.test | Moderator123! |
| Foydalanuvchi | user@yaqin.test | User123! |
| Ikkinchi foydalanuvchi | user2@yaqin.test | User123! |

Bular ochiq o‘quv hisoblari. Umumiy foydalanishdan oldin almashtiring.

## Marshrutlar

URL misoli `?route=listing&id=1`: id alohida query parametridir.

| Vazifa | route |
|---|---|
| Katalog, tafsilot, forma | listings; listing; listing-form |
| E’lon o‘zgartirish (POST) | listing-save; listing-delete; listing-extend; listing-expire |
| Toifalar | categories; category; category-form |
| Toifa o‘zgartirish (POST) | category-save; category-delete |
| Shikoyatlar va qarorlar | complaints; decisions |
| Shikoyat/qaror (POST) | complaint-create; complaint-decide |
| Hisob | login; register; logout |
| Fayllar | files; file-download; file-upload; file-delete |
| Aloqa, rollar, eksport | contact; users; user-role; export |

Aniq maydonlarni tegishli HTML formadan oling. O‘zgartiruvchi amallar POST va CSRF token talab qiladi. Noma’lum marshrut 404, vakolat yetishmasa rad javobi beriladi.

## Jarayon va ruxsatlar

E’lon o‘chirish bilan arxivlanadi: shikoyat va qaror tarixi saqlanadi. Bog‘liq e’loni bor toifa o‘chirilmaydi. Moderator boshqa foydalanuvchining e’lonini egasi sifatida tahrirlay olmaydi, lekin shikoyat bo‘yicha qaror chiqaradi. User eksporti faqat o‘z yozuvlari. Fayllar egasi, moderator va administrator uchun himoyalangan.

Uzaytirish bir amalda 30 kun, hozirdan ko‘pi bilan 180 kun. Bloklangan/arxivlangan yozuv uzaytirish bilan faollashmaydi. Bir shikoyatga bitta yakuniy qaror; moderator o‘zi yuborgan yoki o‘z e’loniga oid shikoyatni hal qila olmaydi.

## SMTP va tekshiruv

Loyiha papkasida `python tools/smtp-test.py` bilan test SMTP qutisini 127.0.0.1:1025da ishga tushiring. Python standart kutubxonalari yetarli; qabul qilingan xabarlar `storage/mailbox/*.eml`da saqlanadi. Python PATHda bo‘lmasa uning to‘liq executable yo‘lini ishlating. Aloqa xabarini bazada va test qutida tekshiring. Faqat `smtp_status=sent` yoki yuborish funksiyasi javobi qabul dalili emas. SMTP to‘xtatilganda xabar bazada qolishi kerak. Koordinatorning test vositasi mavjud bo‘lsa uning yo‘riqnomasidan foydalaning; bu hujjat o‘zi test serverini o‘rnatmaydi.

Reja `docs/talablar-matritsasi.md`da, haqiqiy kuzatilgan natijalar `docs/QA.md`da. Kod mavjudligi, lint, HTTP sinovi va ikkinchi qurilma dalili har xil tekshiruvlardir.

2026-10-31 holatida bajarilgan dalillar:

- Mustaqil HTTP regressiya: **66/66** muvaffaqiyatli (mahalliy QA natijalari).
- SMTP qutida haqiqiy mahalliy qabul: mahalliy SMTP sinovi; server ishlamaganida ham xabar saqlangan (alohida mahalliy SMTP ishlamay qolish sinovi).
- mahalliy backup nusxasi yangi `yaqin_course_restore_20261031` bazasiga tiklandi; sakkiz jadvalning dekodlangan satrlari bir xil (`docs/evidence/restore-check.json`).
- Brauzerda 360/768/1280 px, asosiy sahifalarda yon tomonga chiqish yo‘q; Tab bilan emaildan parolga va Enter bilan kirish bajarildi. Tasvirlar: `docs/mobile.png`, `docs/desktop.png`.
- QA yozuvlari tozalangach: 24 e’lon, 6 toifa, 7 shikoyat, 6 qaror, 4 hisob (`tests/cleanup-result.json`).

Bu natijalar Oracle MySQL 8, haqiqiy ikkinchi qurilma, global PHP hosting, SMTP TLS yoki concurrency stress sinovi o‘rnini bosmaydi.

## Zaxira va tarmoq

`mysqldump` bilan baza zaxirasini va shu vaqtdagi `storage/uploads` nusxasini saqlang. Yangi sinov bazasiga import qilib yozuvlar va bog‘lanishlarni solishtiring. Restore sinovi uchun asosiy bazani o‘chirmang.

Lokal tarmoq namoyishi uchun serverni `0.0.0.0:4180`ga bog‘lab faqat ishonchli LANdan kirishni cheklash mumkin. Boshqa qurilmada serverning LAN IP manzilidan ochib asosiy amalni bajaring. Firewall sozlamasi muhitga bog‘liq. Ushbu yo‘riqnoma yozilgani ikkinchi qurilma sinovi bajarilganini anglatmaydi. Global joylashtirishga PHP/MySQL hosting va HTTPS kerak.

Oldingi `yaqin-elonlar-uzkua...chatgpt.site` statik namuna ushbu PHP backend manzili emas: Sites runtime PHPni bajarmaydi.

## Topshirish

`docs/texnik-topshiriq.md`, `docs/talablar-matritsasi.md`, `docs/malumotlar-modeli.md`, `docs/hisobot.md`, `docs/himoya-rejasi.md` va mustaqil tekshiruvning `docs/QA.md` faylini ko‘ring. Talaba guruh/FISHini to‘ldirib, kod, schema.sql, seed.sql, namunaviy rasm/PDF/MP4 va haqiqiy dalillar bilan `Guruh_FISH_Mavzu48.zip` tayyorlaydi. Hisobotga tekshirilmagan natija “bajarildi” sifatida yozilmaydi.

