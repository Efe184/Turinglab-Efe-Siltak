from turinglab import SingleTapeTM

print("=" * 60)
print("TURINGLAB DEMO — Ahmet Efe Siltak")
print("=" * 60)

input("\n[ENTER] 1. Demo: binary_increment")
print()
tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
result = tm.run("1011", verbose=True)
print(f"\nKabul: {result.accepted} | Sonuc: {result.final_tape.strip('B')} | Adim: {result.steps}")

input("\n[ENTER] 2. Demo: parantez denge kontrolu")
print()
tm2 = SingleTapeTM.from_yaml("machines/student_choice.yaml")
for girdi, beklenen in [("(()())", "KABUL"), ("(())", "KABUL"), ("(()", "RET"), (")(", "RET")]:
    r = tm2.run(girdi)
    durum = "KABUL" if r.accepted else "RET"
    print(f"  {girdi:10} -> {durum}  {'OK' if durum == beklenen else 'HATA'}")

input("\n[ENTER] 3. Demo: binary_compare")
print()
tm3 = SingleTapeTM.from_yaml("machines/binary_compare.yaml")
for girdi, beklenen in [("1100#1011", "KABUL"), ("1011#1100", "RET"), ("101#101", "RET")]:
    r = tm3.run(girdi)
    durum = "KABUL" if r.accepted else "RET"
    print(f"  {girdi:12} -> {durum}  {'OK' if durum == beklenen else 'HATA'}")

input("\n[ENTER] 4. Tum testleri calistir")
print()
import subprocess
subprocess.run(["python", "-m", "pytest", "tests/", "-v"])

print("\n" + "=" * 60)
print("DEMO TAMAMLANDI")
print("=" * 60)
