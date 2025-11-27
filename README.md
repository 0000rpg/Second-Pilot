# Second-Pilot

## Запуск проекта

### _Для разработки_

Для разработки фронтэнда использовать команду (в корне проекта):

```Dockerfile
docker compose watch frontend-dev
```

Эта команда создаст **Docker-контейнеры**, файлы которых синхронизируются с файлами в проекте. Сайт будет находится в <http://localhost/> (порт 80).

### _Для релиза_

Для запуска контейнеров релизной версии использовать:

```Dockerfile
docker compose up frontend-prod
```

Доступ к сайту будет по <http://localhost/> (порт 80)

### _Дополнительная информация_

Больше информации по [**фронтенду**](https://github.com/0000rpg/Second-Pilot/blob/main/frontend/README.md).

Больше информации по [**бекэнду**](https://github.com/0000rpg/Second-Pilot/blob/main/backend/README.md).
