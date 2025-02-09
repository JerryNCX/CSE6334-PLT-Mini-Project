import re

# Token specifications in order of priority
token_specs = [
    ('MODE', r'\b(night mode|vacation mode|silent mode)\b'),
    ('KEYWORD', r'\b(on|then|schedule|at|if|repeat|every|activate|from|to)\b'),
    ('SENSOR', r'\b(motion|temperature|humidity|door|light|sound)\b'),
    ('DEVICE', r'\b(lights|AC|fan|door|alarm|sprinkler)\b'),
    ('OPERATION', r'\b(off|increase|decrease|open|close)\b'),  # "on" is excluded due to conflict
    ('OPERATOR', r'>=|<=|==|>|<'),
    ('TIME_INTERVAL', r'\b\d+\s(seconds|minutes|hours)\b'),
    ('TIME', r'\b(0?[1-9]|1[0-2]):[0-5][0-9]\s(AM|PM)\b'),
    ('NUMBER', r'\b\d+\b'),
    ('EVENT_TRIGGER', r'\b(detected|triggered)\b'),
    ('SEMICOLON', r';'),
    ('SKIP', r'\s+'),
    ('ERROR', r'.'),
]

# Build the regex pattern
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
            # Handle "on" as OPERATION if preceded by a DEVICE
            if kind == 'KEYWORD' and value.lower() == 'on' and tokens and tokens[-1][0] == 'DEVICE':
                tokens.append(('OPERATION', value))
            else:
                tokens.append((kind, value))
    return tokens

# Example usage
if __name__ == "__main__":
    test_command = "on motion detected then lights on"
    try:
        tokens = lex(test_command)
        for token in tokens:
            print(token)
    except SyntaxError as e:
        print(e)