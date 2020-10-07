import yaml

def rule_parse(rule):
    for key in rule:
        print(key)
        print(rule[key])
        print(type(rule[key]))


with open('app/rules.yml') as f:
    rules = yaml.load(f, Loader=yaml.FullLoader)
    print(type(rules))
    for rule in rules:
        print(rule)
        rule_parse(rule)