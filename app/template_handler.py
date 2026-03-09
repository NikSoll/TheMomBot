import os
import shutil

#пути к шаблонам
TEMPLATE_PATHS = {
    'tg': {
        'make': 'bots/tg/bot1_make',
        'shop': 'bots/tg/bot2_shop',
        'quiz': 'bots/tg/bot3_quiz',
        'survey': 'bots/tg/bot4_survey',
        'mailer': 'bots/tg/bot5_mailer',
    },
    'vk': {
        'make': 'bots/vk/bot1_make',
        'shop': 'bots/vk/bot2_shop',
        'quiz': 'bots/vk/bot3_quiz',
        'survey': 'bots/vk/bot4_survey',
        'mailer': 'bots/vk/bot5_mailer',
    }
}


def get_template_path(platform, bot_type):
    return TEMPLATE_PATHS.get(platform, {}).get(bot_type)


def find_config_file(bot_path):
    config_names = ['config.py', 'config1.py', 'config2.py', 'config3.py', 'config4.py', 'config5.py']
    for name in config_names:
        path = os.path.join(bot_path, name)
        if os.path.exists(path):
            return path
    return None


def copy_template(template_path, bot_path):
    if os.path.exists(template_path):
        shutil.copytree(template_path, bot_path)
        return True
    return False


def replace_in_file(file_path, replacements):
    #текс в файле
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)