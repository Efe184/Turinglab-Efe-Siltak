# Tasarım Notları

---

## TM-1: Unary → Binary Çevirici (`unary_to_binary.yaml`)

### 1. Strateji

Makine, şeridi iki bölgeye ayırır: solda unary girdisi (1'ler), sağda `#` ayracının ötesinde binary sonuç. Her turda en soldaki işlenmemiş `1`'i `X` ile işaretler, ardından binary bölümünü 1 artırır (binary increment mantığı). Tüm `1`'ler `X`'e dönüşünce `X` ve `#` silinerek yalnızca binary sonuç kalır. Boş girdi için doğrudan `0` yazılır.

### 2. Durum Sayısı

Toplam 16 durum kullanıldı. Azaltmak teorik olarak mümkün; örneğin `q_shift0` ve `q_shift1` birleştirilebilirdi, ancak carry aşması sırasında MSB ekleme ve bit kaydırma işlemleri ayrı durumlar gerektirdi. 12'nin altına indirmek okunabilirliği ciddi ölçüde düşürürdü.

### 3. Şerit Alfabesi Seçimi

`X` işaretleyicisi, unary `1`'lerini "işlendi" olarak etiketlemek için kullanıldı. `X` yerine `0` kullanılsaydı, binary bölümündeki `0`'larla karışırdı. `#` ayracı, iki bölgeyi birbirinden net biçimde ayırır; olmadan kafa hangi bölgede olduğunu anlayamaz.

### 4. Karmaşıklık

Girdi uzunluğu `n` iken her tur şeridi yaklaşık `2n` kez tarar (sola ve sağa). `n` tur olduğundan toplam adım sayısı O(n²). Bu tek şeritli TM'lerin kaçınılmaz bedelidir; çok şeritli olsaydı O(n log n) mümkündü.

### 5. Hata Ayıklama Hikâyesi

İlk tasarımda `q_carry` durumu `#` sembolüyle karşılaşınca ne yapacağını bilmiyordu; `no_transition` hatası veriyordu. Sebep: `1111` gibi tüm bitleri `1` olan unary girdilerinde binary carry tamamen taşıyordu ve binary'ye yeni bir MSB eklenmesi gerekiyordu. Bu durum için `q_new_msb` durumu eklendi; mevcut bitleri sağa kaydırıp en sola `1` yazıyor. Kaydırma sırasında `0` ve `1`'in taşınması için `q_shift0`/`q_shift1` ayrımına gidildi.

---

## TM-2: İki İkili Sayıyı Karşılaştır (`binary_compare.yaml`)

### 1. Strateji

Makine iki aşamada çalışır. **Aşama 1 — Uzunluk karşılaştırması:** Şeridin sol kısmındaki bitleri sırayla `P` (0 yerine) ve `Q` (1 yerine), sağ kısmındakileri `R` (0) ve `S` (1) ile işaretler. Sol taraf bitince sağ tarafta bit kalmışsa reject, sağ taraf erken biterse accept edilir. **Aşama 2 — Bit bit karşılaştırma:** Uzunluklar eşitse, `P/Q` ile `R/S` soldan sağa sırayla karşılaştırılır; ilk farklı bit bulununca karar verilir (1>0 ise accept, 0<1 ise reject). Tüm bitler eşitse reject.

### 2. Durum Sayısı

15 durum kullanıldı. Çok şeritli bir TM'de 5-6 durum yeterli olurdu; tek şerit zorunlu kıldığı sola-sağa taramalar nedeniyle uzunluk aşaması ve bit karşılaştırma aşaması için ayrı durum kümeleri gerekti.

### 3. Şerit Alfabesi Seçimi

Dört işaretleyici (`P`, `Q`, `R`, `S`) seçilmesinin sebebi bit değerini korumaktır. Tek bir `X` işaretleyiciyle gidilseydi, karşılaştırma aşamasında hangi bitin 0, hangisinin 1 olduğu bilinemezdi.

### 4. Karmaşıklık

Her tur sol taraftan bir bit, sağ taraftan bir bit seçilirken şerit boyunca ileri-geri tarama yapılır: ~O(n) adım. `n` bit için `n` tur gerekeceğinden toplam O(n²). Bit bit karşılaştırma aşaması da benzer şekilde O(n²). Toplamda **O(n²)** — tek şerit geri-gidiş maliyetinin kaçınılmaz sonucu.

### 5. Hata Ayıklama Hikâyesi

İlk tasarımda eşit uzunluk tespiti sonrası basa dönüş durumu (`q_cmp_bk`) eksikti. Uzunluk tespiti sağ uçta tamamlanıyor, bit karşılaştırması ise sol uçtan başlamalıydı. `q_ld` durumu (sol bitti, sağ da bitti) doğrudan `q_cl`'ye geçmeye çalışınca head doğru konumda değildi ve P/Q bitleri görülmeden serit sonu blanki ile karşılaşılıyordu; makine yanlış reject dönüyordu. Aradaki `q_cmp_bk` durumu eklenerek head gerçek serit başına (`B`'ye kadar sol) taşındı.

---

---

## TM-3: Dizgi Kopyalayıcı (`string_copy.yaml`)

### 1. Strateji

Makine şeridi iki bölgeye ayırır: solda orijinal string, sağda `#` ayracından sonra kopyası. Her turda en soldaki işlenmemiş `a`'yı `A`'ya, `b`'yi `C`'ye dönüştürür (işlendiğini işaretlemek için). Ardından `#`'in en sağına gidip o karakterin kopyasını yazar, basa döner. Tüm karakterler işlenince `A` ve `C`'leri geri `a` ve `b`'ye çevirerek makine kabul eder.

### 2. Durum Sayısı

12 durum kullanıldı. Her karakter (`a`, `b`) için ayrı kopyalama durumları gerekti (`q_copy_a`, `q_copy_b`, `q_write_a`, `q_write_b`). Alfabeyi genişletseydik (örneğin 3 karakter), her biri için iki ek durum eklenecekti — durum sayısı alfabe boyutuyla doğrusal büyür.

### 3. Şerit Alfabesi Seçimi

`A` ve `C` büyük harf işaretleyicileri seçildi çünkü `B` zaten blank olarak rezerve. `B_marked` gibi çok karakterli etiket kullanılamaz; her şerit sembolü tek karakter olmalıdır. `#` ayracı iki bölgeyi birbirinden ayırır; olmadan kafa kopyalanmış bölgede mi yoksa orijinalde mi olduğunu bilemezdi.

### 4. Karmaşıklık

Girdi uzunluğu `n` iken her tur şeridi yaklaşık `2n` tarar (sola ve sağa). `n` tur yapıldığından toplam **O(n²)** adım. Son temizleme (A/C → a/b) O(n) ek adım ekler.

### 5. Hata Ayıklama Hikâyesi

İlk tasarımda `q0` durumu hem ilk turu hem sonraki turları aynı şekilde yönetiyordu. Ancak ilk turda henüz `#` yokken `q_go_end_init` sona gidip `#` ekliyordu; sonraki turlar ise varolan `#`'i geçip kopyalama bölgesinin sonuna gitmeliydi. Bu ayrım yapılmadığında `#`'in üzerine tekrar `#` yazılıyor, sonuç `ab##ab` şeklinde bozuluyordu. `q_go_end_init` ve `q_go_sep_end_init` durumları ayrıştırılarak düzeltildi.

---

---

## TM-4: Parantez Denge Kontrolü (`student_choice.yaml`)

*(Adım 18'de eklenecek)*
