import re

# Define token patterns
TOKEN_PATTERNS = {
    "EVENT": r"on|schedule|if|repeat|activate",
    "SENSOR": r"motion|temperature|humidity|door|light|sound",
    "DEVICE": r"lights|AC|fan|door|alarm|sprinkler|watering",
    "OPERATION": r"turn on|turn off|increase|decrease|open|close|start|check",
    "MODE": r"night mode|vacation mode|silent mode",
    "TIME": r"\d{1,2}:\d{2} (AM|PM)",
    "TIME_INTERVAL": r"\d+ (seconds|minutes|hours)",
    "NUMBER": r"\d+",
    "OPERATOR": r">|<|>=|<=|==",
    "THEN": r"then",
    "FROM_TO": r"from|to"
}

# Combine token patterns
TOKEN_REGEX = re.compile(
    "|".join(f"(?P<{key}>{pattern})" for key, pattern in TOKEN_PATTERNS.items()), re.IGNORECASE
)

# Tokenizer function
def tokenize(command):
    tokens = []
    for match in TOKEN_REGEX.finditer(command):
        token_type = match.lastgroup
        value = match.group(token_type)
        tokens.append((token_type, value))
    return tokens

# Syntax validation function
def validate_syntax(tokens):
    if not tokens:
        return False, "Empty command."
    
    first_token = tokens[0][1]
    if first_token == "on":
        return validate_event(tokens)
    elif first_token == "schedule":
        return validate_schedule(tokens)
    elif first_token == "if":
        return validate_condition(tokens)
    elif first_token == "repeat":
        return validate_loop(tokens)
    elif first_token == "activate":
        return validate_mode(tokens)
    else:
        return False, "Invalid command start."

# Specific validation functions
def validate_event(tokens):
    pattern = ["EVENT", "SENSOR", "detected", "THEN", "OPERATION", "DEVICE"]
    return match_pattern(tokens, pattern)

def validate_schedule(tokens):
    pattern = ["EVENT", "OPERATION", "DEVICE", "at", "TIME"]
    return match_pattern(tokens, pattern)

def validate_condition(tokens):
    pattern = ["EVENT", "SENSOR", "OPERATOR", "NUMBER", "THEN", "OPERATION", "DEVICE"]
    return match_pattern(tokens, pattern)

def validate_loop(tokens):
    pattern = ["EVENT", "OPERATION", "SENSOR", "every", "TIME_INTERVAL"]
    return match_pattern(tokens, pattern)

def validate_mode(tokens):
    pattern = ["EVENT", "MODE", "FROM_TO", "TIME", "FROM_TO", "TIME"]
    return match_pattern(tokens, pattern)

def match_pattern(tokens, expected_pattern):
    extracted_types = [t[0] for t in tokens]
    if extracted_types[:len(expected_pattern)] == expected_pattern:
        return True, "Valid command."
    return False, "Syntax error in command."

# Example test cases
commands = [
    "on motion detected then turn on lights",
    "schedule turn on watering at 6:00 AM",
    "if temperature > 30 then turn on AC",
    "repeat check temperature every 10 minutes",
    "activate night mode from 10:00 PM to 6:00 AM"
]

for cmd in commands:
    tokens = tokenize(cmd)
    valid, message = validate_syntax(tokens)
    print(f"Command: {cmd}\nTokens: {tokens}\nValidation: {message}\n")
