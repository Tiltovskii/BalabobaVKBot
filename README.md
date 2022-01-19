# BalabobaVKBot
**A Simple VKBot connecting to Balaboba**

Что за VKBot?
------------------------------------
Основная функция бота - это связь с балабобой от Яндекса в чате в ВК.
Дополнительная же функция - это составление списка токсичный участников беседы. 

Принцип работы 
------------------------------------
С балабобой всё достаточно просто: отпрвляется request на сайт [Balaboba](https://yandex.ru/lab/yalm), после чего его ответ отсылается в беседу. Изначальный текст, который посылается балабобе, - это пересланное или ответ на сообщение с упоминанием бота. 
Это всё находится в файле Balaboba.py

Вторая же функция - токсичность участников беседы, которая работает следующим образом: каждый раз, когда приходит сообщение в чат, бот отправляет на [HuggingFace](https://huggingface.co/SkolkovoInstitute/russian_toxicity_classifier) запрос, ответ которого является отношением токсичности и нейтральности предложения, и если предложение оказывается токсичным, то человеку дается "балл токсичности", из соотношения которых и будет составляться рейтинг.
Это находится в файле toxic.py.
Можно заметить, что в файле есть функция, которая нигде не используется (get_neut_toxic_rate()), у неё есть пара проблем, которые я не решил.
Во-первых, работает она достаточно медленно, особенно если у вас нет вычислительных мощностей.
А во-вторых, для прогона через модель нужно хотя бы 2 Гб ОЗУ, а так как я хотел задеплоить бота бесплатно на AWS, то всего получил 1 Гб.

Начало работы
------------------------------------
Для начала работы вам нужно всего лишь зайти в config.py и изменить root (ваша папка с данными файлами) и token.
Дальше приглашаете вашего бота в беседу и с помощью вызова с упоминанием пишите help (то есть [@упоминание] help) увидите кратко описание команд бота.

Итоги
------------------------------------
Делал всё для себя, для смешков, вооооот.
Всем спасибо за внимание всеееееем покааааа))))


