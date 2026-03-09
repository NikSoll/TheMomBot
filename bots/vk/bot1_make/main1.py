import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import config


def main():
    vk_session = vk_api.VkApi(token=config.VK_TOKEN)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, config.GROUP_ID)

    print("ВК бот запущен!")

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.obj.message
            user_id = msg.from_id
            text = msg.text

            #start
            if text == "start" or text == "Start":
                keyboard = VkKeyboard()
                keyboard.add_button("📝 Записаться", VkKeyboardColor.PRIMARY)
                keyboard.add_button("📋 Мои записи", VkKeyboardColor.SECONDARY)
                keyboard.add_line()
                keyboard.add_button("ℹ️ О салоне", VkKeyboardColor.NEGATIVE)

                vk.messages.send(
                    user_id=user_id,
                    message=config.MESSAGES["welcome"],
                    keyboard=keyboard.get_keyboard(),
                    random_id=0
                )
            else:
                vk.messages.send(
                    user_id=user_id,
                    message=f"Вы написали: {text}",
                    random_id=0
                )


if __name__ == "__main__":
    main()