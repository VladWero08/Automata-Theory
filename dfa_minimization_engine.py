cstari = 0
ctranzitii = 0
csigma = 0
validChecker = ""

sigma = []
stari = []
stareInceput = []
stariFinal = []
tranzitii = []

f = open("dfa_config_file")

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

# CONSTRUIRE TABEL DE STARI
tabelTranzitii = [['' for i in range(len(sigma))] for j in range(len(stari))]

for i in range(len(tranzitii)):
    left = stari.index(tranzitii[i][0])
    right = sigma.index(tranzitii[i][1])
    tabelTranzitii[left][right] = tranzitii[i][2]

# for linie in range(len(tabelTranzitii)):
#     print(tabelTranzitii[linie])


# CONSTRUIRE MATRICE DE VALORI
matriceValori = [['-' for j in range(len(stari))] for i in range(len(stari))]

for i in range(len(tranzitii)):
    # left este starea din care pleaca tranzitia
    left = stari.index(tranzitii[i][0])
    # right este starea in care ajunge
    right = stari.index(tranzitii[i][2])
    # pe pozitia [left][right] o sa fie valoarea care se transmite
    # f(stare1) -- val --> stare2
    verif = 1
    for j in range(len(stari)):
        if tranzitii[i][1] in matriceValori[left][j]:
            verif = 0
            break;

    if verif == 1:
        if matriceValori[left][right] == "-":
            matriceValori[left][right] = {tranzitii[i][1]}
        else:
            matriceValori[left][right].add(tranzitii[i][1])
    else:
        validChecker = "One state can go through in alphabet value only to a single other state."
        break

# CONSTRUIRE MATRICE SUB DIAGONALA - PAS 1
matriceSubDiagonala = []
for i in range(len(stari)):
    # pentru fiecare stare punem numarul de stari
    # corespunzator pozitiei din lista de stari
    # ex. daca q2 e pe pozitia 2, o sa aiba doua '-', etc.
    ls = []
    for j in range(i):
        if (stari[i] in stariFinal and stari[j] not in stariFinal) or (stari[j] in stariFinal and stari[i] not in stariFinal):
            ls.append(1)
        else:
            ls.append(0)
    matriceSubDiagonala.append(ls)

# MARCAREA STARILOR - PAS 2
esteMarcat = True
while(esteMarcat == True):
    esteMarcat = False
    for i in range(len(matriceSubDiagonala)):
        for j in range(len(matriceSubDiagonala[i])):
            # cautam pe fiecare pozitie din submatrice elementele = 0
            if matriceSubDiagonala[i][j] == 0:
                # pentru fiecare litera din alfabet cautam tranzitiile
                # asociate starilor i si j
                for k in range(len(sigma)):
                    # starea pe coloana din stanga
                    stare1 = tabelTranzitii[i][k]
                    # starea pe linia de sus
                    stare2 = tabelTranzitii[j][k]

                    # pentru nu a iesit din matrice !
                    left = max(stari.index(stare1), stari.index(stare2))
                    right = min(stari.index(stare1), stari.index(stare2))

                    if left!=right:
                        if matriceSubDiagonala[left][right] == 1:
                            matriceSubDiagonala[i][j] = 1
                            esteMarcat = True

# stari DFA minimalizat
stariMiniDFA = []
stariMiniDFA.append(stareInceput)
# stari finale DFA minimalizat
stariFinaleMiniDFA = []

miniVerif = []
miniVerif.append(stareInceput)

for i in range(len(matriceSubDiagonala)):
    for j in range(len(matriceSubDiagonala[i])):
        if matriceSubDiagonala[i][j] == 0:
            # unim cele doua stari intr-una si o adaugam in starile
            # dfa-ului minimalizat
            stariMiniDFA.append([stari[i],stari[j]])
            if stari[i] in stariFinal or stari[j] in stariFinal:
                stariFinaleMiniDFA.append([stari[i],stari[j]])
            miniVerif.append(stari[i])
            miniVerif.append(stari[j])

for i in range(len(stariFinal)):
    if stariFinal[i] not in miniVerif:
        stariFinaleMiniDFA.append([stariFinal[i]])
        stariMiniDFA.append([stariFinal[i]])

def cautaMiniDFA(stare):
    for i in range(len(stariMiniDFA)):
        for j in range(len(stariMiniDFA[i])):
            if stare == stariMiniDFA[i][j]:
                return i
    return -1

tabelTranzitiiMiniDFA = [['' for i in range(len(sigma))] for j in range(len(stariMiniDFA))]

for i in range(len(stariMiniDFA)):
    for j in range(len(stariMiniDFA[i])):
        for k in range(len(sigma)):
            left = stari.index(stariMiniDFA[i][j])
            right = k
            # cauta pozitia pe care se afla tranzitia prin sigma[k]
            poz = cautaMiniDFA(tabelTranzitii[left][right])
            tabelTranzitiiMiniDFA[i][k] = stariMiniDFA[poz]

matriceMiniDFA = [['-' for i in range(len(stariMiniDFA))] for j in range(len(stariMiniDFA))]

# print("Minimalized DFA's states:")
# print(stariMiniDFA)
# print()
#
# print("Tabel of transitions for the minimalized DFA:")
# for linie in range(len(tabelTranzitiiMiniDFA)):
#     print(tabelTranzitiiMiniDFA[linie])
# print()

for linie in range(len(tabelTranzitiiMiniDFA)):
    for i in range(len(sigma)):
        # pozitia valorii din tabelul de tranzitii in array-ul de stari
        right = stariMiniDFA.index(tabelTranzitiiMiniDFA[linie][i])

        if matriceMiniDFA[linie][right] == "-":
            matriceMiniDFA[linie][right] = set(sigma[i])
        else:
            matriceMiniDFA[linie][right].add(sigma[i])


print("Value matrix of minimalized DFA:")
for linie in range(len(matriceMiniDFA)):
    print(matriceMiniDFA[linie])

