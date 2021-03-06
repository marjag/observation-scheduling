#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Class Parser parses clingo output
'''
class Parser:
    next_line_facts = False
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
            self.next_line_facts = True
        elif self.next_line_facts == True:
            self.next_line_facts = False
            model['facts'] = self.process_facts(line)
        elif "optimization" in line.lower():
            model['optimization'] = line
        elif "UNSATISFIABLE" in line:
            raise ValueError()
        return model


    def process(self, lines):
        output = {"optimum":False, "models": []}
        clean = []
        model = {}
        capture = False
        for line in lines:
            model = self.process_line(line, model)
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
    '''
    def process_file(self,file_path,answers=1):
        '''
        DRIVER CODE
        '''
        try:
            with open(file_path) as f:
                processed = []
                content = f.readlines()
                parsed = self.process(content)
                models = parsed.get('models')
                answers_found = len(models)
                for model in models[answers_found-int(answers):]:
                    self.print_model(model)
        except ValueError:
            # unsatisfiable
            print(''.join(content))
        except FileNotFoundError:
            print("File {name} not found".format(name=file_path))
