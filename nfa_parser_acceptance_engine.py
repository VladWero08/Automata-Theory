cstari = 0
ctranzitii = 0
csigma = 0
validChecker = ""

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

matrice = [['-' for j in range(len(stari))] for i in range(len(stari))]

for i in range(len(tranzitii)):
    # left este starea din care pleaca tranzitia
    lungimea_tranzitiei = len(tranzitii[i])-1
    left = stari.index(tranzitii[i][0])
    # right este starea in care ajunge
    right = stari.index(tranzitii[i][2])
    # pe pozitia [left][right] o sa fie valoarea care se transmite
    # f(stare1) -- val --> stare2
    if matrice[left][right] == "-":
        matrice[left][right] = {tranzitii[i][1]}
    else:
        matrice[left][right].add(tranzitii[i][1])

# Afiseaza matricea valorilor NFA-ului daca acesta este valid -> ex 2.1
if len(stareInceput) == 1:
    print('Matricea valorilor:')
    for i in range(len(matrice)):
        print(matrice[i])
else:
    validChecker += "There cannot be more than one starting state.\n"

cuvantValid = 0

# Validarea NFA-ului -> ex 2.2
def validareNFA(word, linie):
    global matrice, cuvantValid
    n = len(word)
    for i in range(n):
        for j in range(len(matrice[linie])):
            if word[i] in matrice[linie][j]:
                linie = matrice[linie].index(matrice[linie][j])
                validareNFA(word[i+1:], linie)
    if stari[linie] in stariFinal:
        cuvantValid = 1

print("Starile:",stari, sep=" ")
print("Starile de inceput:",stareInceput, sep=" ")
print("Starile de final:",stariFinal, sep=" ")
print("Tranzitii:",tranzitii, sep=" ")
validareNFA("0000001010",0)
if( cuvantValid == 1):
    print("Cuvantul este valid.")
else:
    print("Cuvantul nu este valid")
