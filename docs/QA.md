# Mustaqil QA bayonnomasi

Vakolatli nishon: faqat ushbu loyiha, `http://127.0.0.1:4180` va `yaqin_course` o‘quv bazasi. Boshqa bazalar va tashqi pochta tizimlari tekshirilmaydi.

## Takrorlash

```powershell
& 'C:/Users/uzkua/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' tests/http_regression.py http://127.0.0.1:4180
```

Python standart kutubxonasi va `C:/xampp/mysql/bin/mysql.exe` ishlatiladi. Sinovlar `QA<vaqt>` nomli alohida yozuvlar yaratadi. Parollar demo hisoblariga tegishli. JSON natijalari `tests/results.json` ichiga yoziladi.

## Qamrov

- Uch rol bilan kirish, mehmon va foydalanuvchi uchun taqiqlangan amallar.
- CSRF tokensiz POST va holat o‘zgartiruvchi GET so‘rovlari.
- E’lon va toifa yaratish, ko‘rish, tahrirlash, arxivlash/o‘chirish.
- Begona yozuvni tahrirlash, arxivlash va faylini yuklab olishga urinish.
- E’lonni tugatish, uzaytirish, takroriy so‘rov, shikoyat va moderator qarori.
- Parametrli qidiruv, saralash, sahifalash va barcha sahifalar bo‘yicha CSV.
- HTML chiqarishda XSS kodlash va CSV formula katagini zararsizlantirish.
- PNG, haqiqiy MP4 va PDF yuklash; MIME mos kelmasligi, ortiqcha hajm, bajariluvchi faylni rad etish; almashtirish/o‘chirish.
- Aloqa ma’lumotini bazaga saqlash, mahalliy SMTPga yuborish va tezlik cheklovi.
- SMTP serveri ishlamasa ham xabarni saqlash alohida ssenariy bilan tekshiriladi.

## Hozirgi dalillar

HTTP sinovlarining bajarilishi va natijalari quyida yakuniy tekshiruvdan keyin qayd etiladi. Skript mavjudligi tekshiruv muvaffaqiyatli bajarilganini anglatmaydi.

## Bajarilgan tekshiruvlar — 2026-10-31

Yakuniy to‘liq HTTP regressiya: **66/66 muvaffaqiyatli**. Dalil: `tests/results.json`. HTTP so‘rovlar JavaScriptsiz yuborildi, shu sababli server tekshiruvlari ham alohida tekshirildi. Dastlabki sinov skriptida lifecycle so‘rovlarining yangi `expected_expires_at` maydoni yo‘q edi; skript shartnomaga moslashtirilib to‘liq qayta bajarildi. Yakuniy dalil dastlabki urinishdan alohida saqlangan.

Tekshirilgan natijalar:

| Yo‘nalish | Kuzatilgan natija |
|---|---|
| Hisoblar | Administrator, moderator, ikki oddiy foydalanuvchi kirishi200; oddiy foydalanuvchi/moderator uchun hisoblar boshqaruvi403; ro‘yxatdan o‘tishda yuborilgan admin roli qabul qilinmadi |
| So‘rov himoyasi | Tokensiz kirish403, o‘chirish GET405, begona yozuvni tahrirlash/arxivlash403; HttpOnly va SameSite=Lax cookie belgilari mavjud |
| CRUD | E’lon yaratish/ko‘rish/tahrirlash/arxivlash va toifa yaratish/ko‘rish/tahrirlash/o‘chirish bajarildi; bog‘langan toifani o‘chirish rad etildi |
| Qidiruv va eksport | SQLga o‘xshash qidiruv qiymati xatoga olib kelmadi; saralash whitelist qiymatidan tashqarisi xavfsiz boshqarildi; sahifalar farq qildi; CSV barcha ruxsat etilgan sahifalarni qamrab oldi; formula katagi apostrof bilan kodlandi |
| Mavzu48 jarayoni | E’lon tugatildi; mehmon uchun yopildi; uzaytirildi; eski snapshot bilan takroriy uzaytirish409; takroriy shikoyat409; moderator tasdig‘idan so‘ng e’lon bloklandi; takroriy qaror409; bloklangan e’lonni uzaytirish409 |
| XSS | Skriptga o‘xshash sarlavha HTML kodi sifatida bajarilmay, kodlangan matn bo‘lib chiqarildi |
| Fayllar | PNG, valid PDF va haqiqiy MP4 yuklandi; egasi/moderator yuklab oldi; boshqa foydalanuvchi403; almashtirish/o‘chirish bajarildi; PDFni PNG deb yuborish,2MBdan ortiq PNG va PHP fayli422 bilan rad etildi |
| Aloqa | Noto‘g‘ri email422, to‘g‘ri xabar saqlandi; takroriy tezkor xabar429; bazada sent qaydi va haqiqiy qabul qilingan `.eml` mavjud |
| Sessiyadan chiqish | Logoutdan so‘ng himoyalangan fayllar bo‘limi401/403 bilan rad etildi |

SMTP muvaffaqiyati faqat funksiyaning javobiga asoslanmagan: mahalliy test qutisida `QA1793455455 local test message` matni qabul qilindi (`tests/smtp-received.eml`). Tashqi pochta xizmatiga xabar yuborilmadi.

SMTP ishlamasligi alohida tekshirildi: koordinator mahalliy SMTP sinkni to‘xtatgach `tests/smtp_failure.py` bajarildi. **HTTP200, bazada failed, xabar saqlangan**. Dalil: `tests/smtp_failure_result.json`. Ushbu holatni tezlik cheklovidan ajratish uchun faqat QA yaratgan oldingi kontakt yozuvi o‘chirildi.

QA yaratgan yozuvlar va fayllar `tests/cleanup.py` orqali olib tashlandi. Qolgan namunaviy baza:24 e’lon,6 toifa,7 shikoyat,6 qaror,4 foydalanuvchi. Dalil: `tests/cleanup-result.json`. Boshqa bazalarga murojaat qilinmadi.

## Koordinator kuzatuvlari

Quyidagilar mustaqil HTTP skriptidan tashqari koordinator tomonidan bildirilgan brauzer dalillaridir:

- E’lonlar sahifasi360,768 va1280px kenglikda ochildi.
- Administratorning beshta himoyalangan sahifasi360px kenglikda sahifa darajasidagi yon siljishsiz ko‘rindi.
- Kirish shaklida emaildan parolga Tab orqali o‘tish va Enter bilan kirish bajarildi.

## Tekshiruv chegaralari

Mazkur tekshiruvlar butun ilova uchun umumiy xavfsizlik kafolati emas. Haqiqiy ikkinchi qurilmadan kirish, global PHP hosting/HTTPS, SMTP autentifikatsiyasi/TLS va katta yuklama/concurrency stress sinovlari ushbu QA agent tomonidan bajarilmadi. Zaxiradan tiklash dalilini koordinator alohida qo‘shadi. Parol xeshlash, PDO parametrlar va satrlarni qulflash manbadan ko‘rildi; concurrency kafolati stress sinovi bilan isbotlangan deb ko‘rsatilmaydi.

Zaxiradan tiklash bo‘yicha koordinator dalili: `docs/evidence/restore-check.json` tekshirildi. `database/backup.sql` yangi tiklash bazasiga import qilinganda barcha8 jadvaldagi yozuvlar manba baza bilan satrma-satr bir xil chiqdi. Bu tiklash sinovi koordinator tomonidan bajarilgan; QA agenti dalil faylini o‘qidi. Muhit MariaDB10.11.16; Oracle MySQL serverida alohida ishga tushirish bajarilmagan.
