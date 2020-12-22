#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Parser:
    def process_facts(self, facts):
        facts = facts.split(" ")
        facts.sort()
        return facts 

    def process_line(self, line, model):
        line = line.replace("\n", "")
        if "reading" in line.lower():
           return model 
        elif "answer" in line.lower():
            model['name'] = line
        elif "execute" in line:
            model['facts'] = process_facts(line)
        elif "optimization" in line.lower():
            model['optimization'] = line

        return model


    def process(self, lines):
        output = {"optimum":False, "models": []}
        clean = []
        model = {}
        capture = False
        for line in lines:
            model = process_line(line, model)
            if line == "\n":
                break
            elif line == "OPTIMUM FOUND\n":
                output['optimum'] = True
            elif model.get("optimization"):
                clean.append(model)
                model = {}

        output['models'] = clean
        return output

    def print_model(self, model):
        print(model.get("name"))
        for fact in model.get("facts"):
            print(fact)
        print()


'''
DRIVER CODE
'''
try:
    fname = "out.lp"
    with open(fname) as f:
        processed = []
        content = f.readlines()
        models = process(content)
        for model in models.get("models"):
            print_model(model)

except FileNotFoundError:
    print("File {name} not found".format(name=fname))


