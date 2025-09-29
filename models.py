from flask_sqlalchemy import SQLAlchemy

# Инициализация объекта SQLAlchemy для работы с базой данных
db = SQLAlchemy()

class ShoppingItem(db.Model):
    """
    Модель товара для списка покупок.
    Определяет структуру таблицы в базе данных и поля товара.
    """
    
    # Имя таблицы в базе данных (необязательно, по умолчанию используется имя класса в нижнем регистре)
    __tablename__ = 'shopping_items'
    
    # Основные поля модели:
    
    # ID товара - первичный ключ, автоинкремент
    id = db.Column(db.Integer, primary_key=True)
    
    # Название товара - обязательное поле, максимальная длина 100 символов
    name = db.Column(db.String(100), nullable=False)
    
    # Категория товара - обязательное поле, максимальная длина 50 символов
    category = db.Column(db.String(50), nullable=False)
    
    # Количество товара - необязательное поле, значение по умолчанию '1 шт'
    quantity = db.Column(db.String(50), default='1 шт')
    
    # Приоритет покупки - необязательное поле, значение по умолчанию 'можно купить'
    priority = db.Column(db.String(20), default='можно купить')
    
    # Статус покупки - булево значение, по умолчанию False (не куплен)
    purchased = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        """
        Строковое представление объекта для отладки и логирования.
        Возвращает форматированную строку с именем товара.
        """
        return f'<Item {self.name}>'