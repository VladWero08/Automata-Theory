import re

variables = []
start_variable = []
terminals = []
rules = {}
errors = []

f = open("cfg_config_file")
s = [linie.strip("\n") for linie in f]
line_cnt = 0

def validateVariables():
    global line_cnt
    line_cnt += 1

    while s[line_cnt] != "--end":
        # if the value is not repeated in terminals
        ok = 0
        if s[line_cnt] not in terminals:
            # if the variable is the start variable
            # we need to delete the last 7 characters
            if len(s[line_cnt]) >= 7 and s[line_cnt][-7:]== ", start":
                s[line_cnt] = s[line_cnt][:-7]
                ok = 1
            # if the value is not repeated in variables
            if s[line_cnt] not in variables:
                if ok == 1:
                    start_variable.append(s[line_cnt])
                    # if there are multiple start variables, print the error
                    if len(start_variable) > 1:
                        error = "Line " + str(line_cnt) + ":" + "There cannot be more than one starting variable." + "("
                        for x in start_variable:
                            error = error + x + " "
                        error = error + "- are there)"
                        errors.append(error)

                variables.append(s[line_cnt])
            else:
                error = "Line " + str(line_cnt) + ": " + "There is already a variable with the value of " + s[line_cnt] + "."
                errors.append(error)
        else:
            error = "Line " + str(line_cnt) + ": " + "There is already a terminal with the value of " + s[line_cnt] + "."
            errors.append(error)
        line_cnt += 1
    line_cnt += 1

    # check if we have a start variable
    if len(start_variable) == 0:
        error = "You need to introduce a starting variable."
        errors.append(error)

def validateTerminals():
    global line_cnt
    line_cnt += 1

    while s[line_cnt] != "--end":
        # if the value is not repeated in variables
        if s[line_cnt] not in variables:
            # if the value is not repeated in terminals
            if s[line_cnt] not in terminals:
                terminals.append(s[line_cnt])
            else:
                error = "Line " + str(line_cnt) + ": " + "There is already a terminal with the value of " + s[line_cnt] + "."
                errors.append(error)
        else:
            error = "Line " + str(line_cnt) + ": " + "There is already a variable with the value of " + s[line_cnt] + "."
            errors.append(error)
        line_cnt += 1
    line_cnt += 1

def validateRules():
    global line_cnt
    line_cnt += 1
    while s[line_cnt] != "--end":
        list = s[line_cnt].split("->",1)
        # first we verify if the config file is valid
        if len(list) < 2:
            error = "Line " + str(line_cnt) + " :" + " The sintax of a rule needs to be: variable_name->terminal_name|variable_name or any valid combination."
            errors.append(error)
        else:
            if list[0] not in variables:
                error = "Line " + str(line_cnt) + " : " + list[0] + " is not a variable."
                errors.append(error)
            else:
                # if there are multiple rules to one variable
                rules[list[0]] = list[1].split("|")
        line_cnt += 1

    line_cnt += 1
    if len(start_variable) == 1:
        if start_variable[0] not in rules.keys():
            error = "You need to introduce a rule that starts from the starting variable."
            errors.append(error)

for i in range(3):
    # variables validation
    if s[line_cnt] == "Variables:":
        validateVariables()
    # terminals validation
    elif s[line_cnt] == "Terminals:":
        validateTerminals()
    # rules validation
    else:
        validateRules()

# check if the strings in rule, that should be terminals, are terminals
def checkInTerminal(j):
    res = re.findall("^(?!<\w+>).", j)
    # if the rule goes into a terminal, check if the terminal is valid
    if len(res) > 0:
        for k in range(len(res)):
            if res[k] not in terminals:
                error = "You cannot add a rule for a terminal that does not exists." + "( " + res[k] + ")"
                errors.append(error)
                return False
    return True

# check if the strings in rule, that should be variables, are variables
def checkInVariables(j):
    res = [i[1:-1] for i in re.findall(r'<\w+>', j)]
    # if the rule goes into a variable, check if the variable is valid
    for k in range(len(res)):
        if res[k] not in variables:
            error = "You cannot add a rule for a variable that does not exists." + "( " + res[k] + ")"
            errors.append(error)
            return False
        if res[k] not in rules.keys():
            error = "You cannot use a rule that goes nowhere.( no rule starts from " + res[k] + ")"
            errors.append(error)
            return False
    return True

def checkVariableEndsInTerminal(var):
    global valid_variable
    for j in rules[var]:
        if checkInTerminal(j) == True:
            return True
        res = [i[1:-1] for i in re.findall(r'<\w+>', j)]
        for k in range(len(res)):
            if checkInTerminal(res[k]) == True:
                checkVariableEndsInTerminal(res[k])
    return False


for i in rules:
    for j in rules[i]:
        if "<" in j and ">" in j:
            # if the rule goes into a variable, check if the variable is valid
            res = [i[1:-1] for i in re.findall(r'<\w+>', j)]
            for k in range(len(res)):
                if res[k] not in variables:
                    # if the rule goes into a variable that doesn't exist
                    error = "You cannot add a rule for a variable that does not exists." + "( " + res[k] + ")"
                    errors.append(error)
                else:
                    # if the rule goes into a variable that doesn't have a rule of her own
                    if res[k] not in rules.keys():
                        error = "You cannot use a rule that goes nowhere.( no rule starts from " + res[k] + ")"
                        errors.append(error)
                    else:
                        if checkVariableEndsInTerminal(res[k]) == False:
                            error = "The variable " + res[k] + " doesn't end in a terminal."
                            errors.append(error)

                checkInTerminal(j)
        else:
            checkInTerminal(j)

if len(errors) == 0:
    print("Your grammar is valid!")
else:
    for i in range(len(errors)):
        print(errors[i])