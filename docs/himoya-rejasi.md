# 15 daqiqalik himoya rejasi

## Oldindan tayyorlash

README bo‘yicha baza va serverni ishga tushiring. Uch rol hisoblarini tekshiring. Namuna rasm, PDF va MP4ni tayyorlang. QA dalillari, filtrlangan CSV, SMTP qutisidagi xabar hamda tiklash dalilini ochishga tayyor tuting. Faqat amalda olingan natijani namoyish qiling.

## 0–2 daqiqa: muammo va tuzilma

Katalog maqsadini, to‘rtta dinamik bo‘limni va asosiy jarayonni ayting. ER diagrammada categories → listings → complaints → moderation_decisions bog‘lanishini ko‘rsating. Bosh sahifa va login alohida predmet bo‘limlari hisoblanmasligini tushuntiring.

## 2–8 daqiqa: amaliy namoyish

1. User sifatida e’lon yarating, tafsilotni ko‘ring, tahrirlang; narx yoki sarlavha natijasini ko‘rsating.
2. Toifa CRUDini administrator sifatida bajaring; bog‘langan toifani o‘chirish nega rad etilishini ko‘rsating.
3. Matn + toifa + hudud filtri, narx bo‘yicha saralash, sahifalash va filtrlangan CSVni oching.
4. E’lon muddatini tugating va uzaytiring. Bloklangan yozuvni oddiy user uzaytira olmasligini ko‘rsating.
5. Ikkinchi user bilan shikoyat yuboring, moderator bilan qaror kiriting. Qaror tarixini va takroriy qarorning rad etilishini ko‘rsating.
6. Ruxsatli fayl va noto‘g‘ri fayl yuklashni, fayl almashtirish/o‘chirishni ko‘rsating.
7. Aloqa xabari bazada va SMTP test qutisida ekanini ko‘rsating. SMTP xatosidagi bazada saqlanish dalili bo‘lsa uni oching.

## 8–12 daqiqa: kod va xavfsizlik

Bir POST so‘rovining `public/index.php` → kontroller → model → View yo‘lini o‘z kodingizdan tushuntiring. GET va POST farqini, PDO parametri bilan sort whitelist farqini ayting. `password_hash`, `password_verify`, sessiya yangilash, CSRF va `htmlspecialchars` vazifalarini ko‘rsating.

Begona ID bilan kirish rad etilishini namoyish qiling. “Tugma yashirilgan” server vakolat nazorati o‘rnini bosmasligini tushuntiring. Tranzaksiyadagi xatoda barcha o‘zgarishlar nega rollback bo‘lishini izohlang. Faylni faqat kengaytma bilan tekshirish nega yetarli emasligini ayting.

## 12–15 daqiqa: mustaqil kichik o‘zgartirish

O‘qituvchi topshirig‘iga qarab yangi filtr, maydon validatsiyasi yoki chiqarish uslubini o‘zgartiring. O‘zgartirishdan so‘ng bitta to‘g‘ri va bitta noto‘g‘ri holatni tekshiring. Tayyor kodni o‘qib berish bilan cheklanmang.

## Baholashni to‘g‘ri talqin qilish

Ko‘rsatma yakuniy 10 ballni nazariy 6 va amaliy 4 ballga ajratadi. Ishlaydigan dastur nazariy bilim uchun avtomatik ball bermaydi. Talaba tushunmagan imkoniyatni o‘ziniki sifatida asoslamasligi, tekshirilmagan natijani “ishlaydi” deb ko‘rsatmasligi kerak.
