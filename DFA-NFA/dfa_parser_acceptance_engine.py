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

        # Verificare daca exista valoarea respectiva in alfabet
        if ls[1] not in sigma:
            validChecker += "Transition value does not exist in the alphabet.\n"

        tranzitii.append(ls)

matrice = [['-' for j in range(len(stari))] for i in range(len(stari))]

for i in range(len(tranzitii)):
    # left este starea din care pleaca tranzitia
    if tranzitii[i][0] in stari:
        left = stari.index(tranzitii[i][0])
    else:
        validChecker += "Transition states do not exist in DFA's states.\n"
    # right este starea in care ajunge
    if tranzitii[i][2] in stari:
        right = stari.index(tranzitii[i][2])
    else:
        validChecker += "Transition states do not exist in DFA's states.\n"
    # pe pozitia [left][right] o sa fie valoarea care se transmite
    # f(stare1) -- val --> stare2

    verif = 1
    for j in range(len(stari)):
        if tranzitii[i][1] in matrice[left][j]:
            verif = 0
            break;

    if verif == 1:
        if matrice[left][right] == "-":
            matrice[left][right] = {tranzitii[i][1]}
        else:
            matrice[left][right].add(tranzitii[i][1])
    else:
        validChecker += "One state can go through in alphabet value only to a single other state.\n"
        break

# afiseaza matricea valorilor DFA-ului daca acesta este valid -> ex 1.1
if(len(stareInceput) == 1):
    if validChecker == "":
        print('Matricea valorilor:')
        for i in range(len(matrice)):
            print(matrice[i])
    else:
        print(validChecker)
else:
    validChecker += "There cannot be more than one starting state.\n"
    print(validChecker)

# validare DFA -> ex 1.2
def validareDFA(word):
    global matrice
    n = len(word)
    k = 0
    veriff = 0
    for i in range(n):
        copiek = k
        for j in range(len(stari)):
            if word[i] in matrice[k][j]:
                verif = 1
                k = j
        if verif == 0:
            break
    if stari[k] in stariFinal:
        print("Cuvantul este valid.")
    else:
        print("Cuvantul nu este valid.")

# print("Starile:",stari, sep=" ")
# print("Starile de inceput:",stareInceput, sep=" ")
# print("Starile de final:",stariFinal, sep=" ")
# print("Tranzitii:",tranzitii, sep=" ")
# validareDFA("0000011110")
# baa acc