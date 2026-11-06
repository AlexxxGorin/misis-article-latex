# Оценка адаптации языковой модели к татарскому языку

Статья для курса научного письма НИТУ «МИСиС». Автор — Горин Александр Олегович; научный руководитель — И. И. Пионтковская.

Текст содержит введение, анализ работ, постановку задачи, методику и список литературы. Эксперимент пока не проводился, поэтому результатов в статье нет. Конкретные модель, корпус и вычислительный бюджет выбираются перед пилотом по описанным в статье критериям.

## Сборка

Исходный текст — `article.md`. Команда `python3 scripts/render_article.py` создаёт `article.tex`. Для локальной сборки нужны XeLaTeX и пакеты класса `misisarticle.cls`:

```bash
python3 scripts/render_article.py
mkdir -p build
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build article.tex
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build article.tex
```

PDF: `build/article.pdf`. GitHub Actions выполняет ту же сборку при push, pull request и ручном запуске; PDF доступен как артефакт `article-pdf` соответствующего запуска.

Оформление основано на [шаблоне НИТУ «МИСиС»](https://github.com/sadekovlar/misis-article-latex). Репозиторий является форком шаблона; исходные `misisarticle.cls` и `LICENSE` сохранены. Класс распространяется под LPPL 1.3c.
