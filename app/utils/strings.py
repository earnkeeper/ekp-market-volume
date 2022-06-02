import re

pattern1 = re.compile(r'(.)([A-Z][a-z]+)')
pattern2 = re.compile(r'([a-z0-9])([A-Z])')

def title_to_kebab(name):
    name = pattern1.sub(r'\1-\2', name)
    return pattern2.sub(r'\1-\2', name).lower()