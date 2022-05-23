import re  # Regular Expressions
import nltk # Natural Language Toolkit
import random # Random


BOT_CONFIG = {
    # Все намерения которые поддерживает наш бот
   "intents": {
        "hello": {
            "examples" : ["Привет", "Здарова", "Йо", "Приветос", "Хеллоу"],
            "responses": ["Здравстсвтсвтвтвуй человек", "И тебе не хворать", "Здоровее видали"],
        },
        "how_are_you": {
            "examples" : ["Как дела", "Чо каво", "Как поживаешь"],
            "responses": ["Маюсь Фигней", "Веду интенсивы", "Учу Пайтон"],
        }
    },
    # Фразы когда бот не может ответить
    "failure_phrases": ["Даже не знаю что сказать", "Поставлен в тупик", "Перефразируйте, я всего лишь бот"],
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
    print("Тупе техт хере:")
    text = input()

    # Для каждого намерения, пытаемся понять ответ
    answer = ''
    for intent in BOT_CONFIG["intents"].values():
        phrase = getAnswer(text, intent["examples"], intent["responses"])
        if (answer): answer = answer + "\n" + phrase  # Выводим на экран случайный элемент списка responses
        else: answer = phrase
    
    if (answer.length() < 1)
        answer = random.choice(BOT_CONFIG["failure_phrases"])



if __name__ == "__main__":
	main()