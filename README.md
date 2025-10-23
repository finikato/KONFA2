<pre>
  Григорьев Кирилл Алексеевич ИКБО-24-24
  Вариант 7
  Минимальный прототип CLI-приложения с конфигурацией
  этап 2.1
  1)Реализована загрузка конфигурации из JSON файлов
  2)Добавлена проверка на соответсвие(валидация) требованиям всех параметров конфигурации
  3)Реализован вывод параметров в формате ключ-значение
  4)Добавлена обработка ошибок для всех параметров
  5)Создана базовая структура приложения с CLI интерфейсом
  
  Тест 1: Успешный запуск
  python dependency_visualizer.py --config config.json

  Тест 2: Файл не существует
  python dependency_visualizer.py --config missing.json

  Тест 3: Невалидный JSON
  python dependency_visualizer.py --config bad_config.json

  Тест 4: Отсутствуют обязательные поля
  python dependency_visualizer.py --config incomplete.json

  Тест 5: Неправильные типы данных
  python dependency_visualizer.py --config wrong_types.json
</pre>
