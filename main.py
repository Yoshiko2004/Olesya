import json
from random import choice
import telebot
from telebot import types

bot = telebot.TeleBot("7129636315:AAEWG7SkG0qHedKiJpj05QW9kTsv9ackYhI")

#открываем и читаем содержимое файлов формата JSON
with open("base.json", "r", encoding='utf8') as b:
    base_dialog = json.load(b)

with open("drawing.json", "r", encoding='utf8') as d:
    drawing_dialog = json.load(d)

with open("olesya.json", "r", encoding='utf8') as o:
    olesya_dialog = json.load(o)

with open("music.json", "r", encoding='utf8') as m:
    music_dialog = json.load(m)

with open("school.json", "r", encoding='utf8') as s:
    school_dialog = json.load(s)

with open("preferences.json.", "r", encoding='utf8') as p:
    preference_dialog = json.load(p)

with open("life.json", "r", encoding='utf8') as l:
    life_dialog = json.load(l)


#Олеся - смелая девушка, поэтому она решается написать нам первой. Эта функция отвечает за её приветствие.
@bot.message_handler(commands=['start'])
def start(message):
    bot_greeting = base_dialog[0]["greeting"]["bot_side"]
    bot.reply_to(message, choice(bot_greeting))


#После того, как мы ей сказали привет в ответ, она у нас решается спросить о нашем настроении.
#Данная функция отвечает за вывод ответа на наше приветствие и следующий за ним второ вопрос.
@bot.message_handler(content_types=['text'])
def continue_dialog(message):
    right_word_g = False

    your_greeting = base_dialog[0]["greeting"]["your_side"]
    her_question = base_dialog[0]["whatsapp"]["bot_side"]

    for greet in your_greeting:
        if greet in str(message.text).lower():
            right_word_g = True

    if right_word_g:
        msg = bot.reply_to(message, choice(her_question))
        bot.register_next_step_handler(msg, whatsapp)
    elif not right_word_g:
        msg = bot.reply_to(message, "Сорян, понять не могу...\n:_[\nНо спросить тебя о самочувствии стоит. Как ты?")
        bot.register_next_step_handler(msg, whatsapp)


#Данная функция отвечает за формирование клавиатуры после нашего ответа на вопрос.
@bot.message_handler(content_types=['text'])
def whatsapp(message):
    themes = types.ReplyKeyboardMarkup()
    drawing = types.KeyboardButton("💞О РИСОВАНИИ💞")
    life = types.KeyboardButton("🍃О ЖИЗНИ🍃")
    school = types.KeyboardButton("🥀О ШКОЛЕ🥀")
    music = types.KeyboardButton("🍄О МУЗЫКЕ🍄")
    preferences = types.KeyboardButton("🍓О ПРЕДПОЧТЕНИЯХ🍓")
    me = types.KeyboardButton("✨ОБО МНЕ✨")

    themes.row(drawing, me)
    themes.row(life, school)
    themes.row(music, preferences)

    right_word_a = False

    your_answer = base_dialog[0]["whatsapp"]["your_side"]
    her_answer = base_dialog[0]["whatsapp"]["bot_answer"]

    for whats in your_answer:
        if whats in str(message.text).lower():
            right_word_a = True

    if right_word_a:
        mg = bot.reply_to(message, choice(her_answer), reply_markup=themes)
        bot.register_next_step_handler(mg, choose)
    else:
        mg = bot.reply_to(message, "Мы точно на одном языке говорим?\nЛадно, опустим.\nПоговорим может?", reply_markup=themes)
        bot.register_next_step_handler(mg, choose)


#В общем данная функция отвечает за функционал основных шести кнопок.
@bot.message_handler(content_types=['text'])
def choose(message):
    # Данный блок отвечает за функционал кнопки, отвечающей за тему рисования. Появляются две подтемы и кнопка назад.
    if message.text == "💞О РИСОВАНИИ💞":
        draw = types.ReplyKeyboardMarkup()
        problems = types.KeyboardButton("💢О ПРОБЛЕМАХ💢")
        succes = types.KeyboardButton("🌷ОБ УСПЕХАХ🌷")
        back = types.KeyboardButton("👉НАЗАД👈")
        draw.row(problems, succes)
        draw.row(back)

        msgd = bot.send_message(message.chat.id, text=choice(base_dialog[0]["choose"]["drawing"]), reply_markup=draw)
        bot.register_next_step_handler(msgd, draws)

    # Данный блок отвечает за функционал кнопки, отвечающей за тему жизни Олеси. Появляются три вопроса и кнопка назад.
    elif message.text == "🍃О ЖИЗНИ🍃":
        life = types.ReplyKeyboardMarkup()
        rest = types.KeyboardButton("Как вы отдыхаете?")
        family = types.KeyboardButton("Расскажи о семье.")
        you = types.KeyboardButton("Расскажи мне, как ты поживаешь.")
        back = types.KeyboardButton("👉НАЗАД👈")
        life.row(rest, family, you)
        life.row(back)

        mgsp = bot.send_message(message.chat.id, text=choice(base_dialog[0]["choose"]["life"]),
                                reply_markup=life)
        bot.register_next_step_handler(mgsp, your_life)

    # Данный блок отвечает за функционал кнопки, отвечающей за тему школы. Появляются два вопроса и кнопка назад.
    elif message.text == "🥀О ШКОЛЕ🥀":
        sch = types.ReplyKeyboardMarkup()
        like = types.KeyboardButton("Что тебе нравится в школе?")
        dislike = types.KeyboardButton("Что тебе в школе не нравится?")
        back = types.KeyboardButton("👉НАЗАД👈")
        sch.row(like, dislike)
        sch.row(back)

        mssch = bot.send_message(message.chat.id, text=choice(base_dialog[0]["choose"]["school"]), reply_markup=sch)
        bot.register_next_step_handler(mssch, schools)

    # Данный блок отвечает за функционал кнопки, отвечающей за тему музыки.
    # Появляется одна кнопка для продолжения разговора.
    elif message.text == "🍄О МУЗЫКЕ🍄":
        mus = types.ReplyKeyboardMarkup()
        c = types.KeyboardButton("Продолжить диалог")
        mus.add(c)
        msgd = bot.send_message(message.chat.id, text=choice(base_dialog[0]["choose"]["music"]), reply_markup=mus)
        bot.register_next_step_handler(msgd, musics)

    # Данный блок отвечает за функционал кнопки, отвечающей за тему предпочтений. Появляются три вопроса и кнопка назад.
    elif message.text == "🍓О ПРЕДПОЧТЕНИЯХ🍓":
        pref = types.ReplyKeyboardMarkup()
        fav_food = types.KeyboardButton("Какую еду ты любишь?")
        fav_games = types.KeyboardButton("Какой твой любимый жанр в играх?")
        fav_films = types.KeyboardButton("Какие жанры фильмов ты любишь?")
        back = types.KeyboardButton("👉НАЗАД👈")
        pref.row(fav_food, fav_games, fav_films)
        pref.row(back)

        mgsp = bot.send_message(message.chat.id, text=choice(base_dialog[0]["choose"]["preferences"]), reply_markup=pref)
        bot.register_next_step_handler(mgsp, preference)

    # Данный блок отвечает за функционал кнопки, отвечающей за тему об Олесе. Появляются три вопроса и кнопка назад.
    elif message.text == "✨ОБО МНЕ✨":
        ques = types.ReplyKeyboardMarkup()
        age = types.KeyboardButton("Сколько тебе лет?")
        familia = types.KeyboardButton("Какая у тебя фамилия?")
        user = types.KeyboardButton("Почему у тебя юзерка странная. И ТГ указывает, что ты бот?")
        back = types.KeyboardButton("👉НАЗАД👈")
        ques.row(age, familia, user)
        ques.row(back)

        msgd = bot.send_message(message.chat.id, text=choice(base_dialog[0]["choose"]["herself"]), reply_markup=ques)
        bot.register_next_step_handler(msgd, question)


#Функция отвечает за функционал кнопок, отвечающих за подтемы темы рисования.
@bot.message_handler(content_types=['text'])
def draws(message):
    #Отвечает за функционал кнопки, отвечающей за появление ещё трёх подтем внутри подтемы.
    if message.text == "💢О ПРОБЛЕМАХ💢":
        problem = types.ReplyKeyboardMarkup()
        realisation = types.KeyboardButton("😥О СКИЛЛЕ В ЦЕЛОМ😥")
        lineart = types.KeyboardButton("😭О ЛАЙНЕ😭")
        render = types.KeyboardButton("😫О ПОКРАСЕ😫")
        problem.row(realisation)
        problem.row(lineart, render)
        msgp = bot.send_message(message.chat.id, text="Понятненько...\n:_[\nО какой проблеме поговорим?", reply_markup=problem)
        bot.register_next_step_handler(msgp, my_problems)

    # Отвечает за функционал кнопки, отвечающей за появление ещё трёх подтем внутри подтемы.
    elif message.text == "🌷ОБ УСПЕХАХ🌷":
        succes = types.ReplyKeyboardMarkup()
        style = types.KeyboardButton("🍂О СВОЁМ СТИЛЕ🍂")
        progress = types.KeyboardButton("🎀О СВОЁМ ПРОГРЕССЕ🎀")
        at_all = types.KeyboardButton("🌺ОБ ОПЫТЕ РИСОВАНИЯ В ЦЕЛОМ🌺")
        succes.row(at_all)
        succes.row(style, progress)
        msgp = bot.send_message(message.chat.id, text="Хорошо!\n;3\nО чём поговорим?",
                                reply_markup=succes)
        bot.register_next_step_handler(msgp, my_succes)

    #Отвечает за функционал кнопки назад. Эта кнопка отвечает за возвращение на "главное меню".
    elif message.text == "👉НАЗАД👈":
        themes = types.ReplyKeyboardMarkup()
        drawing = types.KeyboardButton("💞О РИСОВАНИИ💞")
        life = types.KeyboardButton("🍃О ЖИЗНИ🍃")
        school = types.KeyboardButton("🥀О ШКОЛЕ🥀")
        music = types.KeyboardButton("🍄О МУЗЫКЕ🍄")
        preferences = types.KeyboardButton("🍓О ПРЕДПОЧТЕНИЯХ🍓")
        me = types.KeyboardButton("✨ОБО МНЕ✨")
        themes.row(drawing, me)
        themes.row(life, school)
        themes.row(music, preferences)
        mgc = bot.reply_to(message, "Хорошо, поговорим о чём-нибудь другом.", reply_markup=themes)
        bot.register_next_step_handler(mgc, choose)


#Отвечает за функционирование трёх кнопок, отвечающих за три различые вариации диалога.
@bot.message_handler(content_types=['text'])
def my_problems(message):
    #Отвечает за диалог на тему проблем в рисовании в целом.
    if message.text == "😥О СКИЛЛЕ В ЦЕЛОМ😥":
        opiniond = types.ReplyKeyboardMarkup()
        same = types.KeyboardButton("Жиза, у меня такое часто случается(к сожалению)...")
        good = types.KeyboardButton("Оу... Сожалею... Надеюсь, ты будешь сталкиваться с такими проблемами реже...")
        neutral = types.KeyboardButton("Ок, ичё?")
        negative = types.KeyboardButton("Ой, какие это проблемы? Вот у меня (длинное нытьё о своей жизни)...")
        opiniond.row(same, good)
        opiniond.row(neutral, negative)
        msgo = bot.send_message(message.chat.id, text=choice(drawing_dialog[0]["drawing"]["problems"]["realisation"]),
                                reply_markup=opiniond)
        bot.register_next_step_handler(msgo, reaction_dK)

    # Отвечает за диалог на тему проблемы с контуром рисунка.
    elif message.text == "😭О ЛАЙНЕ😭":
        opinionl = types.ReplyKeyboardMarkup()
        same = types.KeyboardButton("Жиза, я также с этим страдаю...")
        good = types.KeyboardButton("Оу... Сожалею...Надеюсь, ты скоро разовьёшься и эта проблема будет мучать тебя меньше...")
        neutral = types.KeyboardButton("Ок, ичё?")
        negative = types.KeyboardButton("Ой, какие это проблемы? Вот у меня (длинное нытьё о своей жизни)...")
        opinionl.row(same, good)
        opinionl.row(neutral, negative)
        msgo = bot.send_message(message.chat.id, text=choice(drawing_dialog[0]["drawing"]["problems"]["line"]),
                               reply_markup=opinionl)
        bot.register_next_step_handler(msgo, reaction_dK)

    # Отвечает за диалог на тему проблемы с цветом в рисунке.
    elif message.text == "😫О ПОКРАСЕ😫":
        opinionr = types.ReplyKeyboardMarkup()
        same = types.KeyboardButton("Жиза, я также над этим страдаю...")
        good = types.KeyboardButton(
            "Оу... Сожалею...Надеюсь, эти проблемы в скором тебя будут редко мучать...")
        neutral = types.KeyboardButton("Ок, ичё?")
        negative = types.KeyboardButton("Ой, какие это проблемы? Вот у меня (длинное нытьё о своей жизни)...")
        opinionr.row(same, good)
        opinionr.row(neutral, negative)
        msgo = bot.send_message(message.chat.id, text=choice(drawing_dialog[0]["drawing"]["problems"]["rendering"]),
                                reply_markup=opinionr)
        bot.register_next_step_handler(msgo, reaction_dK)


# Отвечает за функционирование трёх кнопок, отвечающих за три различые вариации диалога.
@bot.message_handler(content_types=['text'])
def my_succes(message):
    # Отвечает за диалог на тему опыта в рисовании.
    if message.text == "🌺ОБ ОПЫТЕ РИСОВАНИЯ В ЦЕЛОМ🌺":
        opiniono = types.ReplyKeyboardMarkup()
        same = types.KeyboardButton("У меня также.")
        good = types.KeyboardButton("У тебя ещё всё впереди, не расстраивайся!")
        neutral = types.KeyboardButton("Ок, ичё?")
        negative = types.KeyboardButton("Иш ты, ХВАСТАЕТСЯ ОНА! ТАК ЕЩЁ И НЫТЬ УМУДРЯЕТСЯ!")
        opiniono.row(same, good)
        opiniono.row(neutral, negative)
        msgo = bot.send_message(message.chat.id, text=choice(drawing_dialog[0]["drawing"]["succes"]["at_all"]),
                                reply_markup=opiniono)
        bot.register_next_step_handler(msgo, reaction_dP)

    # Отвечает за диалог на тему своего стиля рисования.
    elif message.text == "🍂О СВОЁМ СТИЛЕ🍂":
        opinionst = types.ReplyKeyboardMarkup()
        same = types.KeyboardButton("Жиза, у меня также стиль колошматит.")
        good = types.KeyboardButton("Интересно, УСПЕХОВ ТЕБЕ!")
        neutral = types.KeyboardButton("Ок, ичё?")
        negative = types.KeyboardButton("Ты думаешь, что кому-то сдались твои рассуждения? ОНИ НИКОМУ НЕ НУЖНЫ!")
        opinionst.row(same, good)
        opinionst.row(neutral, negative)
        msgo = bot.send_message(message.chat.id, text=choice(drawing_dialog[0]["drawing"]["succes"]["style"]),
                                reply_markup=opinionst)
        bot.register_next_step_handler(msgo, reaction_dP)

    # Отвечает за диалог на тему прогресса в рисовании.
    elif message.text == "🎀О СВОЁМ ПРОГРЕССЕ🎀":
        opinionp = types.ReplyKeyboardMarkup()
        same = types.KeyboardButton("Хепхе, у меня также...\n:_)")
        good = types.KeyboardButton("Не печалься ты, я в тебя верю!")
        neutral = types.KeyboardButton("Ок, ичё?")
        negative = types.KeyboardButton("ПРЕКРАТИ СВОЁ НЫТЬЁ!!!!")
        opinionp.row(same, good)
        opinionp.row(neutral, negative)
        msgo = bot.send_message(message.chat.id, text=choice(drawing_dialog[0]["drawing"]["succes"]["progress"]),
                                reply_markup=opinionp)
        bot.register_next_step_handler(msgo, reaction_dP)


#Отвечает за обработку реакций на рассказ о проблемах.
@bot.message_handler(content_types=['text'])
def reaction_dK(message):
    cont = types.ReplyKeyboardMarkup()
    yes = types.KeyboardButton("Да")
    no = types.KeyboardButton("Нет")
    cont.row(yes, no)

    # Отвечает за крайне положительный ответ.
    if message.text == "Жиза, у меня такое часто случается(к сожалению)..." or message.text == "Жиза, я также с этим страдаю..." or message.text == "Жиза, я также над этим страдаю...":
        msgrd = bot.reply_to(message, "Ура, ты меня понимаешь! Ну что, продолжим разговор о проблемах?", reply_markup=cont)
        bot.register_next_step_handler(msgrd, yes_no_dk)
    # Отвечает за положительный ответ.
    elif message.text == "Оу... Сожалею... Надеюсь, ты будешь сталкиваться с такими проблемами реже..." or message.text == "Оу... Сожалею...Надеюсь, ты скоро разовьёшься и эта проблема будет мучать тебя меньше..." or message.text == "Оу... Сожалею...Надеюсь, эти проблемы в скором тебя будут редко мучать...":
        msgrd = bot.reply_to(message, "Навряд-ли мне это поможет, но спасибо за поддержку!\nПоговорим ещё о проблемах?",
                             reply_markup=cont)
        bot.register_next_step_handler(msgrd, yes_no_dk)
    # Отвечает за нейтральный ответ.
    elif message.text == "Ок, ичё?":
        msgrd = bot.reply_to(message, "Х... Кхм, кхм...\nОдин известный орган через плечо... Мне немного обидно... Стоит ли вообще продолжать разговор на эту тему..?",
                             reply_markup=cont)
        bot.register_next_step_handler(msgrd, yes_no_dk)
    # Отвечает за негативный ответ.
    elif message.text == "Ой, какие это проблемы? Вот у меня (длинное нытьё о своей жизни)...":
        msgrd = bot.reply_to(message, "Знаешь, мне кажется, нам не стоит продолжать этот диалог... Имеешь какие-либо возражения?",
                             reply_markup=cont)
        bot.register_next_step_handler(msgrd, yes_no_dk)


#Отвечает за обработку реакций на рассказ об успехах.
@bot.message_handler(content_types=['text'])
def reaction_dP(message):
    cont = types.ReplyKeyboardMarkup()
    yes = types.KeyboardButton("Да")
    no = types.KeyboardButton("Нет")
    cont.row(yes, no)

    # Отвечает за крайне положительный ответ.
    if message.text == "У меня также." or message.text == "Жиза, у меня также стиль колошматит." or message.text == "Хепхе, у меня также...":
        msgrd = bot.reply_to(message, "А мы похожи\n;3\nПродолжим диалог?", reply_markup=cont)
        bot.register_next_step_handler(msgrd, yes_no_dp)
    # Отвечает за положительный ответ.
    elif message.text == "У тебя ещё всё впереди, не расстраивайся!" or message.text == "Интересно, УСПЕХОВ ТЕБЕ!" or message.text == "Не печалься ты, я в тебя верю!":
        msgrd = bot.reply_to(message, "Навряд-ли мне это поможет, но спасибо за поддержку!\nПоговорим ещё?",
                             reply_markup=cont)
        bot.register_next_step_handler(msgrd, yes_no_dp)
    # Отвечает за нейтральный ответ.
    elif message.text == "Ок, ичё?":
        msgrd = bot.reply_to(message,
                             "Х... Кхм, кхм...\nОдин известный орган через плечо... Мне немного обидно... Стоит ли вообще продолжать разговор на эту тему..?",
                             reply_markup=cont)
        bot.register_next_step_handler(msgrd, yes_no_dp)
    # Отвечает за негативный ответ.
    elif message.text == "ПРЕКРАТИ СВОЁ НЫТЬЁ!!!!" or message.text == "Ты думаешь, что кому-то сдались твои рассуждения? ОНИ НИКОМУ НЕ НУЖНЫ!" or "Иш ты, ХВАСТАЕТСЯ ОНА! ТАК ЕЩЁ И НЫТЬ УМУДРЯЕТСЯ!":
        msgrd = bot.reply_to(message,
                             "Знаешь, мне кажется, нам не стоит продолжать этот диалог... Имеешь какие-либо возражения?",
                             reply_markup=cont)
        bot.register_next_step_handler(msgrd, yes_no_dp)


#Отвечает за принятие решения о продолжении диалога на тему проблем в рисовании.
@bot.message_handler(content_types=['text'])
def yes_no_dk(message):
    if message.text == "Да":
        problem = types.ReplyKeyboardMarkup()
        realisation = types.KeyboardButton("😥О СКИЛЛЕ В ЦЕЛОМ😥")
        lineart = types.KeyboardButton("😭О ЛАЙНЕ😭")
        render = types.KeyboardButton("😫О ПОКРАСЕ😫")
        problem.row(realisation)
        problem.row(lineart, render)
        mg = bot.reply_to(message, "Ок, давай продолжим", reply_markup=problem)
        bot.register_next_step_handler(mg, my_problems)
    elif message.text == "Нет":
        draw = types.ReplyKeyboardMarkup()
        problems = types.KeyboardButton("💢О ПРОБЛЕМАХ💢")
        succes = types.KeyboardButton("🌷ОБ УСПЕХАХ🌷")
        back = types.KeyboardButton("👉НАЗАД👈")
        draw.row(problems, succes)
        draw.row(back)
        mg = bot.reply_to(message, "Понятненько...", reply_markup=draw)
        bot.register_next_step_handler(mg, draws)


#Отвечает за принятие решения о продолжении диалога на тему успехов в рисовании.
@bot.message_handler(content_types=['text'])
def yes_no_dp(message):
    if message.text == "Да":
        succes = types.ReplyKeyboardMarkup()
        style = types.KeyboardButton("🍂О СВОЁМ СТИЛЕ🍂")
        progress = types.KeyboardButton("🎀О СВОЁМ ПРОГРЕССЕ🎀")
        at_all = types.KeyboardButton("🌺ОБ ОПЫТЕ РИСОВАНИЯ В ЦЕЛОМ🌺")
        succes.row(at_all)
        succes.row(style, progress)
        mg = bot.reply_to(message, "Ок, давай продолжим", reply_markup=succes)
        bot.register_next_step_handler(mg, my_succes)
    elif message.text == "Нет":
        draw = types.ReplyKeyboardMarkup()
        problems = types.KeyboardButton("💢О ПРОБЛЕМАХ💢")
        succes = types.KeyboardButton("🌷ОБ УСПЕХАХ🌷")
        back = types.KeyboardButton("👉НАЗАД👈")
        draw.row(problems, succes)
        draw.row(back)
        mg = bot.reply_to(message, "Понятненько...", reply_markup=draw)
        bot.register_next_step_handler(mg, draws)


#Функция отвечает за функционал кнопок, отвечающих за вопросы к Олесе
@bot.message_handler(content_types=['text'])
def question(message):
    # Олеся называет свой возраст.
    if message.text == "Сколько тебе лет?":
        ques = types.ReplyKeyboardMarkup()
        age = types.KeyboardButton("Сколько тебе лет?")
        familia = types.KeyboardButton("Какая у тебя фамилия?")
        user = types.KeyboardButton("Почему у тебя юзерка странная. И ТГ указывает, что ты бот?")
        back = types.KeyboardButton("👉НАЗАД👈")
        ques.row(age, familia, user)
        ques.row(back)

        bot.reply_to(message, text=choice(olesya_dialog[0]["herself"]["age"]))
        msq = bot.send_message(message.chat.id, text="Какие ещё имеются вопросы", reply_markup=ques)
        bot.register_next_step_handler(msq, question)

    # Олеся НЕ называет свою фамилию.
    elif message.text == "Какая у тебя фамилия?":
        ques = types.ReplyKeyboardMarkup()
        age = types.KeyboardButton("Сколько тебе лет?")
        familia = types.KeyboardButton("Какая у тебя фамилия?")
        user = types.KeyboardButton("Почему у тебя юзерка странная. И ТГ указывает, что ты бот?")
        back = types.KeyboardButton("👉НАЗАД👈")
        ques.row(age, familia, user)
        ques.row(back)

        bot.reply_to(message, text=choice(olesya_dialog[0]["herself"]["familia"]))
        msq = bot.send_message(message.chat.id, text="Какие ещё имеются вопросы", reply_markup=ques)
        bot.register_next_step_handler(msq, question)

    # Появляются интересные изъяснения.
    elif message.text == "Почему у тебя юзерка странная. И ТГ указывает, что ты бот?":
        ques = types.ReplyKeyboardMarkup()
        age = types.KeyboardButton("Сколько тебе лет?")
        familia = types.KeyboardButton("Какая у тебя фамилия?")
        user = types.KeyboardButton("Почему у тебя юзерка странная. И ТГ указывает, что ты бот?")
        back = types.KeyboardButton("👉НАЗАД👈")
        ques.row(age, familia, user)
        ques.row(back)

        bot.reply_to(message, text=choice(olesya_dialog[0]["herself"]["user"]))
        msq = bot.send_message(message.chat.id, text="Какие ещё имеются вопросы", reply_markup=ques)
        bot.register_next_step_handler(msq, question)

    # Отвечает за функционал кнопки назад. Эта кнопка отвечает за возвращение на "главное меню".
    elif message.text == "👉НАЗАД👈":
        themes = types.ReplyKeyboardMarkup()
        drawing = types.KeyboardButton("💞О РИСОВАНИИ💞")
        life = types.KeyboardButton("🍃О ЖИЗНИ🍃")
        school = types.KeyboardButton("🥀О ШКОЛЕ🥀")
        music = types.KeyboardButton("🍄О МУЗЫКЕ🍄")
        preferences = types.KeyboardButton("🍓О ПРЕДПОЧТЕНИЯХ🍓")
        me = types.KeyboardButton("✨ОБО МНЕ✨")
        themes.row(drawing, me)
        themes.row(life, school)
        themes.row(music, preferences)
        msq = bot.reply_to(message, "Хорошо, поговорим о чём-нибудь другом.", reply_markup=themes)
        bot.register_next_step_handler(msq, choose)


# Начинается разговор на тему музыки. Олеся спрашивает у нас разрешение на выдачу ссылки на видео.
@bot.message_handler(content_types=['text'])
def musics(message):
    if message.text == "Продолжить диалог":
        m_y_n = types.ReplyKeyboardMarkup()
        y = types.KeyboardButton("Да")
        n = types.KeyboardButton("Нет")
        m_y_n.row(y, n)
        bot.send_message(message.chat.id, text=choice(music_dialog[0]["music"]["first_message"]))
        mgm = bot.reply_to(message, choice(music_dialog[0]["music"]["second_message"]), reply_markup=m_y_n)
        bot.register_next_step_handler(mgm, music_url)


# Обработка нашего ответа
@bot.message_handler(content_types=['text'])
def music_url(message):
    # Если мы согласимся, нам дадут ссылка на одно из 3 возможных видео, перекинув на "главное меню".
    if message.text == "Да":
        links = types.InlineKeyboardMarkup()
        linkc = choice(["https://www.youtube.com/watch?v=l-2hOKIrIyI", "https://www.youtube.com/watch?v=lTRiuFIWV54",
                        "https://www.youtube.com/watch?v=FgS5DEMg8K0"])
        link = types.InlineKeyboardButton(choice(["🌸", "💗", "💦"]), url=linkc)
        links.add(link)
        bot.send_message(message.chat.id, choice(music_dialog[0]["music"]["third_message"]["yes"]), reply_markup=links)

        themes = types.ReplyKeyboardMarkup()
        drawing = types.KeyboardButton("💞О РИСОВАНИИ💞")
        life = types.KeyboardButton("🍃О ЖИЗНИ🍃")
        school = types.KeyboardButton("🥀О ШКОЛЕ🥀")
        music = types.KeyboardButton("🍄О МУЗЫКЕ🍄")
        preferences = types.KeyboardButton("🍓О ПРЕДПОЧТЕНИЯХ🍓")
        me = types.KeyboardButton("✨ОБО МНЕ✨")

        themes.row(drawing, me)
        themes.row(life, school)
        themes.row(music, preferences)

        mgm = bot.reply_to(message, choice(music_dialog[0]["music"]["fourth_message"]), reply_markup=themes)
        bot.register_next_step_handler(mgm, choose)

    # Если мы дадим Олесе отказ, нам НЕ дадут ссылка на одно из 3 возможных видео, перекинув на "главное меню".
    elif message.text == "Нет":
        themes = types.ReplyKeyboardMarkup()
        drawing = types.KeyboardButton("💞О РИСОВАНИИ💞")
        life = types.KeyboardButton("🍃О ЖИЗНИ🍃")
        school = types.KeyboardButton("🥀О ШКОЛЕ🥀")
        music = types.KeyboardButton("🍄О МУЗЫКЕ🍄")
        preferences = types.KeyboardButton("🍓О ПРЕДПОЧТЕНИЯХ🍓")
        me = types.KeyboardButton("✨ОБО МНЕ✨")

        themes.row(drawing, me)
        themes.row(life, school)
        themes.row(music, preferences)
        mg = bot.reply_to(message, choice(music_dialog[0]["music"]["third_message"]["no"]), reply_markup=themes)
        bot.register_next_step_handler(mg, choose)


# Обрабатывет кнопки, отвечающие за вопросы на тему школы.
@bot.message_handler(content_types=['text'])
def schools(message):
    # Олеся говорит нам о том, что ей нравится в школе.
    if message.text == "Что тебе нравится в школе?":
        sch = types.ReplyKeyboardMarkup()
        like = types.KeyboardButton("Что тебе нравится в школе?")
        dislike = types.KeyboardButton("Что тебе в школе не нравится?")
        back = types.KeyboardButton("👉НАЗАД👈")
        sch.row(like, dislike)
        sch.row(back)

        bot.reply_to(message, choice(school_dialog[0]["school"]["like"]))
        msgo = bot.send_message(message.chat.id, text="Какие у тебя вопросы ещё остались?",
                                reply_markup=sch)
        bot.register_next_step_handler(msgo, schools)

    # Олеся говорит нам о том, что НЕ ей нравится в школе.
    elif message.text == "Что тебе в школе не нравится?":
        sch = types.ReplyKeyboardMarkup()
        like = types.KeyboardButton("Что тебе нравится в школе?")
        dislike = types.KeyboardButton("Что тебе в школе не нравится?")
        back = types.KeyboardButton("👉НАЗАД👈")
        sch.row(like, dislike)
        sch.row(back)

        bot.reply_to(message, choice(school_dialog[0]["school"]["dislike"]))
        msgo = bot.send_message(message.chat.id, text="Какие у тебя вопросы ещё остались?",
                                reply_markup=sch)
        bot.register_next_step_handler(msgo, schools)

    # Отвечает за функционал кнопки назад. Эта кнопка отвечает за возвращение на "главное меню".
    elif message.text == "👉НАЗАД👈":
        themes = types.ReplyKeyboardMarkup()
        drawing = types.KeyboardButton("💞О РИСОВАНИИ💞")
        life = types.KeyboardButton("🍃О ЖИЗНИ🍃")
        school = types.KeyboardButton("🥀О ШКОЛЕ🥀")
        music = types.KeyboardButton("🍄О МУЗЫКЕ🍄")
        preferences = types.KeyboardButton("🍓О ПРЕДПОЧТЕНИЯХ🍓")
        me = types.KeyboardButton("✨ОБО МНЕ✨")
        themes.row(drawing, me)
        themes.row(life, school)
        themes.row(music, preferences)
        msq = bot.reply_to(message, "Хорошо, поговорим о чём-нибудь другом.", reply_markup=themes)
        bot.register_next_step_handler(msq, choose)


# Обрабатывет кнопки, отвечающие за вопросы на тему предпочтений Олеси.
@bot.message_handler(content_types=['text'])
def preference(message):
    # Олеся говорит нам о своей любимой еде.
    if message.text == "Какую еду ты любишь?":
        pref = types.ReplyKeyboardMarkup()
        fav_food = types.KeyboardButton("Какую еду ты любишь?")
        fav_games = types.KeyboardButton("Какой твой любимый жанр в играх?")
        fav_films = types.KeyboardButton("Какие жанры фильмов ты любишь?")
        back = types.KeyboardButton("👉НАЗАД👈")
        pref.row(fav_food, fav_games, fav_films)
        pref.row(back)

        bot.reply_to(message, choice(preference_dialog[0]["preferences"]["food"]))
        msgo = bot.send_message(message.chat.id, text="Какие у тебя вопросы имеются?",
                                reply_markup=pref)
        bot.register_next_step_handler(msgo, preference)

    # Олеся говорит нам о своём любимом жанре игр.
    elif message.text == "Какой твой любимый жанр в играх?":
        pref = types.ReplyKeyboardMarkup()
        fav_food = types.KeyboardButton("Какую еду ты любишь?")
        fav_games = types.KeyboardButton("Какой твой любимый жанр в играх?")
        fav_films = types.KeyboardButton("Какие жанры фильмов ты любишь?")
        back = types.KeyboardButton("👉НАЗАД👈")
        pref.row(fav_food, fav_games, fav_films)
        pref.row(back)

        bot.reply_to(message, choice(preference_dialog[0]["preferences"]["game"]))
        msgo = bot.send_message(message.chat.id, text="Какие у тебя вопросы ещё остались?",
                                reply_markup=pref)
        bot.register_next_step_handler(msgo, preference)

    # Олеся говорит нам о своём любимом типе фильмов.
    elif message.text == "Какие жанры фильмов ты любишь?":
        pref = types.ReplyKeyboardMarkup()
        fav_food = types.KeyboardButton("Какую еду ты любишь?")
        fav_games = types.KeyboardButton("Какой твой любимый жанр в играх?")
        fav_films = types.KeyboardButton("Какие жанры фильмов ты любишь?")
        back = types.KeyboardButton("👉НАЗАД👈")
        pref.row(fav_food, fav_games, fav_films)
        pref.row(back)

        bot.reply_to(message, choice(preference_dialog[0]["preferences"]["films"]))
        msgo = bot.send_message(message.chat.id, text="Какие у тебя вопросы ещё остались?",
                                reply_markup=pref)
        bot.register_next_step_handler(msgo, preference)

    # Отвечает за функционал кнопки назад. Эта кнопка отвечает за возвращение на "главное меню".
    elif message.text == "👉НАЗАД👈":
        themes = types.ReplyKeyboardMarkup()
        drawing = types.KeyboardButton("💞О РИСОВАНИИ💞")
        life = types.KeyboardButton("🍃О ЖИЗНИ🍃")
        school = types.KeyboardButton("🥀О ШКОЛЕ🥀")
        music = types.KeyboardButton("🍄О МУЗЫКЕ🍄")
        preferences = types.KeyboardButton("🍓О ПРЕДПОЧТЕНИЯХ🍓")
        me = types.KeyboardButton("✨ОБО МНЕ✨")
        themes.row(drawing, me)
        themes.row(life, school)
        themes.row(music, preferences)
        msq = bot.reply_to(message, "Хорошо, поговорим о чём-нибудь другом.", reply_markup=themes)
        bot.register_next_step_handler(msq, choose)


# Обрабатывет кнопки, отвечающие за вопросы на тему жизни.
@bot.message_handler(content_types=['text'])
def your_life(message):
    # Олеся ведует нам о своей жизни.
    if message.text == "Расскажи о семье.":
        life = types.ReplyKeyboardMarkup()
        rest = types.KeyboardButton("Как вы отдыхаете?")
        family = types.KeyboardButton("Расскажи о семье.")
        you = types.KeyboardButton("Расскажи мне, как ты поживаешь.")
        back = types.KeyboardButton("👉НАЗАД👈")
        life.row(rest, family, you)
        life.row(back)

        bot.reply_to(message, choice(life_dialog[0]["life"]["family"]["first"]))
        bot.reply_to(message, choice(life_dialog[0]["life"]["family"]["second"]))
        img = open('my_family.png', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.reply_to(message, "Я очень люблю своего младшего братишку!\n:3")
        msgo = bot.send_message(message.chat.id, text="Если имеются какие-либо вопросы, спрашивай. Я не против.\n:3",
                                reply_markup=life)
        bot.register_next_step_handler(msgo, your_life)

    # Олеся рассказывает нам о членах своей семьи и показывает нам один из двух рисунков младшего брата.
    elif message.text == "Расскажи мне, как ты поживаешь.":
        life = types.ReplyKeyboardMarkup()
        rest = types.KeyboardButton("Как вы отдыхаете?")
        family = types.KeyboardButton("Расскажи о семье.")
        you = types.KeyboardButton("Расскажи мне, как ты поживаешь.")
        back = types.KeyboardButton("👉НАЗАД👈")
        life.row(rest, family, you)
        life.row(back)

        bot.reply_to(message, choice(life_dialog[0]["life"]["olesya"]))
        msgo = bot.send_message(message.chat.id, text="Если имеются какие-либо вопросы, спрашивай. Я не против.\n:3",
                                reply_markup=life)
        bot.register_next_step_handler(msgo, your_life)

    # Олеся рассказывает нам об отдыхе на море, делая это как подводку к показу ещё одного рисунка своего братика.
    elif message.text == "Как вы отдыхаете?":
        life = types.ReplyKeyboardMarkup()
        rest = types.KeyboardButton("Как вы отдыхаете?")
        family = types.KeyboardButton("Расскажи о семье.")
        you = types.KeyboardButton("Расскажи мне, как ты поживаешь.")
        back = types.KeyboardButton("👉НАЗАД👈")
        life.row(rest, family, you)
        life.row(back)

        bot.reply_to(message, choice(life_dialog[0]["life"]["vacation"]))
        img = open('brothers_painting.png', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.reply_to(message,"А вот и сам рисунок!\n:)")
        msgo = bot.send_message(message.chat.id, text="Какие у тебя вопросы ещё остались?",
                                reply_markup=life)
        bot.register_next_step_handler(msgo, your_life)

    # Отвечает за функционал кнопки назад. Эта кнопка отвечает за возвращение на "главное меню".
    elif message.text == "👉НАЗАД👈":
        themes = types.ReplyKeyboardMarkup()
        drawing = types.KeyboardButton("💞О РИСОВАНИИ💞")
        life = types.KeyboardButton("🍃О ЖИЗНИ🍃")
        school = types.KeyboardButton("🥀О ШКОЛЕ🥀")
        music = types.KeyboardButton("🍄О МУЗЫКЕ🍄")
        preferences = types.KeyboardButton("🍓О ПРЕДПОЧТЕНИЯХ🍓")
        me = types.KeyboardButton("✨ОБО МНЕ✨")
        themes.row(drawing, me)
        themes.row(life, school)
        themes.row(music, preferences)
        msq = bot.reply_to(message, "Хорошо, поговорим о чём-нибудь другом.", reply_markup=themes)
        bot.register_next_step_handler(msq, choose)


bot.polling(none_stop=True)