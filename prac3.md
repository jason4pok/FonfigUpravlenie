## Задача 1

Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

```
local parse_bnf(text) = {
  grammar: {},
  rules: [line.split('=') for line in std.strip(text).split('\n')],
  for name, body in rules:
    grammar[std.strip(name)] = [alt.split() for alt in body.split('|')],
  grammar
};

local generate_phrase(grammar, start) =
  if std.objectHas(grammar, start) then
    local seq = std.nth(grammar[start], 0);  // Используем первый элемент для простоты
    std.join([generate_phrase(grammar, name) for name in seq])
  else
    start;

local BNF = '''
E = a
''';

local grammar = parse_bnf(BNF);

local phrases = [
  generate_phrase(grammar, 'E')
  for i in std.range(0, 9)
];

{
  phrases: phrases
}
```

вывод программы: 

```
{
   "groups": [
      "ИКБО-1-20",
      "ИКБО-2-20",
      "ИКБО-3-20",
      "ИКБО-4-20",
      "ИКБО-5-20",
      "ИКБО-6-20",
      "ИКБО-7-20",
      "ИКБО-8-20",
      "ИКБО-9-20",
      "ИКБО-10-20",
      "ИКБО-11-20",
      "ИКБО-12-20",
      "ИКБО-13-20",
      "ИКБО-14-20",
      "ИКБО-15-20",
      "ИКБО-16-20",
      "ИКБО-17-20",
      "ИКБО-18-20",
      "ИКБО-19-20",
      "ИКБО-20-20",
      "ИКБО-21-20",
      "ИКБО-22-20",
      "ИКБО-23-20",
      "ИКБО-24-20"
   ],
   "students": [
      {
         "age": 19,
         "group": "ИКБО-4-20",
         "name": "Иванов И.И."
      },
      {
         "age": 18,
         "group": "ИКБО-5-20",
         "name": "Петров П.П."
      },
      {
         "age": 18,
         "group": "ИКБО-5-20",
         "name": "Сидоров С.С."
      },
      {
         "age": 18,
         "group": "ИКБО-23-20",
         "name": "Попов А.В."
      }
   ],
   "subject": "Конфигурационное управление"
}
```


## Задача 2

Реализовать на Dhall приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

```
let prefix = "ИКБО-"
let suffix = "-20"

let range = [1..24]

let groups =
  range : List Natural
    # List/map Natural Text (λ(n : Natural) → "${prefix}${Natural/show n}${suffix}") range

let students =
  [ { age = 19, group = "ИКБО-4-20", name = "Иванов И.И." }
  , { age = 18, group = "ИКБО-5-20", name = "Петров П.П." }
  , { age = 18, group = "ИКБО-5-20", name = "Сидоров С.С." }
  , { age = 20, group = "ИКБО-6-20", name = "Ваши Ф.И." }  -- Ваши данные
  ]

let subject = "Конфигурационное управление"

in  { groups = groups
    , students = students
    , subject = subject
    }
```

Реализовать грамматики, описывающие следующие языки (для каждого решения привести БНФ). Код решения должен содержаться в переменной bnf_text.

## Задача 3

Язык нулей и единиц.

```
bnf_text = '''
E = E 0 | E 1 | 0 | 1
'''
```

вывод программы:

```
011
110
0
01
00
11101
10
001
11
```

