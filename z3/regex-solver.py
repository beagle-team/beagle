from z3 import *

a = String('a')

s = Solver()

s.add(parse_smt2_string(
    '(declare-const a String)'
    '(assert (str.in.re a '
    '   (re.++ (str.to.re "<script>") (re.* (re.++ (re.range "a" "z") (re.range "A" "Z"))) (str.to.re "</script>"))'
    '))'
    '(assert (> (str.len a) 40))'))

print(s.check())
print(s.model()[a])

for i in range(10):
    s.add(Not(a == s.model()[a]))

    s.check()
    s.model()

    print(s.model()[a])
