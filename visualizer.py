import os#предоставляет функции для работы с файловой системой и окружением
import sys#работа с интерпретатором Python


class ConfigError(Exception):  # кастомное исключение для ошибок конфигурации
    pass


class JSONParser:
    @staticmethod
    def parse(json_string):  # основной метод парсинга json
        json_string = json_string.strip()  # удаляем пробелы по краям

        if not json_string.startswith('{') or not json_string.endswith('}'):  # проверка формата json
            raise ConfigError("невалидный json: должен начинаться с { и заканчиваться }")

        content = json_string[1:-1].strip()  # извлечение содержимого без фигурных скобок

        if not content:  # обработка пустого объекта
            return {}

        result = {}
        pairs = JSONParser._split_pairs(content)  # разделение на пары ключ-значение

        for pair in pairs:  # обработка каждой пары ключ-значение
            key, value = JSONParser._parse_pair(pair)  # парсинг каждой пары
            result[key] = value

        return result

    @staticmethod
    def _split_pairs(content):  # разделение содержимого на отдельные пары
        pairs = []
        current = ""  # текущая накапливаемая пара
        brace_count = 0  # счетчик вложенных объектов
        in_string = False  # флаг нахождения внутри строки
        escape = False  # флаг экранирования

        for char in content:  # обработка каждого символа
            if escape:  # обработка экранированных символов
                current += char
                escape = False
            elif char == '\\':  # начало экранирования
                current += char
                escape = True
            elif char == '"':  # переключение флага строки
                in_string = not in_string
                current += char
            elif char == '{':  # увеличение вложенности
                brace_count += 1
                current += char
            elif char == '}':  # уменьшение вложенности
                brace_count -= 1
                current += char
            elif char == ',' and brace_count == 0 and not in_string:  # разделитель пар
                pairs.append(current.strip())  # добавляем готовую пару
                current = ""  # сбрасываем текущую пару
            else:  # обычный символ
                current += char

        if current.strip():  # добавление последней пары
            pairs.append(current.strip())

        return pairs

    @staticmethod
    def _parse_pair(pair):  # парсинг одной пары ключ-значение
        parts = pair.split(':', 1)  # разделяем по первому двоеточию
        if len(parts) != 2:  # проверяем формат пары
            raise ConfigError(f"невалидная пара: {pair}")

        key = JSONParser._parse_string(parts[0].strip())  # парсим ключ
        value = JSONParser._parse_value(parts[1].strip())  # парсим значение

        return key, value

    @staticmethod
    def _parse_string(str_value):  # парсинг строкового значения
        if not str_value.startswith('"') or not str_value.endswith('"'):  # проверка кавычек
            raise ConfigError(f"строка должна быть в кавычках: {str_value}")

        return str_value[1:-1]  # возвращаем строку без кавычек

    @staticmethod
    def _parse_value(value):  # парсинг значения любого типа
        if value.startswith('"'):  # строковый тип
            return JSONParser._parse_string(value)
        elif value.lower() == 'true':  # булево true
            return True
        elif value.lower() == 'false':  # булево false
            return False
        elif value.lower() == 'null':  # null значение
            return None
        elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):  # целое число
            return int(value)
        else:  # попытка парсинга float
            try:
                return float(value)
            except:  # неподдерживаемый тип
                raise ConfigError(f"неподдерживаемый тип значения: {value}")


class DependencyVisualizer:
    def __init__(self, config_file: str = "config.json"):  # инициализация визуализатора
        self.config_file = config_file  # путь к файлу конфигурации
        self.config = {}  # словарь для хранения конфигурации

    def load_config(self) -> None:  # загрузка конфигурации из файла
        try:
            if not os.path.exists(self.config_file):  # проверка существования файла
                raise ConfigError(f"конфигурационный файл '{self.config_file}' не найден")

            with open(self.config_file, 'r', encoding='utf-8') as f:  # открытие файла
                file_content = f.read()  # чтение содержимого
                self.config = JSONParser.parse(file_content)  # парсинг json

        except ConfigError as e:  # перехват ошибок конфигурации
            raise e
        except Exception as e:  # перехват прочих ошибок
            raise ConfigError(f"ошибка чтения файла конфигурации: {e}")

    def validate_config(self) -> None:  # валидация параметров конфигурации
        required_fields = [  # список обязательных полей
            'package_name',
            'repository_url',
            'test_repository_mode',
            'package_version',
            'output_filename',
            'max_dependency_depth'
        ]

        for field in required_fields:  # проверка наличия обязательных полей
            if field not in self.config:
                raise ConfigError(f"обязательное поле '{field}' отсутствует в конфигурации")

        if not isinstance(self.config['package_name'], str):  # проверка типа package_name
            raise ConfigError("параметр 'package_name' должен быть строкой")

        if not isinstance(self.config['repository_url'], str):  # проверка типа repository_url
            raise ConfigError("параметр 'repository_url' должен быть строкой")

        if not isinstance(self.config['test_repository_mode'], bool):  # проверка типа test_repository_mode
            raise ConfigError("параметр 'test_repository_mode' должен быть булевым значением")

        if not isinstance(self.config['package_version'], str):  # проверка типа package_version
            raise ConfigError("параметр 'package_version' должен быть строкой")

        if not isinstance(self.config['output_filename'], str):  # проверка типа output_filename
            raise ConfigError("параметр 'output_filename' должен быть строкой")

        if not isinstance(self.config['max_dependency_depth'], int):  # проверка типа max_dependency_depth
            raise ConfigError("параметр 'max_dependency_depth' должен быть целым числом")

        if self.config['max_dependency_depth'] < 0:  # проверка диапазона max_dependency_depth
            raise ConfigError("параметр 'max_dependency_depth' не может быть отрицательным")

        if not self.config['package_name'].strip():  # проверка пустого package_name
            raise ConfigError("параметр 'package_name' не может быть пустым")

        if not self.config['output_filename'].strip():  # проверка пустого output_filename
            raise ConfigError("параметр 'output_filename' не может быть пустым")

    def display_config(self) -> None:  # отображение текущей конфигурации
        print("=== параметры конфигурации ===")  # заголовок
        for key, value in self.config.items():  # перебор всех параметров
            print(f"{key}: {value}")  # вывод ключ-значение
        print("===============================")  # завершающая линия

    def run(self) -> None:  # основной метод запуска
        try:
            print("загрузка конфигурации...")  # информационное сообщение
            self.load_config()  # загрузка конфигурации

            print("валидация параметров...")  # информационное сообщение
            self.validate_config()  # валидация параметров

            print("конфигурация успешно загружена и проверена!")  # сообщение об успехе
            self.display_config()  # отображение конфигурации

            print("\nготово! на следующем этапе будет реализован анализ зависимостей.")  # планы на будущее

        except ConfigError as e:  # обработка ошибок конфигурации
            print(f"ошибка конфигурации: {e}", file=sys.stderr)  # вывод в stderr
            sys.exit(1)  # завершение с ошибкой
        except Exception as e:  # обработка неожиданных ошибок
            print(f"неожиданная ошибка: {e}", file=sys.stderr)  # вывод в stderr
            sys.exit(1)  # завершение с ошибкой


def main():  # главная функция
    config_file = "config.json"  # значение по умолчанию

    if len(sys.argv) > 1:  # проверка аргументов командной строки
        if sys.argv[1] in ['--config', '-c'] and len(sys.argv) > 2:  # обработка флагов --config/-c
            config_file = sys.argv[2]  # установка пути из аргумента
        elif sys.argv[1].endswith('.json'):  # обработка прямого указания json-файла
            config_file = sys.argv[1]  # установка пути из аргумента

    visualizer = DependencyVisualizer(config_file)  # создание экземпляра визуализатора
    visualizer.run()  # запуск визуализатора


if __name__ == "__main__":  # точка входа
    main()  # вызов главной функции