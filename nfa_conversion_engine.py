cstari = 0
ctranzitii = 0
csigma = 0

sigma = []
stari = []
stareInceput = []
stariFinal = []
tranzitii = []

f = open("nfa_config_file")

def statesAppendance(word,*sections):
    # in word o sa fie linia, iar primul element inainte de " ," este starea
    ls = word.split(" ,")
    stari.append(ls[0])
    if(len(sections) == 2):
        # daca o sa aiba doua sectiuni, o sa fie si stare de inceput si final
        stareInceput.append(ls[0])
        stariFinal.append(ls[0])
    elif(sections[0] == "Ending"):
        # daca '*sections' primeste 'Ending' e stare de final
        stariFinal.append(ls[0])
    else:
        # altfel, e doar stare de inceput
        stareInceput.append(ls[0])

for line in f.readlines():
    line = line.strip("\n")
    if line[0] == "#":
        continue
    if "Sigma" in line:
        csigma = 1
        continue
    if ("End" in line) and csigma == 1:
        csigma = 0
        continue
    if "States" in line:
        cstari = 1
        continue
    if ("End" in line) and cstari == 1:
        cstari = 0
        continue
    if "Transitions" in line:
        ctranzitii = 1
        continue
    if ("End" in line) and ctranzitii == 1:
        ctranzitii = 0
        continue

    if csigma == 1:
        sigma.append(line)

    if cstari == 1:
        if ("S" in line and "F" in line):
            statesAppendance(line, "Ending", "Starting")
        elif ("S" in line):
            statesAppendance(line, "Starting")
        elif ("F" in line):
            statesAppendance(line, "Ending")
        else:
            stari.append(line)

    if ctranzitii == 1:
        # aici inainte sa facem matricea, facem un array cu fiecare tranzitie
        # care o sa aiba elemente de forma [ stare1, valoare, stare2]
        ls = line.split(" ,")
        tranzitii.append(ls)


matriceNFA = [['-' for j in range(len(stari))] for i in range(len(stari))]
tabelNFA = [[set({}) for j in range(len(sigma))] for i in range(len(stari))]

for i in range(len(tranzitii)):
    # left este starea din care pleaca tranzitia
    lungimea_tranzitiei = len(tranzitii[i])-1
    left = stari.index(tranzitii[i][0])
    # right este starea in care ajunge
    right = stari.index(tranzitii[i][2])
    # pe pozitia [left][right] o sa fie valoarea care se transmite
    # f(stare1) -- val --> stare2
    if matriceNFA[left][right] == "-":
        matriceNFA[left][right] = {tranzitii[i][1]}
    else:
        matriceNFA[left][right].add(tranzitii[i][1])

    alphabetIndex = sigma.index(tranzitii[i][1])
    tabelNFA[left][alphabetIndex].add(tranzitii[i][2])


print('Matricea NFA-ului incarcat:')
for i in range(len(matriceNFA)):
    print(matriceNFA[i])
print()

 # print("Alfabet", sigma, sep=" ")
 # print("Starile:",stari, sep=" ")
 # print("Starile de inceput:",stareInceput, sep=" ")
 # print("Starile de final:",stariFinal, sep=" ")
 # print("Tranzitii:",tranzitii, sep=" ")

stariDFA = [set(stareInceput)]
tabelDFA = [tabelNFA[0]]
lungimeStariTabel = 0
i = 0
verif = True

while i <= lungimeStariTabel:
    # pentru fiecare stare din tabelul DFA
    for j in range(len(sigma)):
        if tabelDFA[i][j] not in stariDFA:
            # daca starea nu exista in tabelul DFA-ului o adaugam
            lungimeStariTabel += 1
            tabelDFA.append([])
            stariDFA.append(tabelDFA[i][j])
            # pentru fiecare litera a alfabetului aflam
            # valoarea corespunzatoare
            for k in range(len(sigma)):
                emptySet = set()
                for kk in range(len(tabelDFA[i][j])):
                    emptySet = emptySet.union(tabelNFA[kk][k])
                tabelDFA[lungimeStariTabel].append(emptySet)
    i += 1

matriceDFA = [['-' for j in range(len(stariDFA))] for i in range(len(stariDFA))]
print("Matricea DFA-ului obtinut din NFA-ul incarcat:")
for i in range(len(stariDFA)):
    for j in range(len(sigma)):
        # in stanga este starea din care pleaca
        left = i
        # in dreapta e starea in care ajunge
        right = stariDFA.index(tabelDFA[i][j])

        if matriceDFA[left][right] == "-":
            matriceDFA[left][right] = set(sigma[j])
        else:
            matriceDFA[left][right].add(sigma[j])


for i in range(len(matriceDFA)):
    # afiseaza matricea valorilor dfa-ului obtinut
    print(matriceDFA[i])






