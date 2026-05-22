def run_tm(tape_list, transitions, start, accept_states, reject_states, blank='B', max_steps=500000):
    tape = dict(enumerate(tape_list))
    head = 0
    state = start
    for step in range(max_steps):
        sym = tape.get(head, blank)
        if state in accept_states:
            return 'accept', tape, step
        if state in reject_states:
            return 'reject', tape, step
        key = (state, sym)
        if key not in transitions:
            return 'no_transition', tape, step
        write, move, nstate = transitions[key]
        tape[head] = write
        head += 1 if move == 'R' else -1
        state = nstate
    return 'timeout', tape, max_steps


T = {}

def mv(st, sym, w, d, ns): T[(st,sym)] = (w,d,ns)
def pr(st, syms):
    for s in syms: T[(st,s)] = (s,'R',st)
def pl(st, syms):
    for s in syms: T[(st,s)] = (s,'L',st)

# P=sol0, Q=sol1, R=sag0, S=sag1
# X=islenmis sol, Y=islenmis sag

# FAZA 1: Uzunluk karsilastirma
# Her tur: sol'dan bir bit al (P/Q), sag'dan bir bit al (R/S)

# Basa git
pr('q0','01#PQRSXY')
mv('q0','B','B','L','q_bk')
pl('q_bk','01#PQRSXY')
mv('q_bk','B','B','R','q_ll')  # gerçek bas

# Sol'dan en soldaki orijinal biti al
mv('q_ll','P','P','R','q_ll')
mv('q_ll','Q','Q','R','q_ll')
mv('q_ll','0','P','R','q_lr')
mv('q_ll','1','Q','R','q_lr')
mv('q_ll','#','#','R','q_ld')   # sol bitti

# Sol bitti: sag'da bit var mi?
mv('q_ld','R','R','R','q_ld')
mv('q_ld','S','S','R','q_ld')
mv('q_ld','0','0','R','q_rej')  # sag devam -> reject
mv('q_ld','1','1','R','q_rej')
mv('q_ld','B','B','L','q_cmp_bk')  # esit uzunluk -> bit karsilastir

# Sol bit alindi, sag'a git
pr('q_lr','01PQ')
mv('q_lr','#','#','R','q_rr')

# Sag'dan esleseni al
mv('q_rr','R','R','R','q_rr')
mv('q_rr','S','S','R','q_rr')
mv('q_rr','0','R','L','q_bk')   # sag0=R
mv('q_rr','1','S','L','q_bk')   # sag1=S
mv('q_rr','B','B','R','q_acc')  # sag bitti, sol devam -> accept

# FAZA 2: Esit uzunluk - bit bit karsilastir
# Basa don
pl('q_cmp_bk','PQRSXY#01')
mv('q_cmp_bk','B','B','R','q_cl')  # gercek bas

# Sol'dan P veya Q al
mv('q_cl','X','X','R','q_cl')
mv('q_cl','P','X','R','q_cg0')   # sol=0
mv('q_cl','Q','X','R','q_cg1')   # sol=1
mv('q_cl','#','#','R','q_rej')   # hepsi esit
mv('q_cl','B','B','R','q_rej')

# Sol=0, sag'a git
pr('q_cg0','XPQ01')
mv('q_cg0','#','#','R','q_cr0')

mv('q_cr0','Y','Y','R','q_cr0')
mv('q_cr0','R','Y','L','q_cb')   # 0==0, devam
mv('q_cr0','S','Y','R','q_rej')  # sol0 < sag1 -> reject
mv('q_cr0','B','B','R','q_rej')

# Sol=1, sag'a git
pr('q_cg1','XPQ01')
mv('q_cg1','#','#','R','q_cr1')

mv('q_cr1','Y','Y','R','q_cr1')
mv('q_cr1','R','Y','R','q_acc')  # sol1 > sag0 -> accept
mv('q_cr1','S','Y','L','q_cb')   # 1==1, devam
mv('q_cr1','B','B','R','q_rej')

# Geri don
pl('q_cb','XYPQRS#01')
mv('q_cb','B','B','R','q_cl')

# Terminal
for sym in '01#PQRSXYB':
    T[('q_acc',sym)] = (sym,'R','q_acc')
    T[('q_rej',sym)] = (sym,'R','q_rej')

tests = [
    ('1100#1011', True),
    ('1011#1100', False),
    ('101#101',   False),
    ('1#0',       True),
    ('0#1',       False),
]

for inp, expected_acc in tests:
    reason, tape, steps = run_tm(list(inp), T, 'q0', {'q_acc'}, {'q_rej'})
    got_acc = reason == 'accept'
    ok = 'OK' if got_acc == expected_acc else 'FAIL'
    exp_str = 'accept' if expected_acc else 'reject'
    print(f'{ok} | {inp} -> {reason} (beklenen: {exp_str}) steps={steps}')
