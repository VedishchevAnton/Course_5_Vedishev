from configparser import ConfigParser

user = "postgres"
password = "231287"


def config(filename="database.ini", section="postgresql"):
    """
    Функция для чтения конфигурационного файла и получения параметров подключения к базе данных.

    :param filename: имя файла конфигурации (по умолчанию "database.ini")
    :param section: секция с параметрами подключения (по умолчанию "postgresql")
    :return: словарь с параметрами подключения к базе данных
    :raises Exception: если секция с параметрами подключения не найдена в файле
    """
    # Создаем парсер
    parser = ConfigParser()
    # Читаем конфигурационный файл
    parser.read(filename)
    db = {}
    # Проверяем наличие секции с параметрами подключения
    if parser.has_section(section):
        params = parser.items(section)
        # Заполняем словарь параметрами подключения
        for param in params:
            db[param] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename)
        )
    return db


# # Пример работы функции
# params_test = config()
# print(params_test)
