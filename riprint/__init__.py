from termcolor import colored

bracket_colors = [
  'red',
  'green',
  'yellow',
  'blue',
  'magenta',
  'cyan',
]

def _riprint(value, color, indent=0):
  indent_str = '  ' * indent
  next_indent_str = indent_str + '  '
  bracket_color = color or bracket_colors[indent % len(bracket_colors)]
  if value is None:
    return colored(value, color, attrs=['bold'])
  elif isinstance(value, (int, float)):
    return colored(value, color or 'yellow')
  elif isinstance(value, str):
    if indent == 0:
      return colored(f"{value}", color)
    else:
      return colored(f"'{value}'", color or 'green')
  elif isinstance(value, (tuple, list, set)):
    open_bracket = colored('[' if isinstance(value, list) else '(' if isinstance(value, tuple) else '{', bracket_color)
    close_bracket = colored(']' if isinstance(value, list) else ')' if isinstance(value, tuple) else '}', bracket_color)
    children = [_riprint(val, color, indent + 1) for val in value]
    child_str = ', '.join(children)
    if len(child_str) <= 80 and '\n' not in child_str:
      return f"{open_bracket}{child_str}{close_bracket}"
    else:
      children = [next_indent_str + child for child in children]
      child_str = ',\n'.join(children)
      return f"{open_bracket}\n{child_str}\n{indent_str}{close_bracket}"
  elif isinstance(value, dict):
    open_bracket = colored('{', bracket_color)
    close_bracket = colored('}', bracket_color)
    children = [
      f"{next_indent_str}{_riprint(key, color, indent + 1)}: {_riprint(val, color, indent + 1)}"
      for key, val in value.items()
    ]
    child_str = ',\n'.join(children)
    return f"{open_bracket}\n{child_str}\n{indent_str}{close_bracket}"
  return str(value)

def riprint(*values, color=None, print=print, **kwargs):
  print(*(_riprint(value, color) for value in values), **kwargs)
