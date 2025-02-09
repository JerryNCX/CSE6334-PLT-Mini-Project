import re

def tokenize(command):
    tokens = []
    token_specs = [
        ('EVENT', r'on|schedule|if|repeat|activate'),
        ('SENSOR', r'motion|temperature|humidity|door|light|sound'),
        ('DEVICE', r'lights|AC|fan|door|alarm|sprinkler|watering'),
        ('OPERATION', r'on|off|increase|decrease|open|close|start|turn on|turn off|check'),
        ('MODE', r'night mode|vacation mode|silent mode'),
        ('OPERATOR', r'>|<|>=|<=|=='),
        ('VALUE', r'\d+'),
        ('TIME', r'\d{1,2}:\d{2} (AM|PM)'),
        ('TIME_INTERVAL', r'\d+ (seconds|minutes|hours)'),
        ('THEN', r'then'),
        ('FROM', r'from'),
        ('TO', r'to'),
        ('DETECTED', r'detected'),
        ('TRIGGERED', r'triggered'),
        ('AT', r'at'),
        ('EVERY', r'every'),
        ('MISC', r'\S+')
    ]
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
    for match in re.finditer(tok_regex, command):
        kind = match.lastgroup
        value = match.group(kind)
        tokens.append((kind, value))
    return tokens

def validate(tokens):
    if not tokens:
        return "Syntax error in command."
    
    first_token = tokens[0][1]
    
    if first_token == 'on':
        if len(tokens) == 6 and tokens[1][0] == 'SENSOR' and tokens[2][0] in ['DETECTED', 'TRIGGERED'] and tokens[3][0] == 'THEN' and tokens[4][0] == 'OPERATION' and tokens[5][0] == 'DEVICE':
            return "Valid command."
    elif first_token == 'schedule':
        if len(tokens) == 5 and tokens[1][0] == 'OPERATION' and tokens[2][0] == 'DEVICE' and tokens[3][0] == 'AT' and tokens[4][0] == 'TIME':
            return "Valid command."
    elif first_token == 'if':
        if len(tokens) == 7 and tokens[1][0] == 'SENSOR' and tokens[2][0] == 'OPERATOR' and tokens[3][0] == 'VALUE' and tokens[4][0] == 'THEN' and tokens[5][0] == 'OPERATION' and tokens[6][0] == 'DEVICE':
            return "Valid command."
    elif first_token == 'repeat':
        if len(tokens) == 5 and tokens[1][0] == 'OPERATION' and tokens[2][0] == 'DEVICE' and tokens[3][0] == 'EVERY' and tokens[4][0] == 'TIME_INTERVAL':
            return "Valid command."
    elif first_token == 'activate':
        if len(tokens) == 6 and tokens[1][0] == 'MODE' and tokens[2][0] == 'FROM' and tokens[3][0] == 'TIME' and tokens[4][0] == 'TO' and tokens[5][0] == 'TIME':
            return "Valid command."
    
    return "Syntax error in command."

def process_command(command):
    tokens = tokenize(command)
    validation = validate(tokens)
    return tokens, validation

# Example test cases
test_cases = [
    "on motion detected then turn on lights",
    "schedule turn on watering at 6:00 AM",
    "if temperature > 30 then start AC",
    "repeat check temperature every 10 minutes",
    "activate night mode from 10:00 PM to 6:00 AM"
]

for command in test_cases:
    tokens, validation = process_command(command)
    print(f"Command: {command}")
    print(f"Tokens: {tokens}")
    print(f"Validation: {validation}\n")
