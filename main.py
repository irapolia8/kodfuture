import json
import os
import random
import string
from datetime import datetime
from typing import List, Optional


# ==================== МОДЕЛЬ ====================
class PasswordRecord:
    """Модель данных для записи пароля"""
    
    def __init__(self, service: str, username: str, password: str, created_at: Optional[str] = None):
        self.service = service
        self.username = username
        self.password = password
        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    def to_dict(self) -> dict:
        """Преобразование в словарь для JSON"""
        return {
            "service": self.service,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря"""
        return cls(
            service=data["service"],
            username=data["username"],
            password=data["password"],
            created_at=data.get("created_at")
        )
    
    def __str__(self) -> str:
        return f"Сервис: {self.service}\nЛогин: {self.username}\nПароль: {self.password}\nСоздано: {self.created_at}\n"


# ==================== ХРАНИЛИЩЕ ====================
class PasswordStorage:
    """Класс для работы с хранением данных"""
    
    def __init__(self, filename: str = "passwords.json"):
        self.filename = filename
        self.records: List[PasswordRecord] = []
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.records = [PasswordRecord.from_dict(item) for item in data]
            else:
                self.records = []
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            self.records = []
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            data = [record.to_dict() for record in self.records]
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
    
    def add_record(self, record: PasswordRecord):
        """Добавление новой записи"""
        if record is None:
            raise ValueError("Запись не может быть пустой")
        self.records.append(record)
        self.save_data()
    
    def get_all_records(self) -> List[PasswordRecord]:
        """Получение всех записей"""
        return self.records.copy()
    
    def delete_record(self, service: str) -> bool:
        """Удаление записи по названию сервиса"""
        for i, record in enumerate(self.records):
            if record.service.lower() == service.lower():
                self.records.pop(i)
                self.save_data()
                return True
        return False


# ==================== ГЕНЕРАТОР ПАРОЛЕЙ ====================
class PasswordGenerator:
    """Класс для генерации случайных паролей"""
    
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIAL_CHARS = "!@#$%^&*()_-+=<>?"
    
    @classmethod
    def generate(cls, length: int = 12, use_lowercase: bool = True, 
                 use_uppercase: bool = True, use_digits: bool = True, 
                 use_special: bool = True) -> str:
        """
        Генерация случайного пароля
        
        Args:
            length: Длина пароля
            use_lowercase: Использовать строчные буквы
            use_uppercase: Использовать заглавные буквы
            use_digits: Использовать цифры
            use_special: Использовать спецсимволы
        
        Returns:
            Сгенерированный пароль
        """
        if length <= 0:
            raise ValueError("Длина пароля должна быть больше 0")
        
        chars = ""
        if use_lowercase:
            chars += cls.LOWERCASE
        if use_uppercase:
            chars += cls.UPPERCASE
        if use_digits:
            chars += cls.DIGITS
        if use_special:
            chars += cls.SPECIAL_CHARS
        
        if not chars:
            raise ValueError("Должен быть выбран хотя бы один тип символов")
        
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
    
    @classmethod
    def generate_with_settings(cls) -> str:
        """Генерация пароля с настройками от пользователя"""
        try:
            length_input = input("Длина пароля (по умолчанию 12): ").strip()
            length = int(length_input) if length_input else 12
            
            use_lower = input("Использовать строчные буквы? (y/n, по умолчанию y): ").strip().lower() != 'n'
            use_upper = input("Использовать заглавные буквы? (y/n, по умолчанию y): ").strip().lower() != 'n'
            use_digits = input("Использовать цифры? (y/n, по умолчанию y): ").strip().lower() != 'n'
            use_special = input("Использовать спецсимволы? (y/n, по умолчанию y): ").strip().lower() != 'n'
            
            return cls.generate(length, use_lower, use_upper, use_digits, use_special)
        except ValueError as e:
            print(f"Ошибка: {e}")
            return cls.generate()  # Возвращаем пароль по умолчанию


# ==================== ПРЕДСТАВЛЕНИЕ ====================
class ConsoleView:
    """Класс для работы с консольным интерфейсом"""
    
    @staticmethod
    def show_menu():
        """Отображение главного меню"""
        print("\n" + "=" * 40)
        print("       PASSWORD MANAGER")
        print("=" * 40)
        print("  1. Добавить запись")
        print("  2. Просмотреть все записи")
        print("  3. Удалить запись")
        print("  4. Сгенерировать пароль")
        print("  5. Выход")
        print("=" * 40)
    
    @staticmethod
    def show_message(message: str, is_error: bool = False):
        """Отображение сообщения"""
        if is_error:
            print(f"\n❌ {message}")
        else:
            print(f"\n✅ {message}")
        input("\nНажмите Enter для продолжения...")
    
    @staticmethod
    def show_records(records: List[PasswordRecord]):
        """Отображение всех записей"""
        if not records:
            ConsoleView.show_message("Нет сохраненных записей", True)
            return
        
        print("\n" + "=" * 70)
        print("СОХРАНЕННЫЕ ПАРОЛИ".center(70))
        print("=" * 70)
        
        for i, record in enumerate(records, 1):
            print(f"\n📌 Запись #{i}")
            print("-" * 60)
            print(record)
            print("-" * 60)
        
        input("\nНажмите Enter для продолжения...")
    
    @staticmethod
    def get_record_input() -> Optional[PasswordRecord]:
        """Получение данных для новой записи"""
        print("\n" + "=" * 40)
        print("ДОБАВЛЕНИЕ ЗАПИСИ".center(40))
        print("=" * 40)
        
        service = input("Название сервиса: ").strip()
        if not service:
            return None
        
        username = input("Имя пользователя / Логин: ").strip()
        if not username:
            return None
        
        password = input("Пароль (или оставьте пустым для генерации): ").strip()
        
        if not password:
            print("\nГенерация пароля...")
            password = PasswordGenerator.generate()
            print(f"Сгенерированный пароль: {password}")
        
        return PasswordRecord(service, username, password)
    
    @staticmethod
    def get_service_to_delete() -> str:
        """Получение названия сервиса для удаления"""
        print("\n" + "=" * 40)
        print("УДАЛЕНИЕ ЗАПИСИ".center(40))
        print("=" * 40)
        return input("Введите название сервиса для удаления: ").strip()
    
    @staticmethod
    def show_generated_password(password: str):
        """Отображение сгенерированного пароля"""
        print("\n" + "=" * 40)
        print("СГЕНЕРИРОВАННЫЙ ПАРОЛЬ".center(40))
        print("=" * 40)
        print(f"\n\033[93mПароль: {password}\033[0m")  # Желтый цвет
        input("\nНажмите Enter для продолжения...")
    
    @staticmethod
    def confirm_action(message: str) -> bool:
        """Подтверждение действия"""
        response = input(f"{message} (y/n): ").strip().lower()
        return response == 'y'


# ==================== КОНТРОЛЛЕР ====================
class PasswordController:
    """Контроллер для управления логикой приложения"""
    
    def __init__(self):
        self.storage = PasswordStorage()
        self.view = ConsoleView()
    
    def run(self):
        """Запуск основного цикла приложения"""
        while True:
            self.view.show_menu()
            choice = input("\nВыберите действие: ").strip()
            
            if choice == '1':
                self.add_record()
            elif choice == '2':
                self.view_records()
            elif choice == '3':
                self.delete_record()
            elif choice == '4':
                self.generate_password()
            elif choice == '5':
                if self.view.confirm_action("Вы уверены, что хотите выйти?"):
                    self.view.show_message("До свидания!")
                    break
            else:
                self.view.show_message("Неверный выбор! Попробуйте снова.", True)
    
    def add_record(self):
        """Добавление новой записи"""
        try:
            record = self.view.get_record_input()
            
            if record is None:
                self.view.show_message("Запись не может быть пустой!", True)
                return
            
            if not record.service:
                self.view.show_message("Название сервиса не может быть пустым!", True)
                return
            
            if not record.username:
                self.view.show_message("Имя пользователя не может быть пустым!", True)
                return
            
            if not record.password:
                self.view.show_message("Пароль не может быть пустым!", True)
                return
            
            self.storage.add_record(record)
            self.view.show_message(f"Запись для сервиса '{record.service}' успешно добавлена!")
        except Exception as e:
            self.view.show_message(f"Ошибка при добавлении записи: {e}", True)
    
    def view_records(self):
        """Просмотр всех записей"""
        records = self.storage.get_all_records()
        self.view.show_records(records)
    
    def delete_record(self):
        """Удаление записи"""
        service = self.view.get_service_to_delete()
        
        if not service:
            self.view.show_message("Название сервиса не может быть пустым!", True)
            return
        
        if self.storage.delete_record(service):
            self.view.show_message(f"Запись для сервиса '{service}' успешно удалена!")
        else:
            self.view.show_message(f"Запись для сервиса '{service}' не найдена!", True)
    
    def generate_password(self):
        """Генерация пароля"""
        password = PasswordGenerator.generate_with_settings()
        self.view.show_generated_password(password)


# ==================== ГЛАВНЫЙ КЛАСС ====================
def main():
    """Главная функция"""
    # Настройка кодировки для Windows
    if os.name == 'nt':
        import sys
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    controller = PasswordController()
    controller.run()


if __name__ == "__main__":
    main()
