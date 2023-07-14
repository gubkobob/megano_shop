#Запуск докера
docker build . -t app

#Запуск докер-компоуз
docker-compose up --build

RUN -d --hostname rmq --name rabbit-server -p 8080:15672 -p 5672:5672 rabbitmq:3-management