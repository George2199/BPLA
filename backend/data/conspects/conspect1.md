# Конспект видео по теме "Переменные"

Добавьте краткое описание проекта, опишите какую задачу он решает. 1-3 предложения будет достаточно. Добавьте бейджи для важных статусов.

![Компьютер](/data/imgs/Drone.png)

<div style="margin: 20px 0">
  <button onclick="window.downloadAnyContent('http://localhost:5000/data/conspects/example.txt', 'example.txt')" style="background-color: #4CAF50; color: white; padding: 10px 15px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">
    Скачать текстовый файл
  </button>
</div>

<script>
// Если глобальная функция не определена, используем локальную
if (typeof window.downloadAnyContent !== 'function') {
  window.downloadAnyContent = function(url, filename) {
    console.log(`Локальная функция скачивания: ${url}, ${filename}`);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.target = '_blank';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
}
</script>

## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Contributing](#contributing)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Технологии
- [GatsbyJS](https://www.gatsbyjs.com/)
- [TypeScript](https://www.typescriptlang.org/)
- ...

## Использование
Расскажите как установить и использовать ваш проект, покажите пример кода:

```python
# Пример кода на Python
def hello_world():
    print("Hello, World!")
    
hello_world()
```

### Подраздел 1
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies tincidunt, nisl nisl aliquam nisl, nec aliquam nisl nisl sit amet nisl. Nullam auctor, nisl eget ultricies tincidunt, nisl nisl aliquam nisl, nec aliquam nisl nisl sit amet nisl.

### Подраздел 2
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies tincidunt, nisl nisl aliquam nisl, nec aliquam nisl nisl sit amet nisl. Nullam auctor, nisl eget ultricies tincidunt, nisl nisl aliquam nisl, nec aliquam nisl nisl sit amet nisl.

### Подраздел 3
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies tincidunt, nisl nisl aliquam nisl, nec aliquam nisl nisl sit amet nisl. Nullam auctor, nisl eget ultricies tincidunt, nisl nisl aliquam nisl, nec aliquam nisl nisl sit amet nisl.



