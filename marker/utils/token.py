import os
from . import CONFIG_DIR, ensure_config_dir
import json

class TokenNotFoundError(Exception):
    pass

TOKENS_PATH = os.path.join(CONFIG_DIR, "tokens.json")

def load_tokens_dict():
    if not os.path.isfile(TOKENS_PATH):
        return {}
    with open(TOKENS_PATH) as file:
        return json.load(file)

def save_token(lms, identifier, token):
    ensure_config_dir()
    tokens = load_tokens_dict()
    if lms not in tokens:
        tokens[lms] = {}
    tokens[lms][identifier] = token
    with open(TOKENS_PATH, "w") as file:
        json.dump(tokens, file, indent=2)

def get_token(lms, identifier):
    tokens = load_tokens_dict()
    if lms not in tokens or identifier not in tokens[lms]:
        raise Exception("Token not found")
    return tokens[lms][identifier]

def get_or_prompt_token(console, lms, identifier):
    try:
        return get_token(lms, identifier)
    except BaseException as e:
        pass
    token = console.get(f"Enter {lms} token")
    if token is None or token == "":
        raise TokenNotFoundError(f"Couldn't get token for {lms}:{identifier}")

    token = token.strip()
    save = console.ask(f"Save token [red]{TOKENS_PATH}[/red]?", default=True)
    if save:
        save_token(lms, identifier, token)
    return token