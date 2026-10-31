# Mustaqil ish hisoboti

**Fan:** Web dasturlashga kirish  
**Mavzu:** 48. Elektron e’lonlar va xizmatlar katalogi  
**Loyiha:** Yaqin  
**Talaba va guruh:** topshirishdan oldin talaba o‘z ma’lumotlarini kiritadi  
**Hujjat holati:** texnik hisobot; amaliy dalillar alohida QA bayonnomasida

## 1. Predmet sohasi

Loyiha buyum yoki xizmat haqidagi e’lonni toifalash, kerakli e’lonni izlash, muddatini boshqarish va shikoyat bo‘yicha qaror qabul qilish jarayonlarini qamrab oladi. Ommaviy katalog va vakolatli boshqaruv bir tizimda ishlaydi. Namuna shaxsiy ma’lumotlar ishlatiladi.

## 2. Talablar va tanlangan yechim

To‘rtta predmet bo‘limi — e’lonlar, toifalar, shikoyatlar, tekshirish qarorlari. Sof PHP MVC tanlangan, chunki topshiriq tayyor framework va CMSni ruxsat etmaydi. MySQLga PDO orqali ulanish ma’lumot va SQL tuzilmasini ajratishga yordam beradi. HTML serverda chiqariladi; CSS moslashuvchan ko‘rinish, JavaScript interaktiv qulayliklarni beradi. Batafsil qabul shartlari `talablar-matritsasi.md` da.

## 3. MVC va so‘rov oqimi

Yagona kirish nuqtasi `public/index.php`. `?route=...` yo‘naltiruvchi so‘rovga mos kontroller amalini tanlaydi. Kontroller sessiya, rol, yozuv egaligi, CSRF va qiymatlarni tekshiradi; model bazani va predmet qoidasini boshqaradi; View HTML chiqaradi.

Misol: e’lonni saqlash POST so‘rovi keladi → foydalanuvchi aniqlanadi → CSRF tekshiriladi → sarlavha, toifa va narx tekshiriladi → model PDO parametrli so‘rovini bajaradi → muvaffaqiyatli natijadan keyin ro‘yxat yoki tafsilotga yo‘naltiriladi. Foydalanuvchi begona yozuv ID sini yuborsa, modelni o‘zgartirishdan oldin egalik nazorati uni rad etishi kerak.

## 4. Baza

Asosiy jadvallar categories, listings, complaints va moderation_decisions. users, attachments, contact_messages va auth_attempts yordamchi vazifalarni bajaradi. Bog‘lanishlar FK bilan mustahkamlangan. Takroriy toifa nomi va hisob emaili UNIQUE, bitta shikoyatning yakuniy qarori esa complaint_id UNIQUE orqali cheklangan. ER va ustunlar lug‘ati `malumotlar-modeli.md` da.

E’lon arxivlanadi, chunki unga bog‘langan shikoyat va tekshirish tarixini saqlash kerak. Bog‘langan e’loni bor toifa o‘chirishda rad etiladi. Seed yozuvlari dastur namoyishi uchun mo‘ljallangan; ularning soni va import natijasi sinovda alohida hisoblanadi.

## 5. Vakolatlar va xavfsizlik

Tizimga kiradigan rollar admin, moderator va user. Moderator shikoyatlarni tekshiradi, biroq begona e’lonning egasi sifatida tahrirlash vakolatiga ega emas. Administrator hisoblar va rollarni boshqaradi. User o‘z e’lonlari hamda shikoyatlariga tegishli ruxsatlardan foydalanadi.

Autentifikatsiya parol va sessiya bilan, avtorizatsiya esa serverda rol/egalik tekshiruvlari bilan bajariladi. PDO parametrli so‘rov, HTML kodlash, CSRF token, cookie atributlari, urinish limiti va maxfiy sozlamalarni public katalogidan tashqarida tutish bir-birini to‘ldiradi. Hech biri boshqa himoyaning o‘rnini bosmaydi.

## 6. Muddat va moderatsiya

E’lon `active`, `expired`, `blocked` yoki `archived` holatga ega. Muddati o‘tgan e’lon ommaviy ro‘yxatda ko‘rinmaydi. Egasi ruxsat etilgan holatdagina muddatni uzaytira oladi; bloklashni oddiy uzaytirish bilan bekor qilmasligi kerak.

Shikoyat `open` holatdan `approved` yoki `rejected` holatga o‘tadi. Moderator qarorining muallifi, asosi va vaqti yoziladi. Qaror, shikoyat va zarur e’lon holati bitta tranzaksiyada yangilanadi. Takroriy yoki bir vaqtda kelgan qarorlar predmet qoidalarini buzmasligi shart. Ushbu to‘g‘ri va taqiqlangan ssenariylar himoyada amalda ko‘rsatiladi.

## 7. Fayllar, aloqa va eksport

Biriktirmalar e’longa va yuklagan foydalanuvchiga bog‘lanadi. Rasm, PDF va MP4 uchun server MIME, kengaytma va hajmni tekshiradi. Saqlash nomi tasodifiy; asl nom faqat metama’lumot. Himoyalangan fayl yuklash huquqi serverda nazorat qilinadi.

Aloqa xabari bazada saqlanib, sozlangan SMTP qutiga yuboriladi. `sent` holati yoki funksiyaning javobi yetkazilganlikning mustaqil isboti emas: test pochta qutisidagi qabul dalili zarur. SMTP ishlamasa xabar bazada qolishi tekshiriladi.

CSV eksport joriy qidiruv, ikki filtr va saralashga mos barcha ruxsatli yozuvlarni chiqaradi. Faqat ekrandagi bitta sahifa eksport qilinmaydi. UTF-8, qo‘shtirnoq, satr uzilishi va formulaga o‘xshash matnlar xavfsiz chiqarilishi sinovdan o‘tkaziladi.

## 8. Sinov va foydalanish muhiti

Muhit: XAMPP PHP 8.3.36 va MySQL bilan mos MariaDB 10.11.16. Ushbu versiyalar koordinator tomonidan aniqlangan. Aniq funksiyalar va xavfsizlik bo‘yicha kuzatilgan natijalar `QA.md` da yuritiladi. 2026-10-31 yakuniy mustaqil HTTP regressiyada 66/66 sinov muvaffaqiyatli o‘tdi (`tests/results.json`). So‘rovlar JavaScriptsiz yuborilib server nazoratlari alohida tekshirildi. Ushbu qamrov umumiy xavfsizlik kafolati yoki yuklama sinovi emas.

Mahalliy SMTP test qutisida xabar haqiqatan qabul qilingan (`tests/smtp-received.eml`). SMTP ishlamagan alohida sinovda HTTP 200 javobi, bazada failed holati va xabarning saqlangani kuzatildi (`tests/smtp_failure_result.json`). Tashqi pochta xizmatiga xabar yuborilmadi.

Koordinator `database/backup.sql`ni yangi `yaqin_course_restore_20261031` bazasiga tikladi; sakkiz jadvaldagi dekodlangan satrlar manba baza bilan bir xil (`docs/evidence/restore-check.json`). Tekshiruvdan so‘ng baza 24 e’lon, 6 toifa, 7 shikoyat, 6 qaror va 4 hisobdan iborat. Fayl upload/replace/delete sinovlari alohida bajarilgan; tiklash paytida attachments jadvali bo‘sh bo‘lgan, shu sababli bu restore dalili yuklangan fayllarni to‘liq tiklashni isbotlamaydi.

Brauzerda 360, 768 va 1280 px sahifalar tekshirildi; sahifa darajasida yon tomonga chiqish kuzatilmadi. Kirish formasida Tab bilan emaildan parolga o‘tish va Enter orqali kirish bajarildi. Tasvirlar `docs/mobile.png` va `docs/desktop.png`. Oracle MySQL 8 hamda haqiqiy ikkinchi qurilma alohida tekshirilmagan.

Oldingi Sites havolasida statik namuna joylashtirilgan edi. Ushbu PHP dasturini u yerda PHP serveri sifatida ishga tushirish mumkin emas. Yangi loyiha PHP va MySQL muhitida ishga tushiriladi; tarmoqdan ikkinchi qurilma dalili va haqiqiy PHP hosting dalili bo‘lmasa “global joylashtirildi” deyilmaydi.

## 9. Topshirish va cheklovlar

To‘plamga dastur kodi, schema.sql, seed.sql, namunaviy rasm/PDF/MP4, ishga tushirish yo‘riqnomasi, mazkur hisobot, ER, talablar matritsasi va haqiqiy sinov dalillari kiritiladi. Talaba FISH/guruhini to‘ldirib arxivni `Guruh_FISH_Mavzu48.zip` shaklida nomlaydi.

Mahalliy SMTP va SQL zaxiradan tiklash dalillari yuqorida qayd etildi. Haqiqiy ikkinchi qurilmadan tarmoq namoyishi va global PHP hosting hali tasdiqlanmagan. Kodning mavjudligi yoki sintaksis tekshiruvi ikkinchi qurilmadan foydalanishni isbotlamaydi. Talaba loyihani mustaqil tushuntirishi va himoyada kichik o‘zgartirishni bajarishi lozim.
