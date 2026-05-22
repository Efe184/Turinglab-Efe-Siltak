from turinglab import SingleTapeTM

tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
result = tm.run("1011", verbose=True)

print(f"\naccepted : {result.accepted}")
print(f"final_tape: {result.final_tape}")
print(f"steps    : {result.steps}")
