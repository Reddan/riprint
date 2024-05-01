import numpy as np
import shutil
from termcolor import colored

dict_values = type({}.values())
dict_keys = type({}.keys())
list_types = (list, dict_values, dict_keys)

bracket_colors = [
  None,
  'red',
  'blue',
  'magenta',
  'cyan',
  'grey',
]

def get_terminal_width():
  return shutil.get_terminal_size((80, 0))[0]

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
      return colored(f'"{value}"', color or 'green')
  elif isinstance(value, (tuple, set, list_types)):
    open_bracket = colored('[' if isinstance(value, list_types) else '(' if isinstance(value, tuple) else '{', bracket_color)
    close_bracket = colored(']' if isinstance(value, list_types) else ')' if isinstance(value, tuple) else '}', bracket_color)
    children = [_riprint(val, color, indent + 1) for val in value]
    child_str = ', '.join(children)
    terminal_width = get_terminal_width()
    if len(child_str) <= terminal_width and '\n' not in child_str:
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
    child_str = child_str and f"\n{child_str}\n{indent_str}"
    return f"{open_bracket}{child_str}{close_bracket}"
  elif isinstance(value, np.ndarray):
    array_lines = np.array2string(
      value,
      max_line_width=get_terminal_width(),
      edgeitems=5,
    ).splitlines()
    if len(array_lines) == 1:
      return array_lines[0]
    else:
      array_lines[0] = ' ' + array_lines[0][1:]
      array_lines[-1] = array_lines[-1][:-1]
      array_lines = [next_indent_str + line for line in array_lines]
      array_str = '\n'.join(array_lines)
      return f"ndarray [\n{array_str}\n{indent_str}]"
  return str(value)

def riprint(*values, color=None, print=print, **kwargs):
  print(*(_riprint(value, color) for value in values), **kwargs)

print = riprint
