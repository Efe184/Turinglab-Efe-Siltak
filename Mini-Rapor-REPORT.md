# TuringLab — Mini-Rapor

**Öğrenci:** Ahmet Efe Sıltak  
**Ders:** Hesaplama Kuramı — Selçuk Üniversitesi Bilgisayar Mühendisliği  
**Tarih:** Mayıs 2026

---

## 1. Giriş

TuringLab, deterministik tek-şeritli Turing makinelerini (TM) YAML dosyalarından yükleyip
çalıştıran bir Python kütüphanesidir. Proje iki ana bölümden oluşur: makineleri yorumlayan
bir motor (Bölüm 1) ve bu motor üzerinde test edilen dört özgün TM tasarımı (Bölüm 2).

Temel kullanım şöyledir:

```python
from turinglab import SingleTapeTM

tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
result = tm.run("1011", verbose=True)
print(result.accepted, result.final_tape.strip("B"))  # True  1100
```

Proje tamamen Python 3.13 ile yazılmış; yalnızca PyYAML ve pytest bağımlılıkları kullanılmıştır.


tm2 = SingleTapeTM.from_yaml("machines/student_choice.yaml")
print(tm2.run("(()())").accepted)
print(tm2.run("(())").accepted)
print(tm2.run("(()").accepted)
print(tm2.run(")(").accepted)

exit()
python -m pytest tests/ -v
---

## 2. Mimari

### Modül Organizasyonu

```
turinglab/
├── __init__.py       # SingleTapeTM ve RunResult dışa aktarımı
└── tm_engine.py      # Tüm motor kodu: Tape, Configuration, RunResult, SingleTapeTM
machines/             # YAML makine tanımları
tests/                # pytest test dosyaları
docs/                 # Tasarım notları ve demo video
```

### Önemli Tasarım Kararları

**Şerit temsili — `dict[int, str]` (sparse):**  
Şerit bir Python sözlüğü olarak tutulur; sadece yazılan hücreler bellekte yer kaplar.
`list` kullanılsaydı her sola-taşma veya sağa-genişleme için yeniden boyutlandırma
gerekirdi. `dict` ile kafa negatif konumlara gidebilir, boyut sınırı yoktur.

**`dataclass` kullanımı:**  
`Configuration` ve `RunResult` Python `dataclass`'ları olarak tanımlandı. Normal sınıf
yerine `dataclass` kullanmak; `__init__`, `__repr__` ve tip ipuçlarını otomatik sağlar,
gereksiz kodu ortadan kaldırır.

**Geçiş tablosu — `dict[(state, symbol), (write, dir, new_state)]`:**  
Transition'lar `(durum, sembol)` çiftini anahtar olarak kullanan bir sözlükte tutulur.
Bu yapı O(1) arama süresi sağlar; liste taramasına gerek kalmaz.

**Sonlanma koşulları:**

| Durum | `accepted` | `reason` |
|-------|-----------|---------|
| Kabul durumuna ulaşıldı | `True` | `"accept"` |
| Geçerli geçiş yok | `False` | `"no_transition"` |
| `max_steps` aşıldı | `False` | `"timeout"` |
| Kafa sol sınırın dışına çıktı | `False` | `"head_out_of_bounds"` |

---

## 3. Tasarlanan Turing Makineleri

### TM-1 — Unary → Binary Çevirici (`unary_to_binary.yaml`)

Girdi olarak `n` tane `1` içeren bir dizi alır (unary gösterim), çıktı olarak `n`'nin ikili
gösterimini şeride yazar. Algoritma: her turda en sağdaki işaretsiz `1`'i `X` ile işaretle,
sonuçtaki ikili sayıyı sona yaz. En zorlandığım nokta, boş girdi için `"0"` üretmekti;
başlangıç blank kontrolü eklenmeden önce makine accept durumuna ulaşmadan sonlanıyordu.

**Karmaşıklık:** O(n²) — her bit için şerit baştan sona taranır.

### TM-2 — İkili Sayı Karşılaştırıcı (`binary_compare.yaml`)

`A#B` formatında iki ikili sayı alır; `A > B` ise kabul, değilse ret. Strateji: her turda
sol taraftan bir biti işaretle (`X`), `#` geçildikten sonra sağ taraftan karşılık gelen biti
bul, bit farklıysa sonuca göre karar ver. `#` ayracını kaçırdığımda kafa sonsuz döngüye
giriyordu; `max_steps` guard'ı sayesinde bu hatayı fark ettim.

**Karmaşıklık:** O(n²) — tek şeritte her bit karşılaştırması ileri-geri tarama gerektirir.

### TM-3 — Dizgi Kopyalayıcı (`string_copy.yaml`)

`abba` → `abba#abba` dönüşümü gerçekleştirir. Her turda sıradaki `a` veya `b` karakterini
büyük harf işaretleyicisiyle (`A`, `B_marked`) işaretler, `#` ayracının ötesine taşır,
orijinal konuma döner. İşaretleyici kullanmadan kopyalamak denendiğinde hangi karakterin
nereye yazıldığı takip edilemedi.

**Karmaşıklık:** O(n²) — n karakter için her biri n adım ileri taşınır.

### TM-4 — Parantez Denge Kontrolü (`student_choice.yaml`)

Öğrenci seçimi olarak parantez denge kontrolü tasarlandı. Strateji: şeridi tarayarak
`(` görünce sola kayıt tut, `)` görünce kayıttan sil; sonunda kayıt sıfırsa kabul.
Tek şeritte sayaç `(` karakterlerini `X` ile işaretleyerek takip edildi. `)` geldiğinde
eşleşecek `X` yoksa ret.

**Karmaşıklık:** O(n²) — her `)` için en yakın eşleşmeyen `(` aranır.

---

## 4. Kavramsal Tartışma

**Soru (c): Modern bir programlama dili (Python) ile TM arasındaki "boşluk" nedir?**

Turing makinesi, hesaplamanın matematiksel modelidir: sonsuz şerit, sonlu durum kümesi,
ve deterministik geçiş fonksiyonu. Python ise bu modelin pratik bir uzantısıdır.

İki temel fark öne çıkar:

**1. Soyutlama seviyesi.** TM'de her işlem — bir karakteri okumak, yazmak, bir adım
sola ya da sağa hareket etmek — ayrı bir geçiş kuralıdır. Python'da `x = x + 1` tek bir
satırdır; ama bu işlem, TM'de onlarca geçiş adımına karşılık gelir. Python, TM'nin
üzerinde binlerce soyutlama katmanı barındırır (bytecode, yorumlayıcı, işletim sistemi,
donanım).

**2. Bellek modeli.** TM'nin şeridi teorik olarak sonsuzdur. Python'da bellek fiziksel
olarak sınırlıdır; ancak Python'un dinamik bellek yönetimi bu sınırı programcıdan gizler.
Pratikte ikisi de "yeterince büyük" girdiler için aynı hesaplamaları yapabilir.

**Boşluk nerede kapanır?** Church-Turing tezi, TM'nin hesaplayabildiği her şeyi Python'un
da hesaplayabileceğini (ve tersini) öne sürer. Bu projede bunu somutlaştırdım: Python ile
yazdığım `run()` fonksiyonu, herhangi bir TM'yi simüle edebilir. Yani Python, evrensel bir
Turing makinesi gibi davranır. Gerçek boşluk; verimlilik, yazım kolaylığı ve insan
okunabilirliğidir — hesaplama gücünde değil.

---

## 5. Sınırlar ve İleri Çalışma

**Eksik kalanlar:**

- **Çok-şeritli TM (Bonus A):** TM-2'yi tasarlarken tek şeritte O(n²) karmaşıklığa
  takıldım. İki şeritli versiyon O(n) olurdu; `multi_tape.py` bu projenin doğal bir
  sonraki adımı.
- **Görselleştirici:** Verbose mod şeridi terminale yazdırıyor ancak animasyonlu bir
  görsel çok daha anlaşılır olurdu. `Pillow` ile adım adım PNG üretimi eklenebilir.
- **NTM desteği:** `ntm.py` ile BFS tabanlı non-deterministik simülasyon eklenebilir;
  bu, "01 alt dizisi var mı?" gibi problemleri daha doğal modellemeye izin verir.
- **YAML doğrulama:** Şu an geçiş tablosundaki tutarsızlıklar (örn. var olmayan duruma
  geçiş) çalışma zamanında sessizce `no_transition` döndürüyor; başlangıçta uyarı
  verilebilir.

**Bir hafta daha olsaydı:** Bonus A (çok-şeritli motor) + TM-2'nin iki şeritli versiyonu
yazılırdı. Bu, tek-şeritli ve çok-şeritli TM'lerin adım sayısı farkını deneysel olarak
gösterme fırsatı verirdi.

---

## 6. Kaynakça

- Sipser, M. (2013). *Introduction to the Theory of Computation* (3. baskı). Cengage.
  — TM formal tanımı, geçiş fonksiyonu, hesaplama tarihi kavramları.
- Python Docs: `dataclasses` modülü — https://docs.python.org/3/library/dataclasses.html
- PyYAML Docs — https://pyyaml.org/wiki/PyYAMLDocumentation
- pytest Docs — https://docs.pytest.org/
