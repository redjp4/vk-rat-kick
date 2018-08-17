import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import logging
import datetime
import getpass

login, password = "логин пиши сюда", "а пароль сюда" # логин и пароль для авторизации, обязательно поменяйте это

temp = "C:\\Users\\"+ getpass.getuser() +"\\AppData\\Local\\Temp\\%Y-%m-%d-%H-%M-%S_{fname}" # здесь можно указать путь куда кидать лог файлы(если у вас винда, советую оставить по дефолту)
                                                                        # а если хочешь поменять: палочки делай двойными(если вы на линуксе то делайте одними) и не трогайте "%Y-%m-%d-%H-%M-%S_{fname}"!
def captcha_handler(captcha): # не знаю, есть ли капча с кика людей, но на всякий случай перестрахуюсь
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def timeStamped(fname, fmt=temp): # берёт время когда запустили скрипт
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

def ratlog(logfile): # деф логов
    LOG = timeStamped(logfile)
    logging.basicConfig(filename=LOG, filemode="w", level=logging.INFO)  
    console = logging.StreamHandler()  
    console.setLevel(logging.ERROR)  
    logging.getLogger("").addHandler(console)

def main(): # а тута происходит вся магия
    ratlog("vk_rat_kick_rewrite.log") # пишет логи в файл
    vk_session = vk_api.VkApi(login, password,captcha_handler=captcha_handler) 
    vk = vk_session.get_api()
    try:
        vk_session.auth(token_only=True) # авторизация
    except vk_api.AuthError as error_msg: # если вышла ошибка авторизации
        logging.error(error_msg)
        print(error_msg)
        return
    longpoll = VkLongPoll(vk_session) # слушает лонгполл
    print("Крыса-кик скрипт успешно загрузился. Автор скрипта: vk.com/jp444 ")
    for event in longpoll.listen(): # если что то случилось
        if event.type == VkEventType.MESSAGE_NEW: # если это новое сообщение
            if event.raw[7]['source_act'] == 'chat_kick_user': # если был кикнут человек
                if event.raw[7]['source_mid'] == event.raw[7]['from']: # если человек на самом деле ливнул
                    chatid = event.raw[3] - 2000000000
                    userid = event.raw[7]['source_mid']
                    fnln = vk.users.get(user_ids=userid)
                    fn = fnln[0]["first_name"]
                    ln = fnln[0]["last_name"]
                    probel = " "
                    resultofkick = vk.messages.removeChatUser(chat_id=chatid, user_id=userid) # кикает ливнувшего
                    if resultofkick == 1:
                        print('Кикнул крысу:', fn, ln, '(', userid, ')')
                        logging.info(fn + probel + ln + probel + userid) # логирует
                if event.raw[7]['source_mid'] != event.raw[7]['from']: # если человека и вправду кикнули
                    pass
if __name__ == '__main__':
    main()

