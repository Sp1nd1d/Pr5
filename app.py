from flask import Flask, render_template, request, redirect, url_for
from models import db, ShoppingItem

# Создание экземпляра Flask приложения
app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping_list.db'  # SQLite база данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение отслеживания модификаций

# Инициализация базы данных с приложением
db.init_app(app)

# Предопределенные значения для выпадающих списков
CATEGORIES = ['Молочка', 'Овощи/Фрукты', 'Мясо/Рыба', 'Бакалея', 
              'Хлеб', 'Напитки', 'Бытовая химия', 'Сладости', 'Другое']
PRIORITIES = ['срочно купить', 'можно купить']

@app.route('/')
def index():
    """
    Главная страница - отображение списка покупок с фильтрацией
    """
    # Получаем параметры фильтрации из URL-параметров запроса
    category_filter = request.args.get('category', '')  # Фильтр по категории
    priority_filter = request.args.get('priority', '')  # Фильтр по приоритету
    show_purchased = request.args.get('show_purchased', 'false') == 'true'  # Показать купленные?
    
    # Строим запрос с фильтрами
    query = ShoppingItem.query
    
    # Применяем фильтры, если они указаны
    if category_filter:
        query = query.filter(ShoppingItem.category == category_filter)
    if priority_filter:
        query = query.filter(ShoppingItem.priority == priority_filter)
    if not show_purchased:
        query = query.filter(ShoppingItem.purchased == False)  # Скрываем купленные
    
    # Сортируем по приоритету (срочные первыми) и получаем все элементы
    items = query.order_by(ShoppingItem.priority.desc()).all()
    
    # Рендерим шаблон с передачей всех необходимых данных
    return render_template('index.html', 
                         items=items,
                         categories=CATEGORIES,
                         priorities=PRIORITIES,
                         current_category=category_filter,
                         current_priority=priority_filter,
                         show_purchased=show_purchased)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """
    Добавление нового товара - обработка GET (форма) и POST (создание)
    """
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        priority = request.form['priority']
        
        # Создаем новый объект товара
        new_item = ShoppingItem(
            name=name,
            category=category,
            quantity=quantity,
            priority=priority
        )
        
        # Сохраняем в базу данных
        db.session.add(new_item)
        db.session.commit()
        
        # Перенаправляем на главную страницу
        return redirect(url_for('index'))
    
    # GET запрос - отображаем форму добавления
    return render_template('add_edit_item.html',
                         categories=CATEGORIES,
                         priorities=PRIORITIES,
                         item=None)  # Передаем None для режима добавления

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """
    Редактирование существующего товара
    """
    # Получаем товар по ID или возвращаем 404 если не найден
    item = ShoppingItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        # Обновляем данные товара из формы
        item.name = request.form['name']
        item.category = request.form['category']
        item.quantity = request.form['quantity']
        item.priority = request.form['priority']
        
        # Сохраняем изменения
        db.session.commit()
        return redirect(url_for('index'))
    
    # GET запрос - отображаем форму редактирования с текущими данными
    return render_template('add_edit_item.html',
                         categories=CATEGORIES,
                         priorities=PRIORITIES,
                         item=item)  # Передаем объект товара для редактирования

@app.route('/toggle/<int:item_id>')
def toggle_item(item_id):
    """
    Переключение статуса покупки товара (куплен/не куплен)
    """
    item = ShoppingItem.query.get_or_404(item_id)
    item.purchased = not item.purchased  # Инвертируем текущий статус
    db.session.commit()
    return redirect(url_for('index'))  # Возвращаем на главную

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    """
    Удаление товара из списка
    """
    item = ShoppingItem.query.get_or_404(item_id)
    db.session.delete(item)  # Удаляем из базы
    db.session.commit()
    return redirect(url_for('index'))  # Возвращаем на главную

if __name__ == '__main__':
    # Создаем таблицы в базе данных при первом запуске
    with app.app_context():
        db.create_all()
    
    # Запускаем приложение в режиме отладки
    app.run(host="0.0.0.0", port=5000, debug=True)