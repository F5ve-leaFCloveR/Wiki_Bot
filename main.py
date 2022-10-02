import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from translate import Translator
import wikipedia

# авторизация
vk = vk_api.VkApi(token="Add your token")
session_api = vk.get_api()
longpool = VkLongPoll(vk)

# язык выдачи информации
wikipedia.set_lang('ru')


# функция для ожидания сообщения от конкретного пользователя
def watch_for_message(id):
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                if id == event.user_id:
                    return message


# функция для отправки сообщений
def sender(id, query):
    vk.method("messages.send", {"user_id": id, "message": query, "random_id": 0})
    print("Сообщение пользователю " + str(id) + " отправлено")


def menu(id):
    sender(id, "Menu:\n1. Translator\n2. Wikipedia")
    message = watch_for_message(id)
    if message == "1":
        translate(id)
    elif message == "2":
        wiki(id)


def wiki(id):
    sender(id, "Введите запрос и получите ответ.")
    while True:
        message = watch_for_message(id)
        if message == "back":
            break
        final = wikipedia.summary(message, sentences=4)
        sender(id, final)


def translate(id):
    sender(id, "Выберите  \n1. Russian to english\n 2. English to russian\n 3. Menu")
    message = watch_for_message(id)
    if message == "1":
        translator = Translator(from_lang="ru", to_lang="en")
        sender(id, "Введите текст")
        while True:
            message = watch_for_message(id)
            if message == "back":
                break
            translation = translator.translate(message)
            sender(id, translation)
        translate(id)
    elif message == "2":
        translator = Translator(from_lang="en", to_lang="ru")
        sender(id, "Введите текст")
        while True:
            message = watch_for_message(id)
            if message == "назад":
                break
            translation = translator.translate(message)
            sender(id, translation)
        translate(id)
    elif message == "3":
        menu(id)


def main():
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                id = event.user_id
                if message == "start":
                    menu(id)


if __name__ == "__main__":
    main()
