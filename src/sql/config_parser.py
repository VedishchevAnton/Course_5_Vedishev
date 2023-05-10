from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """
    Читает конфигурационный файл и возвращает параметры подключения к базе данных.
    :param filename: имя файла конфигурации (по умолчанию "database.ini")
    :param section: секция с параметрами подключения в файле конфигурации (по умолчанию "postgresql")
    :return: словарь с параметрами подключения к базе данных
    :raises Exception: если указанная секция не найдена в файле конфигурации
    """

    # Создаем парсер
    parser = ConfigParser()
    # Читаем файл конфигурации
    parser.read(filename)
    db = {}
    # Проверяем наличие указанной секции в файле конфигурации
    if parser.has_section(section):
        params = parser.items(section)  # Извлекаем параметры подключения из секции
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


# print(config())
