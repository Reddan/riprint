from termcolor import colored

def _riprint(value, color, indent=0):
  indent_str = '  ' * indent
  next_indent_str = indent_str + '  '
  if isinstance(value, (int, float)):
    return colored(value, color or 'yellow')
  elif isinstance(value, str):
    return colored(f"'{value}'", color or 'green')
  elif isinstance(value, tuple):
    child_str = ', '.join([_riprint(val, color, indent) for val in value])
    return f"({child_str})"
  elif isinstance(value, list):
    children = [_riprint(val, color, indent + 1) for val in value]
    cand_text = ', '.join(children)
    if len(cand_text) <= 80 and '\n' not in cand_text:
      return f"[{cand_text}]"
    else:
      children = [next_indent_str + child for child in children]
      child_str = ',\n'.join(children)
      return f"[\n{child_str}\n{indent_str}]"
  elif isinstance(value, dict):
    children = [next_indent_str + _riprint(key, color) + ': ' + _riprint(val, color, indent + 1) for key, val in value.items()]
    child_str = ',\n'.join(children)
    return f"{{\n{child_str}\n{indent_str}}}"
  return value

def riprint(*values, color=None):
  print(*(_riprint(value, color) for value in values))
