# TuringLab

Python ile yazılmış tek şeritli deterministik Turing makinesi simülatörü. YAML formatında tanımlanan makineleri yükler, adım adım çalıştırır ve sonucu raporlar.

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

```python
from turinglab import SingleTapeTM

tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
result = tm.run("1011", verbose=True)

print(result.accepted)     # True
print(result.final_tape)   # 1100B
print(result.steps)        # adım sayısı
```

## Testleri Çalıştırma

```bash
pytest tests/ -v
```
