# Electronic Network API

## Описание

Проект представляет собой веб-приложение с API интерфейсом и админ-панелью, с базой данных на PostgreSQL.
Данное приложение для сети по продаже электроники. Сеть имеет иерархическую структуру из трёх уровней: завод, розничная сеть и индивидуальный предприниматель.
Каждое звено сети ссылается только на одного поставщика оборудования (не обязательно предыдущего по иерархии). Уровни определяются не название звена, а отношением к остальным элементам сети.
Завод всегда на уровне 0, сеть может быть 1-ого уровня и 2-ого, в зависимости от того, у кого она закупается. Ровно также с ИП.
Также реализован блок транзакций по опалате и добавлено действие в административной панели по очищению задолженности перед поставщиком у выбранных закупщиков.

Все функции доступны через API.
Стек технологий: Python, Django, DRF, PostgreSQL, Docker, Redoc, Swagger


# Установка через DOCKER

1. Клонирование репозитория ```git clone https://github.com/fniad/electronics-network.git```
2. ```cd electronics-network```
3. ```touch .env.docker```
```nano .env.docker```
и заполнить по шаблону из **.env.docker.test**
4. На Ubuntu или Linux сначала остановить postgresql ```systemctl stop postgresql```
5. ```docker-compose build```
6. ```docker-compose up```

# Админ-панель
Доступ к админ-панели по адресу http://0.0.0.0:8000/admin/ с использованием учетных данных суперпользователя.
Чтобы добавить суперпользователя, требуется открыть новое терминальное окно и ввести следующую команду:
```docker-compose exec app python3 manage.py createsuperuser```

# Использование

1. Создавайте объекты сети через админ-панель.
2. Используйте API для выполнения операций CRUD с поставщиками.
3. Фильтруйте объекты по стране, используя API.
4. Для просмотра деталей по поставщикам перейдите к нужной вам категории.
5. Фильтруйте объекты по названию города в админ-панели.
6. Используйте действие администратора для очистки долгов выбранных объектов сети.