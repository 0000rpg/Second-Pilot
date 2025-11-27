# Frontend Second-Pilot

## Описание

Frontend использует фреймворк Vue.js. В качестве формата
[SFC](https://ru.vuejs.org/guide/scaling-up/sfc.html) (однофайловых компонентов - `.vue` файлов)
используется - [Composition API](https://ru.vuejs.org/guide/introduction.html#api-styles).

## Рекомендуемое IDE

[VS Code](https://code.visualstudio.com/) +
[Плагин Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar)

## Cтилизатора кода

Для использования стилизатора кода (он отображает ошибки и правит стиль кода) скачиваем расширения для VSCode - [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) и [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint). И в папке frontend выполняем команду:

```bash
npm install
```

Если Prettier не работает (не ставит ';' и т.д.), то запускать его вручную командой (в папке frontend):

```bash
npm run format
```

## Рекомендуемые настройки браузера

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
    - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
    - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
    - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
    - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)
