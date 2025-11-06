# Фронтенд Second-Pilot

## Рекомендуемое IDE

[VS Code](https://code.visualstudio.com/) +
[Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (и выклчить Vetur).

## Рекомендуемые настройки браузера

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
    - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
    - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
    - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
    - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Запуск контейнера

### _Для разработки_

Для разработки фронтэнда использовать команду (в корне проекта):

```Dockerfile
docker compose watch frontend-dev
```

Эта команда создаст **Docker-контейнер**, файлы которого синхронизируются с файлами в проекте. Сайт
будет находится в <http://localhost:5173/>.

Для использования стилизатора кода скачиваем расширение для VSCode - prettier. И в папке frontend
выполняем команду:

```bash
npm install
```

### _Для релиза_

Для запуска контейнера релизной версии фронтенда использовать:

```Dockerfile
docker compose up frontend-prod
```

Доступ к сайту будет по <http://localhost/> (порт 80)
