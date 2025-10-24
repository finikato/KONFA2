import sys#импорт системных функций
import os#импорт функций операционной системы

class Config:#класс для работы с конфигурацией
    def __init__(self):#конструктор класса
        self.params = {}#словарь для хранения параметров
    
    def load(self, path="config.json"):#метод загрузки конфигурации
        if not os.path.exists(path):#проверка существования файла
            raise Exception(f"файл не найден: {path}")#ошибка если файл не найден
        
        with open(path, 'r') as f:#открытие файла для чтения
            content = f.read().strip()#чтение содержимого и удаление пробелов
        
        if not content.startswith('{') or not content.endswith('}'):#проверка формата json
            raise Exception("неправильный json format")#ошибка если не json
        
        pairs = content[1:-1].strip().split(',')#разделение на пары ключ-значение
        for pair in pairs:#перебор всех пар
            if ':' not in pair: continue#пропуск некорректных пар
            key, value = pair.split(':', 1)#разделение на ключ и значение
            key = key.strip().strip('"')#очистка ключа
            value = value.strip().strip('"')#очистка значения
            
            if value.isdigit(): #проверка на целое число
                value = int(value)#преобразование в целое число
            elif value.lower() == 'true': #проверка на true
                value = True#преобразование в булево true
            elif value.lower() == 'false': #проверка на false
                value = False#преобразование в булево false
            elif value.replace('.', '').replace('-', '').isdigit() and value.count('.') <= 1 and value.count('-') <= 1:#проверка на вещественное число
                try: value = float(value)#преобразование в вещественное число
                except: pass#игнорирование ошибок
            
            self.params[key] = value#добавление параметра в словарь
        
        required = ['package_name', 'repository_url', 'test_repository_mode', #список обязательных полей
                   'package_version', 'output_filename', 'max_dependency_depth']
        for field in required:#проверка обязательных полей
            if field not in self.params:#если поле отсутствует
                raise Exception(f"поле не найдено: {field}")#ошибка отсутствия поля
        
        #валидация значений
        if not self.params['package_name'] or not isinstance(self.params['package_name'], str):#проверка имени пакета
            raise Exception("package_name должен быть не пустой строкой")#ошибка если пустое или не строка
        if not isinstance(self.params['repository_url'], str):#проверка url репозитория
            raise Exception("repository_url должен быть строкой")#ошибка если не строка
        if not isinstance(self.params['test_repository_mode'], bool):#проверка режима тестирования
            raise Exception("test_repository_mode должен быть булевым (true/false)")#ошибка если не булево значение
        if not isinstance(self.params['package_version'], str):#проверка версии пакета
            raise Exception("package_version должен быть строкой")#ошибка если не строка
        if not self.params['output_filename'] or not isinstance(self.params['output_filename'], str):#проверка имени файла вывода
            raise Exception("output_filename должен быть не пустой строкой")#ошибка если пустое или не строка
        if not isinstance(self.params['max_dependency_depth'], int) or self.params['max_dependency_depth'] < 0:#проверка глубины зависимостей
            raise Exception("max_dependency_depth должен быть целым положительным")#ошибка если не целое или отрицательное

def main():#главная функция
    if len(sys.argv) > 2 and sys.argv[1] in ['--config', '-c']:#проверка аргументов командной строки
        config_file = sys.argv[2]#установка файла конфигурации из аргумента
    else:
        config_file = "config.json"#использование файла по умолчанию
    
    try:
        config = Config()#создание экземпляра конфигурации
        config.load(config_file)#загрузка конфигурации
        
        print("конфигурация параметров:")#вывод заголовка
        for key, value in config.params.items():#перебор всех параметров
            print(f"{key}: {value}")#вывод ключа и значения
            
    except Exception as e:#обработка исключений
        print(f"error: {e}")#вывод ошибки
        sys.exit(1)#завершение с кодом ошибки

if __name__ == "__main__":#точка входа в программу
    main()#вызов главной функци