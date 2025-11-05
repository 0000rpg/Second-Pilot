# Second-Pilot

## Фронтенд

### _Для разработки_

Для разработки фронтэнда использовать команду (в корне проекта):

```Dockerfile
docker compose watch frontend-dev
```

Эта команда создаст **Docker-контейнер**, файлы которого синхронизируются с файлами в проекте. Сайт будет находится в <http://localhost:5173/>.

### _Для релиза_

Для запуска контейнера релизной версии фронтенда использовать:

```Dockerfile
docker compose up frontend-prod
```

Доступ к сайту будет по <http://localhost/> (порт 80)

Больше информации по [**фронтенду**](https://github.com/0000rpg/Second-Pilot/blob/main/frontend/README.md).
