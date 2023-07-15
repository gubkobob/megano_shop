#Запуск сельдерей

celery -A config  worker -l info -P eventlet




## Для Mac Загрузка 
>1. ***brew install rabbitmq***
>2. ***export PATH=$PATH:/usr/local/sbin***
>>###  Start server (Mac)
>>> ***sudo rabbitmq-server -detached***   
_(-флаг отсоединения указывает, что сервер должен работать в фоновом режиме)_ 
>>>> Переходим по_ _http://localhost:15672_ _вводим логин и пароль_
>>>>> ***_Username: guest_***
>>>>>> ***_Password: guest_***
>
>>### To stop server
>>>sudo rabbitmqctl stop
> 
>>###Доп. пользовательские настройки (не обязательно)
>>>1. sudo rabbitmq-server -detached
>>>2. sudo rabbitmqctl add_user myuser mypassword
>>>3. sudo rabbitmqctl add_vhost myvhost
>>>4. sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"



## Для Ubuntu
>1. apt-get install -y erlang
>2. apt-get install rabbitmq-server
>
>># Включение и запуск:
>>>1. systemctl enable rabbitmq-server
>>>2. systemctl start rabbitmq-server
>
>>##Проверка состояния сервера
>>> systemctl status rabbitmq-server​
