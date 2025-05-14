* Получаем токен https://sso.sberosc.sigma.sbrf.ru/dashboard/profile/
*  Создаем pip.ini здесь: `~/.config/pip/pip.conf`

```asciidoc
[global]
index-url=https://token:<TOKEN>@sberosc.sigma.sbrf.ru/repo/pypi/simple
trusted-host=sberosc.sigma.sbrf.ru
default-timeout=120
```

* Качаем библиотеки (sber os)

```bash
cd ./venv/bin
```

```bash
pip install -U langchain-gigachat

#Для работы с langchain_community библиотекой (например document_loaders)
pip install -U langchain-community
 
#Для слплита файлов на документы (например SentenceTransformerEmbeddings)
pip install -U sentence-transformers
 
#Для работы с бд ембеддингов
pip install -U chromadb
 
#Для работы с бд ембеддингов (взамен хромы, так как тот слабо поддерживается и не работает нормально)
pip install -U faiss-cpu
```

* Генерируем тесты `postscript:monoscript [compileTestJava]` 
* Собираем шаги `postscript:monoscript [reportCucumberSteps]`