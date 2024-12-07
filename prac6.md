Практическое задание №6. Системы автоматизации сборки
П.Н. Советов, РТУ МИРЭА

Работа с утилитой Make.

Изучить основы языка утилиты make. Распаковать в созданный каталог make.zip, если у вас в в системе нет make.

Создать приведенный ниже Makefile и проверить его работоспособность.

```
dress: trousers shoes jacket
    @echo "All done. Let's go outside!"

jacket: pullover
    @echo "Putting on jacket."

pullover: shirt
    @echo "Putting on pullover."

shirt:
    @echo "Putting on shirt."

trousers: underpants
    @echo "Putting on trousers."

underpants:
    @echo "Putting on underpants."

shoes: socks
    @echo "Putting on shoes."

socks: pullover
    @echo "Putting on socks."
```

![image](https://github.com/user-attachments/assets/81eca60b-587d-448e-a942-c711df5193bb)

## Задача 1
Написать программу на Питоне, которая транслирует граф зависимостей civgraph в makefile в духе примера выше. Для мало знакомых с Питоном используется упрощенный вариант civgraph: civgraph.json.

Пример:
```
> make mathematics
mining
bronze_working
sailing
astrology
celestial_navigation
pottery
writing
code_of_laws
foreign_trade
currency
irrigation
masonry
early_empire
mysticism
drama_poetry
mathematics
```

![image](https://github.com/user-attachments/assets/a0ec8eb1-71be-487c-b733-65fcc1f17eaf)
![image](https://github.com/user-attachments/assets/9d898339-a52f-4fa0-a40e-ed5a79622a65)
![image](https://github.com/user-attachments/assets/6d2b8480-a1a0-4bc5-a141-246f421becc0)
