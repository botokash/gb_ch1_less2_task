
operators = {
  '+': (1, lambda x, y: x + y),
  '-': (1, lambda x, y: x - y),
  '*': (2, lambda x, y: x * y),
  '/': (2, lambda x, y: x / y),
}


def check_unary(token):
  if token.isdigit() or \
    token == ')':
    return False
  else:
    return True


def grade(operator):
  return operators[operator][0]


def eval(operator, x, y):
  return operators[operator][1](x, y)


def sorting_yard(exp):
  result = []
  stack = []
  sign = ''
  unary = True
  for token in exp:
    if token.isdigit():
      result.append(sign + token)
      sign = ''
    elif token == '(':
      stack.append(token)
    elif token == ')':
      while stack:
        operator = stack.pop()
        if operator == '(':
          break
        else:
          result.append(operator)
    elif token in operators:
      if unary and \
        (token == '-' or token == '+'):
        sign = token
      else:
        if stack and \
          (stack[-1] in operators) and \
          (grade(token) <= grade(stack[-1])):
          result.append(stack.pop())
        stack.append(token)
        sign = ''
    unary = check_unary(token)
  while stack:
    result.append(stack.pop())
  return result


def calc(polish):
  stack = []
  for token in polish:
    if token in operators:
      y, x = stack.pop(), stack.pop()
      stack.append(eval(token, x, y))
    else:
      stack.append(int(token))
  return stack[0]


exp = input()
polish = sorting_yard(exp)
print(''.join(polish))
result = calc(polish)
print(result)
