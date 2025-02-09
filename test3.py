import re

# Token specifications (updated to match BNF)
token_specs = [
    ('MODE', r'\b(night mode|vacation mode|silent mode)\b'),
    ('KEYWORD', r'\b(on|then|schedule|at|if|repeat|every|activate|from|to)\b'),
    ('SENSOR', r'\b(motion|temperature|humidity|door|light|sound)\b'),
    ('DEVICE', r'\b(lights|AC|fan|door|alarm|sprinkler)\b'),
    ('OPERATION', r'\b(on|off|increase|decrease|open|close)\b'),
    ('OPERATOR', r'>=|<=|==|>|<'),
    ('TIME_INTERVAL', r'\b\d+\s(seconds|minutes|hours)\b'),
    ('TIME', r'\b(0?[1-9]|1[0-2]):[0-5][0-9]\s(AM|PM)\b'),
    ('NUMBER', r'\b\d+\b'),
    ('EVENT_TRIGGER', r'\b(detected|triggered)\b'),
    ('SEMICOLON', r';'),
    ('SKIP', r'\s+'),
    ('ERROR', r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)

def lex(input_str):
    tokens = []
    for match in re.finditer(tok_regex, input_str, re.IGNORECASE):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        elif kind == 'ERROR':
            raise SyntaxError(f'Invalid token: {value}')
        else:
            tokens.append((kind, value))
    return tokens

def validate_syntax(tokens):
    try:
        ptr = 0
        while ptr < len(tokens):
            current_token = tokens[ptr][0]
            
            # Event Command
            if current_token == 'KEYWORD' and tokens[ptr][1].lower() == 'on':
                if (ptr+3 < len(tokens) and 
                    tokens[ptr+1][0] == 'SENSOR' and
                    tokens[ptr+2][0] == 'EVENT_TRIGGER' and
                    tokens[ptr+3][0] == 'KEYWORD' and tokens[ptr+3][1] == 'then'):
                    ptr += 4
                    if ptr >= len(tokens) or (tokens[ptr][0] not in ['DEVICE', 'OPERATION']):
                        return False
                else:
                    return False
            
            # Schedule Command
            elif current_token == 'KEYWORD' and tokens[ptr][1].lower() == 'schedule':
                if (ptr+3 < len(tokens) and 
                    tokens[ptr+1][0] == 'DEVICE' and
                    tokens[ptr+2][0] == 'KEYWORD' and tokens[ptr+2][1] == 'at' and
                    tokens[ptr+3][0] == 'TIME'):
                    ptr += 4
                else:
                    return False
            
            # Conditional Command
            elif current_token == 'KEYWORD' and tokens[ptr][1].lower() == 'if':
                if (ptr+5 < len(tokens) and 
                    tokens[ptr+1][0] == 'SENSOR' and
                    tokens[ptr+2][0] == 'OPERATOR' and
                    tokens[ptr+3][0] == 'NUMBER' and
                    tokens[ptr+4][0] == 'KEYWORD' and tokens[ptr+4][1] == 'then' and
                    tokens[ptr+5][0] == 'DEVICE' and 
                    tokens[ptr+6][0] == 'OPERATION'):
                    ptr += 7
                else:
                    return False
            
            # Mode Command
            elif current_token == 'KEYWORD' and tokens[ptr][1].lower() == 'activate':
                if (ptr+5 < len(tokens) and 
                    tokens[ptr+1][0] == 'MODE' and
                    tokens[ptr+2][0] == 'KEYWORD' and tokens[ptr+2][1] == 'from' and
                    tokens[ptr+3][0] == 'TIME' and
                    tokens[ptr+4][0] == 'KEYWORD' and tokens[ptr+4][1] == 'to' and
                    tokens[ptr+5][0] == 'TIME'):
                    ptr += 6
                else:
                    return False
            
            else:
                return False
        return True
    except:
        return False

# Test case processing
test_cases = [
    "on motion detected then turn on lights",
    "schedule turn on watering at 6:00 AM",
    "if temperature > 30 then turn on AC",
    "repeat check temperature every 10 minutes",
    "activate night mode from 10:00 PM to 6:00 AM"
]

for cmd in test_cases:
    try:
        tokens = lex(cmd)
        is_valid = validate_syntax(tokens)
        print(f"Command: {cmd}")
        print(f"Tokens: {tokens}")
        print(f"Validation: {'Valid command' if is_valid else 'Syntax error in command.'}\n")
    except SyntaxError as e:
        print(f"Command: {cmd}")
        print(f"Error: {e}\n")