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

*(Adım 14'te eklenecek)*

---

## TM-3: Dizgi Kopyalayıcı (`string_copy.yaml`)

*(Adım 16'da eklenecek)*

---

## TM-4: Parantez Denge Kontrolü (`student_choice.yaml`)

*(Adım 18'de eklenecek)*
