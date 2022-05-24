import re  # Regular Expressions
import nltk # Natural Language Toolkit
import random, psutil
from numpy import append # Random and pseudorandom data for seeding


BOT_CONFIG = {
    # Все намерения которые поддерживает наш бот
   "intents": {
        "hello": {
            "examples" : ["Привет", "Здарова", "Йо", "Хай", "Хеллоу"],
            "responses": ["Здравстсвтсвтвтвуй человек", "И тебе не хворать", "Здоровее видали"],
        },
        "how_are_you": {
            "examples" : ["Как дела", "Чо каво", "Как поживаешь"],
            "responses": ["Маюсь Фигней", "Веду интенсивы", "Учу Пайтон"],
        },
        "chatting1": {
            "examples" : ["Что нового", "Чем занимаешься", "Какие планы"],
            "responses": ["Продолжу фигнёй страдать", "Скоро спать пойду", "Пойду гулять"],
        },
        "acks": {
            "examples" : ["Ладно", "Хорошо", "Отлично","Давай","Конечно", "Ясно","Договорились"],
            "responses": ["А теперь твой вопрос", "Ок, теперь тебя слушаю", "Ок. Я слушаю"],
        },
        "stopper":{
            "examples" : ["Пока!", "До свиданья", "Хватит", "Закончили", "Стоп", "Иди нахер", "Отвали"],
            "responses": ["Ладно, до встречи!", "Так и быть...", "И тебе всего хорошего!", "Жаль, что так рано закончили", "Ещё увидимся!"],
        }
    },
    # Фразы когда бот не может ответить
    "failure_phrases": ["Чоэтобыло?", "Даже не знаю что сказать", "Поставлен в тупик", "Перефразируйте, я всего лишь бот"],
}


# На вход: два текста, на выход: boolean(True, False) 
# Функция isMatch вернет True, если тексты совпадают или False иначе
def isMatch(text1, text2, threshhold=0.4):
  text1 = text1.lower()  # Приводим к нижнему регистру ("ПрИвет" => "привет")
  text2 = text2.lower()

  # Удаление знаков препинания
  # = Удалить все кроме букв и пробелов
  pattern = r'[^\w\s]'
  text1 = re.sub(pattern, "", text1) # Делать замену символов в строке
  text2 = re.sub(pattern, "", text2)

  # Проверить что одна фраза является частью другой

  # Text1 содержит text2
  if text1.find(text2) != -1:
    return True
  
  # Text2 содержит text1
  if text2.find(text1) != -1:
    return True

  # Расстояние Левенштейна (edit distance = расстояние редактирования)
  distance = nltk.edit_distance(text1, text2)  # 0...Inf
  length = (len(text1) + len(text2))/2
  score = distance/length

  return score < threshhold


def getAnswer(text, examples, responses):
    for example in examples:  # Для каждого элемента списка examples
        if isMatch(text, example):  # Если пример совпадает с текстом пользователя
            return random.choice(responses)
   

def main():
    # initialize random seed
    random.seed(int(psutil.virtual_memory()[3]%psutil.virtual_memory()[4]*psutil.cpu_percent(1)))
    
    intents_noted = set()
    
    # Для каждого намерения, пытаемся понять ответ
    print("Привет! Давай поговорим?")

    while True:
        text = input()

        answer = ''

        for int_name, intent in BOT_CONFIG["intents"].items():
            phrase = getAnswer(text, intent["examples"], intent["responses"])
            if (phrase): # если что-то нашлось
                if (answer): 
                    answer = answer + "\n" + phrase  # дописываем в наш ответ
                else: 
                    answer = phrase # или просто записываем в ответ
                intents_noted.add(int_name) # запоминаем, какие намерения встретились
        
        if (not answer): # если бот вообще ничего не понял из сказанного
            answer = random.choice(BOT_CONFIG["failure_phrases"]) # выдать дежурную фразу

        print(answer)

        if ("stopper" in intents_noted): # если кожаный ублюдок хочет закончить разговор
            print("Было приятно пообщаться!") # заканчиваем
            break
        else: 
            intents_noted = set() # в противном случае можно обнулить намерения и продолжаем


if __name__ == "__main__":
	main()