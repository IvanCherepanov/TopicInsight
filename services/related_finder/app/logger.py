# Настройка базовой конфигурации логирования
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Создание объекта логгера
logger = logging.getLogger(__name__)

# Добавление обработчика для записи логов в файл
file_handler = logging.FileHandler('my_app.log')  # Имя файла логов
file_handler.setLevel(logging.INFO)  # Уровень логирования для файла
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)