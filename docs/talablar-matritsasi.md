# Talablar va qabul sinovlari matritsasi

Manba: uslubiy ko‘rsatma 5.1–5.11, 7–8-bo‘limlar va A ilova 48-mavzu. Bu jadval sinov rejasi; “kutilgan natija” kuzatilgan natija degani emas. Haqiqiy natijalar `sinov-bayonnomasi.md` yoki sinov ijrochisining alohida daliliga yoziladi.

| ID | Manba | Majburiy natija | Qabul sinovi va kutilgan natija |
|---|---|---|---|
| R01 | 1.4, 5.2 | Sof PHP MVC, HTML/CSS/JS, MySQL PDO | So‘rov router → controller → model → view yo‘lidan o‘tadi; Viewda SQL yo‘q |
| R02 | 5.1, A48 | To‘rtta predmetga oid dinamik bo‘lim | E’lonlar, toifalar, shikoyatlar, tekshirish qarorlari bazadan ochiladi |
| R03 | 5.1 | Semantik va moslashuvchan sahifalar | 360/768/1280 pxda asosiy amallar; maydon nomlari, alt, klaviatura ishlaydi |
| R04 | 5.1 | Kamida uch JS imkoniyat | Forma validatsiyasi, interaktiv qidiruv/filtr, muddat yoki holatga oid yangilash ko‘rsatiladi |
| R05 | 5.3 | Kamida uch bog‘langan predmet jadvali | categories → listings → complaints va qarorlar FK bilan bog‘langan; user/fayl/aloqa bu hisobga kirmaydi |
| R06 | 5.3 | ER, ma’lumotlar lug‘ati, PK/FK/UNIQUE/indeks, utf8mb4 | Yetim FK va takroriy UNIQUE rad etiladi, o‘zbekcha matn buzilmaydi |
| R07 | 5.3 | SQL tuzilma va seed, 20/5/5 yozuv | Yangi bazaga import: listings ≥20, categories ≥5, complaints ≥5 |
| R08 | 5.4 | Ikki predmet obyektida to‘liq CRUD | E’lon va toifani yaratish/ro‘yxat/tafsilot/tahrirlash/o‘chirish yoki asoslangan arxivlash |
| R09 | 5.4 | O‘chirish tasdig‘i, bog‘liqlik nazorati | Tasdiqsiz yo‘qotish yo‘q; bog‘liq toifani o‘chirish tushunarli rad etiladi |
| R10 | 5.4 | Qidiruv, ikki filtr, whitelist saralash, sahifalash | Matn+toifa+hudud birga ishlaydi; noma’lum sort SQLni o‘zgartirmaydi; bo‘sh natija xabari bor |
| R11 | 5.5 | Uchta autentifikatsiyalangan rol | admin, moderator, user hisoblarida kirish; mehmon rol soniga kirmaydi |
| R12 | 5.5–5.6 | Hisob, kirish/chiqish, parol xeshi, sessiya | To‘g‘ri/noto‘g‘ri parol, kirishda ID almashishi, chiqishdan keyin yopiq sahifa rad etilishi |
| R13 | 5.5 | Serverda rol va egalik | User to‘g‘ridan-to‘g‘ri admin POST yoki begona listing/file ID yuborsa o‘zgarish/oshkor bo‘lish yo‘q |
| R14 | 5.6 | Mustaqil server validatsiyasi | JSsiz bo‘sh maydon, manfiy narx, noto‘g‘ri sana/toifa saqlanmaydi |
| R15 | 5.6 | PDO parametrlar, XSS kodlash, CSRF | SQLga o‘xshash matn so‘rovni buzmaydi; script matn bo‘lib chiqadi; tokensiz POST rad etiladi |
| R16 | 5.6 | Xavfsiz cookie, urinish limiti, maxfiy sozlama/log | Cookie atributlari; takroriy noto‘g‘ri kirish cheklanishi; xatoda parol/token ko‘rsatilmasligi |
| R17 | 5.7 | Rasm/PDF/video yuklash va qidirish | JPG/PNG/WEBP 2 MB, PDF 5 MB, MP4 20 MB; nom/tavsif bo‘yicha qidirish |
| R18 | 5.7 | Fayl almashtirish/o‘chirish va himoya | Soxta MIME/kengaytma/ortiqcha hajm/bajariluvchi fayl rad; begona fayl rad; disk/baza izchil |
| R19 | 5.8 | Aloqa bazaga va SMTP qutiga | Ism/email/xabar saqlanadi; qabul qiluvchi sozlamadan; test qutida real qabul dalili |
| R20 | 5.8 | SMTP xatosida xabar saqlanishi | SMTP to‘xtatiladi, xabar bazada qoladi va jo‘natish xatosi qayd etiladi |
| R21 | 5.9 | Ruxsatli filtrlangan UTF-8 CSV | Barcha filtrlangan sahifalar eksportda; tartib mos; murakkab matn to‘g‘ri; formula satri xavfsiz |
| R22 | A48, 5.10 | E’lon muddatini tugatish/uzaytirish | Muddati o‘tgan e’lon ommaviy katalogdan chiqadi; egasi ruxsatli holatda uzaytira oladi |
| R23 | A48, 5.10 | Moderator qarori va tarixi | Shikoyat → qaror → e’lon holati tranzaksiyada; takroriy qaror rad etiladi |
| R24 | 5.2 | 404 va xavfsiz HTTP metodlar | Noma’lum route 404; GET bilan yaratish/tahrirlash/o‘chirish bajarilmaydi |
| R25 | 5.11 | public ildizi va noindex | config/storage/SQL webdan ochilmaydi; kabinet indekslanmaydi; ommaviy title/meta bor |
| R26 | 5.11 | Tarmoqdan ishlash va restore | Ikkinchi qurilmadan asosiy amal dalili; yangi bazaga backupdan restore natijasi |
| R27 | 8 | Topshirish to‘plami va hisobot | Kod, schema.sql, seed.sql, namunaviy rasm/PDF/MP4, yo‘riqnoma, hisobot, dalillar |
| R28 | 8 | Mustaqil himoya | Talaba kod yo‘lini tushuntiradi va kichik o‘zgartirishni o‘zi bajaradi |

## Natijani qayd etish qoidasi

Har bir sinovda boshlang‘ich holat, amal, kutilgan natija, kuzatilgan natija va dalil alohida bo‘ladi. “Kod yozilgan”, “lint o‘tdi”, “HTTP amali tekshirildi”, “boshqa qurilmada ishladi” turli darajadagi dalillar; birini ikkinchisining o‘rniga ko‘rsatish mumkin emas.


## 2026-10-31 dalillar holati

| Talablar | Kuzatilgan dalil | Chegara |
|---|---|---|
| R01, R05–R18, R21–R24 | Mustaqil HTTP regressiya 66/66; `tests/results.json`, batafsil `QA.md` | Matritsaning har bir kichik bandi alohida stress sinovi bilan isbotlangan degani emas |
| R03 | Koordinator 360/768/1280 px, yon siljish nazorati, Tab va Enter kirishi; `mobile.png`, `desktop.png` | Barcha foydalanuvchi ssenariylari bo‘yicha to‘liq accessibility auditi emas |
| R07 | Yakuniy namuna 24 listing, 6 category, 7 complaint, 6 decision, 4 user; `tests/cleanup-result.json` | Oracle MySQL 8da alohida import tekshirilmagan; ishlatilgan server MariaDB 10.11.16 |
| R19 | `tests/smtp-received.eml` mahalliy SMTP qabul dalili | Global pochta, autentifikatsiya va TLS tekshirilmagan |
| R20 | `tests/smtp_failure_result.json`: HTTP 200, failed va xabar saqlangan | Ataylab to‘xtatilgan mahalliy SMTP ssenariysi |
| R26: SQL restore | `database/backup.sql` yangi `yaqin_course_restore_20261031` bazasiga import; `evidence/restore-check.json` barcha 8 jadval satrlari teng | Restore vaqti attachments jadvali bo‘sh; yuklangan fayllarni to‘liq tiklash dalili emas |
| R26: boshqa qurilma | **Kutilmoqda** | Haqiqiy ikkinchi qurilmadan asosiy amal ko‘rsatilmagan; global PHP hosting ham tasdiqlanmagan |
| R27 | Kod, SQLlar, README, mazkur docs va QA dalillari mavjud | Talaba FISH/guruh va yakuniy topshirish arxivi nomini o‘zi to‘ldiradi |
| R28 | **Talabaning himoyasida bajariladi** | Dastur va hisobot mavjudligi mustaqil tushuntirish yoki bahoni kafolatlamaydi |

R04dagi uchta JavaScript imkoniyat va R25dagi ommaviy/noindex siyosatning to‘liq qamrovi kod va tegishli sinov bilan tekshiriladi; yuqoridagi umumiy HTTP natijasi ushbu barcha mayda bandlarga avtomatik “to‘liq bajarilgan” maqomini bermaydi.

Koordinatorning alohida baza sinovida UNIQUE takrori va mavjud bo‘lmagan tashqi kalit rad etildi: `docs/evidence/constraints.json` (R06).
