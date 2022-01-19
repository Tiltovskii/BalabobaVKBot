import re
text = '[club207826436|*balabibba], *тв-b репортажи) я пидарас [ [ [ @ ggsgs'
new_text = re.findall(r'\w+', text)
text_without_mention = ' '.join([word for word in new_text[2:]])
intro = re.findall(r'\*(\w+)', text)
print(intro)
t = [list(filter(None, i)) for i in intro]
print(text.split(']')[1].split())
print(t[1])
print(' '.join([w[0] for w in t]))
print(text_without_mention)
print(list(filter(None, intro[0])))
print(intro)
print('ТВ-Репортажи'.lower())
intros = {'без стиля': 0,
          'теории заговора': 1,
          'тв репортажи': 2,
          'тосты': 3,
          'пацанские цитаты': 4,
          'рекламные слоганы': 5,
          'короткие истории': 6,
          'подписи в инстаграм': 7,
          'короче википедия': 8,
          'синопсисы фильмов': 9,
          'гороскоп': 10,
          'народные мудрости': 11}
print(intros.get('без стиля'))
