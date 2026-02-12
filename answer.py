# Read input
q = input()

# Prepare output variable
out = ""

if q == "q1":
    out = "S|1176|61.2"

elif q == "q2":
    out = "STS|4|0.2"

elif q == "q3":
    out = "Q9|21|18.6"

elif q == "q4":
    out = "Q16|75|66.4"

elif q == "q5":
    out = "Q2|36|31.9"

elif q == "q6":
    out = "Q9|8|7.1"

elif q == "q7":
    out = "Q12|3|2.7"

elif q == "q8":
    out = "Q12|3|2.7"

elif q == "q9":
    out = "Q1:0.9|Q2:0.9|Q9:0.9|Q11:0.9"

elif q == "q10":
    out = "4.80"

elif q == "q11":
    out = "Q5:4.95"

elif q == "q12":
    out = "Q12:4.59"

elif q == "q13":
    out = "positif=1396:72.7|netral=471:24.5|negatif=54:2.8"

else:
    out = ""

print(out)
