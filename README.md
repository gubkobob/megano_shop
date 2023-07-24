![main page](./static/assets/img/logo_footer.png) 

<h1 align="center"> Командный дипломный проект по курсу Python Django </h1>
<h2 align="center">Проект сайта интернет-магазина MEGANO</h2><h5 align="center">Период работы над проектом 29 апреля 2023 - 24 июля 2023</h5>
<h3>Участники Проекта: </h3> 
<h4>TeamLead: Максим Семенюк </h4>
<h4> Татьяна Федутик </h4>
<h4> Владимир Игнатушенко </h4>
<h4> Александр Белов </h4>
<h4> Александр Малафеевский </h4>

![main page](./uploads/img_readmi/team.jpg) 



<h1>Добро пожаловать в MEGANO !</h1> 


> <h2> Структура сайта: </h2>
> <p> Главная страница</p>
> <p> Каталог (сам каталог, детальная страница товара)</p>
> <p> Скидки </p>
> <p> Сравнение </p>
> <p> Страница оформления заказа (корзина, оформление заказа, оплата)</p>
> <p> Личный кабинет (личный кабинет, профиль, история заказов)</p>
> <p> Административный раздел</p>


> <h2> Главная страница </h2>
>
> ![main page](./uploads/img_readmi/main_page_1.jpg)
> ![main page](./uploads/img_readmi/main_page_2.jpg)
> ![main page](./uploads/img_readmi/main_page_3.jpg)


> <h2> Каталог </h2>
> <h3> Каталог </h3>
>
> ![main page](./uploads/img_readmi/catalog.jpg)
> 
> <h3> Детальная страница товара </h3>
>
> ![main page](./uploads/img_readmi/detail.jpg)


> <h2> Скидки </h2>
>
> ![main page](./uploads/img_readmi/discounts.jpg)


> <h2> Сравнение </h2>
>
> ![main page](./uploads/img_readmi/comparison.jpg)


> <h2> Оформление заказа </h2>
> <h3> Корзина </h3>
>
> ![main page](./uploads/img_readmi/cart.jpg)
> <h3> Оформление Шаг 1 </h3>
>
> ![main page](./uploads/img_readmi/order_step_1.jpg)
> <h3> Оформление Шаг 2 </h3>
>
> ![main page](./uploads/img_readmi/order_step_2.jpg)
> <h3> Оформление Шаг 3 </h3>
>
> ![main page](./uploads/img_readmi/order_step_3.jpg)
> <h3> Оформление Шаг 4 </h3>
>
> ![main page](./uploads/img_readmi/order_step_4.jpg)
> <h3> Предварительный просмотр и подтверждение </h3>
>
> ![main page](./uploads/img_readmi/order.jpg)
> <h3> Оплата Способ 1 - Онлайн картой </h3>
>
> ![main page](./uploads/img_readmi/payment_2.jpg)
> <h3> Оплата Способ 2 - Онлайн со случайного чужого счета </h3>
>
> ![main page](./uploads/img_readmi/payment_1.jpg)
 

> <h2> Личный кабинет </h2>
> <h3> Личный кабинет </h3>
>
> ![main page](./uploads/img_readmi/account.jpg)
> 
> <h3> Профиль </h3>
>
> ![main page](./uploads/img_readmi/profile.jpg)
> 
> <h3> История заказов </h3>
>
> ![main page](./uploads/img_readmi/order_history.jpg)



> <h3> Регистрация нового пользователя </h3>
>
> ![main page](./uploads/img_readmi/registration.jpg)
> 
> 
> <h3> Вход в личный кабинет </h3>
>
> ![main page](./uploads/img_readmi/input.jpg)
> 
> 
> <h3> Восстановление пароля </h3>
>
> ![main page](./uploads/img_readmi/password_recovery.jpg)



> <h2> Пошаговый запуск проекта локально: </h2>
>
> <h3> Активируем виртуальное окружение </h3> 
>
>> <p><i> source venv/bin/activate </i></p> 
> <h3> Устанавливаем пакеты </h3>  
>
>> <p><i> pip install -r requirements.txt </i></p> 
> <h3> Запускаем базу данных </h3> 
> 
>> <p><i> python manage.py makemigrations </i></p> 
>> <p><i> python manage.py migrate </i></p> 
> <h3> Запускаем фикстуры </h3> 
> 
>> <p><i> python manage.py loaddata fixtures/1_Setting.json </i></p>
>> <p><i> python manage.py loaddata fixtures/2_User.json </i></p>
>> <p><i> python manage.py loaddata fixtures/3_Category.json </i></p>
>> <p><i> python manage.py loaddata fixtures/4_SubCategory.json </i></p>
>> <p><i> python manage.py loaddata fixtures/5_Shop.json </i></p>
>> <p><i> python manage.py loaddata fixtures/6_Product.json </i></p>
>> <p><i> python manage.py loaddata fixtures/7_ProductInShop.json </i></p>
>> <p><i> python manage.py loaddata fixtures/8_ProductInShopImage.json </i></p>
>> <p><i> python manage.py loaddata fixtures/9_Specifications.json </i></p>
>> <p><i> python manage.py loaddata fixtures/10_Subspecifications.json </i></p>
>> <p><i> python manage.py loaddata fixtures/11_Discount.json </i></p>
>
> <h3> Запуск сельдерей для проведения оплаты </h3> 
>
>> <p><i> celery -A config  worker -l info -P eventlet </i></p>
>> <p><i> celery worker --app=config --loglevel=info </i></p>
>> <p><i> docker-compose up --build -d </i></p>
>
>
>> <h3> Для Mac Загрузка сельдерей </h3>
>>  <p><i>1. brew install rabbitmq </i></p>
>>  <p><i>2. export PATH=$PATH:/usr/local/sbin </i></p>
>> 
>> <h3>Start server (Mac) </h3>
>> <p><i>3. sudo rabbitmq-server -detached  <p>(-detached указывает, что сервер должен работать в фоновом режиме) </p>  </i></p>
>> <p><i>4. Переходим по http://localhost:15672 вводим логин и пароль </i></p>
>> <p><i>5. Username: guest </i></p>
>> <p><i>6. Password: guest </i></p>
>>
>> <h3>To stop server </h3>
>> <p><i>7. sudo rabbitmqctl stop </i></p>
>> 
>> <h3>Еще 1 вариант, если с предыдущими не получилось </h3>
>> <p><i> 1. brew install rabbitmq </i></p>
>> <p><i> 2. export PATH=$PATH:/usr/local/sbin </i></p>
>> <p><i> 3. rabbitmq-server  </i></p>
>> <p><i> 4. python manage.py runserver </i></p>
>> <p><i> 5. Переходим по http://localhost:15672 вводим логин и пароль </i></p>
>> <p><i> 6. Username: guest  </i></p>
>> <p><i> 7. Password: guest  </i></p>
>>
>
> <h3> Запускаем проект </h3>
>
>> <p><i> python manage.py runserver </i></p>
>
> <h2> Пошаговый запуск проекта в Docker: </h2>
>
>> <h3>Устанавливаем Docker на рабочий стол </h3>
>>
>>> <p><i> скачать можно тут: https://www.docker.com/ </i></p>
>> <h3>Запускаем в терминале </h3> 
>>
>>> <p><i> docker-compose up --build </i></p>
>>> <p> или </p>
>>> <p><i> docker-compose up --build -d (с возможностью закрывать терминал) </i></p>
