
operators = {
  '+': (1, lambda x, y: x + y),
  '-': (1, lambda x, y: x - y),
  '*': (2, lambda x, y: x * y),
  '/': (2, lambda x, y: x / y),
}


def check_lexeme(char):
  if char.isdigit() or char == '.':
    return 'digit'
  elif char == '(':
    return 'open_bracket'
  elif char == ')':
    return 'close_bracket'
  elif char in operators:
    return 'operator'
  else:
    return 'error'


def grade(operator):
  return operators[operator][0]


def eval(operator, x, y):
  return operators[operator][1](x, y)


def sorting_yard(exp):
  result_stack = []
  oper_stack = []
  last_type = ''

  for lexeme in exp:
    type = check_lexeme(lexeme)
    
    if type == 'error':
      raise ValueError('Symbol error: ' + lexeme)
    
    if type == 'digit':
      if last_type == 'digit':
        result_stack[-1]['value'] += lexeme
      else:
        result_stack.append(
          {
            'type': type,
            'value': lexeme,
          }
        )

    elif type == 'open_bracket':
      oper_stack.append(lexeme)

    elif type == 'close_bracket':
      while oper_stack:
        operator = oper_stack.pop()
        if operator == '(':
          break
        else:
          result_stack.append(
            {
              'type': 'operator',
              'value': operator,
            }
          )

    elif type == 'operator':
      if (lexeme == '-' or lexeme == '+') \
        and (not result_stack \
            or (last_type == 'operator' \
                or last_type == 'open_bracket') \
         ):
        type = 'digit'
        result_stack.append(
          {
            'type': 'digit',
            'value': lexeme,
          }
        )
      else:
        if oper_stack \
          and (oper_stack[-1] in operators) \
          and (grade(lexeme) <= grade(oper_stack[-1])):
          result_stack.append(
            {
              'type': 'operator',
              'value': oper_stack.pop(),
            }
          )
        oper_stack.append(lexeme)
    
    last_type = type

  while oper_stack:
    result_stack.append(
      {
        'type': 'operator',
        'value': oper_stack.pop(),
      }
    )

  return result_stack


def polish_repr(data):
  tokens = []
  for el in data:
    tokens.append(el['value'])
  return ' '.join(tokens)

def calc(stack):
  buff_stack = []
  for token in stack:
    if token['type'] == 'operator':
      if len(buff_stack) < 2:
        raise ValueError('Formula incorrect')
      y, x = buff_stack.pop(), buff_stack.pop()
      buff_stack.append(eval(token['value'], x, y))
    else:
      buff_stack.append(float(token['value']))
  return buff_stack[0]


exp = input()
exp = exp.replace(' ', '')

try:
  exp_stack = sorting_yard(exp)
  print(polish_repr(exp_stack))
  result = calc(exp_stack)
  print(result)
except ValueError as err:
  print(err)
