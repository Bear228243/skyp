def read_json_file(file_path: str) -> List[Dict[str, Any]]: 
    """ 
    Читает JSON-файл и возвращает список словарей с данными о транзакциями. 

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список словарей с данными о транзакциях. 
        Если файл не найден, пустой или содержит не список, то возвращает пустой список.

    Raises:
        FileNotFoundError: Если файл не существует
        JSONDecodeError: Если файл содержит некорректный JSON
    """ 
    if not os.path.exists(file_path): 
        print(f"Файл {file_path} не найден") 
        return [] 

    try: 
        with open(file_path, 'r', encoding='utf-8') as file: 
            data = json.load(file) 

        if not isinstance(data, list): 
            print(f"Файл {file_path} не содержит список") 
            return [] 

        return data 

    except json.JSONDecodeError as e: 
        print(f"Ошибка декодирования JSON в файле {file_path}: {e}") 
        return [] 
    except Exception as e: 
        print(f"Неожиданная ошибка при чтении файла {file_path}: {e}") 
        return [] 