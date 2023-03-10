import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.state import StatesGroup, State
from sqlalchemy import insert, select, update
import emoji
from bot.database.main import Users, async_session
from bot.misc.util import accept
from bot.keyboards.inline import inline_kb1, inline_kb2

base = [
    ':red_heart: Что бы не случилось, знай, я всегда на твоей стороне и окажу тебе любую помощь и поддержку. Просто дай мне знать. :red_heart::kiss_mark:',
    ':red_heart: Мне жаль, что тебе пришлось столкнуться с этим, но ты самый сильный человек из всех, кого я знаю, ты справишься. :raised_fist::face_blowing_a_kiss:',
    ':red_heart: Я понимаю, как тяжело тебе сейчас, но ты можешь на меня положиться. Поверь, скоро все наладится, я буду рядом, чтобы помочь тебе пережить это. :folded_hands:',
    ':red_heart: Выход есть из любой ситуации. Мы вместе справимся со всеми трудностями и потом будем вспоминать это время с улыбкой. :kissing_face_with_closed_eyes:',
    'Сейчас тебе очень трудно, но вспомни, ты уже справлялся с подобными ситуациями, значит справишься и сейчас, ты такой сильный. :smiling_face_with_smiling_eyes::red_heart:',
    'Я горжусь тобой, как ты справляешься со всеми трудностями.:red_heart:',
    'Как бы трудно тебе не было сегодня, знай, что я не покину тебя и всегда буду рядом, как бы тяжело тебе не пришлось. :woman_and_man_holding_hands::red_heart:',
    ':red_heart: У нас с тобой и радость и беда — одна на двоих, не скрывай свои чувства, я в любом случае помогу тебе и поддержу тебя.',
    'Дорогу осилит идущий, давай пройдем этот путь вместе с тобой, чтобы эта дорога была более легкой и приятной для тебя. Ведь вдвоем легче преодолеть любые трудности. :kiss::red_heart:',
    ':red_heart: Мне больно смотреть на тебя в таком состоянии. Я переживаю и за тебя и желаю, чтобы все твои трудности закончились как можно скорее. Я помогу тебе в этом.',
    ':red_heart: Главное — не паникуй, помни, что паника вносит негатив, только сохранение спокойствия поможет сконцентрироваться на успехе. :thumbs_up:',
    'Эта работа помогла тебе приобрести много замечательных навыков, которые будут полезны в дальнейшем. :face_blowing_a_kiss::red_heart:',
    ':red_heart: Я вижу, что это так важно для тебя. Я хочу помочь тебе в достижении твоей цели.',
    'Верь тем, кто любит тебя. Они знают твои сильные стороны и ценят тебя за них, сейчас как никогда нужно поверить в себя.:red_heart:',
    ':red_heart: Ты не должен справляться со всем в одиночку. Не бойся попросить о помощи, позволь тем, кто любит тебя сделать это вместе с тобой. :winking_face:',
    'Ты не обязан решать все эти вопросы прямо сейчас. Успокойся, составь план и сосредоточься на маленьких шагах, так ты сможешь все.:red_heart:',
    'Если тебе кажется, что сейчас ты попал в тупик, попробуй развернуться и пойти в другом направлении. Иногда конец — это новое начало. :cowboy_hat_face::red_heart:',
    ':red_heart: Я верю, что при твоих навыках и опыте ты сможешь добиться всего, чего пожелаешь, а я буду рядом, чтобы поддержать тебя. :kiss_mark:',
    'Возможно, у тебя не получается это, так как ты слишком устал. Отдохни, провели время приятно и попробуй еще раз.:red_heart:',
    ':red_heart: Не вини себя во всем, ты не должен брать на себя чрезмерную ответственность, ты сделал все, что было в твоих силах. :kiss_mark:',
    ':red_heart: Хоть сейчас тебя нет рядом со мной, ты в моих мечтах и мне так хочется поскорее оказаться в твоих объятиях. :revolving_hearts:',
    ':red_heart: Каждую секунду всех тех дней, когда тебя нет рядом со мной, я не перестаю думать о тебе и жду, когда мы снова встретимся.',
    ':red_heart: Как бы далеко ты сейчас не находился, сколько бы километров нас не разделяли, мое сердце всегда остается с тобой. :heart_decoration:',
    'Несмотря на то, что сейчас мы так далеко друг от друга, настоящей любви не километры — не помехи. :kiss_mark::red_heart:',
    ':red_heart: Не люблю ждать, но, если результатом ожидания будет наша встреча, я готова ждать тебя вечно.',
    ':red_heart: Сложно быть так далеко от тебя, но меня утешает только мысль, что наша разлука не навсегда. Скучаю по тебе каждую минуту. :kissing_face_with_closed_eyes:',
    ':red_heart: Даже когда нас разделяют тысячи километров, ты остаешься самым близким человеком для меня.',
    'Так трудно скучать по тебе ежедневно, но я успокаиваю себя мыслью, что каждый день приближает нашу с тобой встречу.:red_heart:',
    ':red_heart: Расстояние между нами — это не преграда, а всего лишь проверка, насколько крепкими могут быть наши чувства.',
    'Просыпаться без тебя тяжело, но когда я вспоминаю, что ты скоро напишешь мне, мне становится легче.:red_heart:',
    ':red_heart: Я надеюсь, что ты принимаешь все нужные лекарства и соблюдаешь режим. Поскорее поправляйся! :flexed_biceps:',
    'Как бы я хотела взять твою болезнь на себя, чтобы облегчить твои старания. Это то, что я хочу сейчас. :pensive_face::red_heart:',
    ':red_heart: Моя единственная мечта — увидеть тебя здоровым и веселым. Надеюсь, она сбудется в скором времени.',
    'Как только ты поправишься, займемся тем, что ты так любишь. Я верю, что уже скоро ты будешь готов к этому. :camping::winking_face::red_heart:',
    'Поделись со мной своим состоянием, для меня важно, как ты себя чувствуешь. Ведь твой покой и хорошее самочувствие — самое главное для меня.:red_heart:',
    ':red_heart: Когда я вижу тебя таким, я чувствую боль. Скорее поправляйся, я очень переживаю за твое самочувствие. :folded_hands:',
    ':red_heart: Когда самому прекрасному человеку плохо, даже погода портится, наверное, поэтому сегодня целый день идет дождь.',
    ':red_heart: Постарайся поправиться как можно скорее, я не могу найти себе места, когда вижу, как ты страдаешь. :red_heart:',
    ':red_heart: Крепко обнимаю и целую, может быть, моя забота поможет тебе почувствовать себя лучше. Выздоравливай скорее.',
    'Когда тебе плохо, я больше ни о чем не могу думать, у меня все валится из рук. Постарайся как можно скорее прийти в себя.:red_heart:',
    ':red_heart: Все пройдет отлично, иначе и не может быть.\xa0 Запасись силами и оптимизмом, я верю в тебя.',
    ':red_heart: Желаю тебе легкой и успешной операции, я знаю, что ты нервничаешь, но верю, что все пройдет, как нельзя лучше. :relieved_face:',
    'Всем сердцем желаю, чтобы все прошло благополучно, очень переживаю за тебя, сил и тебе и веры в лучшее.:red_heart:',
    ':red_heart: Главное — ничего не бойся и верь только в хорошее, уже скоро все это останется позади. :face_blowing_a_kiss:',
    ':red_heart: Желаю тебе, чтобы операция прошла успешно, и ты поскорее вернулся к здоровой полноценной жизни.',
    'Я знаю, что ты сейчас очень волнуешься, но твой сильный организм сможет справится с этим, все пройдет благополучно. :flexed_biceps::red_heart:',
    'Ничего не бойся и старайся верить в самое лучшее. Ведь вера и оптимизм помогут твоему организму преодолеть все трудности.:red_heart:',
    'Впереди тебя ждет сложное и важное событие, но я хочу, чтобы ты успокоился и верил, что все пройдет хорошо, чтобы не случилось, я буду рядом.:red_heart:',
    ':red_heart: Твое волнение — это нормально, но поводов для беспокойства нет, все пройдет лучшим образом и уже скоро будет позади. :kissing_face_with_smiling_eyes:',
    'Отбрось переживания, все пройдет замечательно, и я буду рядом с тобой.:red_heart:',
    'Ты самый дорогой человек для меня, каждый день я вспоминаю моменты из нашей жизни и жду, когда мы снова будем рядом. :kiss::red_heart:',
    ':red_heart: Я так устала от этих писем и сообщений, от того, что не могу просто тебя увидеть, но совсем скоро мы снова будем рядом. :red_heart:',
    ':red_heart: Так скучаю по временам, когда мы все время проводили вместе. Не могу поверить, что мы не увидимся еще столько месяцев.',
    ':red_heart: Когда мне очень грустно, я думаю о тебе и вспоминаю, что тебе там сейчас еще сложнее. Но мы сможем преодолеть это и снова быть вместе. :face_blowing_a_kiss:',
    ':red_heart: Грустно, что я могу сейчас только смотреть на твое фото, но смогу обнять тебя еще много месяцев.',
    ':red_heart: Я так скучаю и отсчитываю дни до нашей новой встречи. :kiss_mark:',
    'Сейчас для нас обоих трудный период, но давай постараемся взять себя в руки и пережить его достойно, чтобы снова обрести друг друга.:red_heart:',
    'Каждую ночь я засыпаю в слезах, но меня утешает то, что это скоро закончится. :folded_hands::red_heart:',
    'Мне так хочется увидеть тебя, обнять, услышать твой голос, но пока что мне остается только каждый день смотреть на твое фото.:red_heart:',
    ':red_heart: Разлука невыносима для нас обоих, но мы справимся с этим, ведь рассвет наступает даже после самой темной ночи. :sunrise::red_heart:',
    ':red_heart: Вместе с этим сообщением я отправляю тебе свой позитив и веру в лучшее.',
    ':red_heart: Не концентрируйся на плохом, старайся думать о том, что приносит тебе радость. Я с тобой.',
    ':red_heart: Даже если от тебя отвернется весь мир, я буду с тобой. :face_blowing_a_kiss:',
    'Пусть этот день подарит тебе только самые светлые и позитивные эмоции. Каждый день может стать лучшим в твоей жизни.:red_heart:',
    'Я хочу зарядить тебя оптимистичным настроем и позитивом, ты слышишь, это удача уже стучит в твою дверь.:red_heart:',
    'Главное верь, что все будет в порядке, поставь перед собой установку, и тогда все будет отлично.:red_heart:',
    'Не думай о завтра, живи счастливым настоящим, даже если сперва тебе показалось, что не такое уж оно и счастливое.:red_heart:',
    ':red_heart: Я думаю о тебе, надеюсь, что у тебя все в порядке, и все складывается так, как планируешь. Хочу сейчас быть рядом.',
    ':red_heart: Начинаю каждый день, думая о тебе. Это так приятно, просыпаться и вспоминать, что у меня есть ты. С тобой я становлюсь счастливее с каждым днем.',
    'Не могу на чем-то сосредоточиться, так как весь день думаю о тебе, скучаю и жду нашей с тобой скорейшей встречи.:red_heart:',
    'Даже если ты сам не веришь в себя, знай, что я верю, и всегда буду верить, что бы не произошло.:red_heart:',
    'А знаю, что ты справишься с этим, ведь ты никогда не теряешь силу духа. Я ценю в тебе это качество.:red_heart:',
    ':red_heart: Прошу, пообещай мне, что ты не забудешь — ты гораздо сильнее, смелее и талантливее, чем тебе кажется в трудные минуты.',
    ':red_heart: Если очень хочется, ты можешь пожаловаться и даже поплакать. Это не делает тебя слабым человеком. Главное — не сдавайся.',
    ':red_heart: Каким бы ни был твой выбор и как бы ты не поступил, я всегда буду с тобой и поддержу любой твой выбор. :red_heart:',
    ':red_heart: Твоя сила воли и вера мотивируют меня и помогают мне становится лучше с каждым днем, спасибо что ты есть.',
    ':red_heart: Не падай духом, вселенная не дает таких испытаний, которые мы бы не могли пройти. Ты сильный и справишься с этим.',
    'Запомни: для меня ты всегда будешь самым лучшим, даже в те дни, когда ты чувствуешь себя опустошенным и разбитым, я всегда поддержу тебя.:red_heart:',
    ':red_heart: Это нормально, что тебе грустно, каждый человек имеет право немного похандрить. Главное — не сломайся, ты удивительный человек.',
    ':red_heart: Твоя самая большая сила не в том, чтобы никогда не падать, а в том, чтобы уметь подняться после каждого падения.',
    ':red_heart: Твоя поддержка очень много для меня значит, спасибо, что ты всегда оказываешься рядом и даешь мне энергию и силы.',
    ':red_heart: У меня нет слов, чтобы передать тебе свою благодарность, с тобой я становлюсь лучше, ты даешь мне свет и силы двигаться дальше.',
    'Спасибо тебе за то, что с тобой моя жизнь изменилась, она словно озарилась светом и приобрела новый смысл.:red_heart:',
    ':red_heart: Спасибо, что ты есть, я не устаю благодарить небо за то, что мы познакомились, каждый день общения с тобой для меня счастье.',
    ':red_heart: Спасибо тебе за отзывчивость и за то, что ты всегда рядом, когда я в тебе нуждаюсь, ты все, что нужно мне в этой жизни.',
    ':red_heart: Ты — светлый лучик, который есть в моей жизни, который освещает мою жизнь даже в самый темный день. Спасибо, что ты есть.',
    'Не представляю, как выразить тебе мою благодарность. Ты делаешь мою жизнь ярче и помогаешь радоваться каждому ее дню.:red_heart:',
    'Сегодня так сложно найти человека, который всегда поддержит и искреннее порадуется за тебя, спасибо, что ты стал для меня этим человеком.:red_heart:',
    'Спасибо тебе, что ты вошел в мою жизнь и стал моим новым миром, раскрасил его новыми красками. Ты много значишь для меня.:red_heart:',
    ':red_heart: Хочу сказать тебе спасибо за то, что ты терпишь все мои капризы и всегда остаешься рядом со мной, несмотря ни на что.',
    ':red_heart: Я не могу описать словами, как много ты для меня значишь. :purple_heart:',
    'Ты такой сильный и целеустремленный, я горжусь твоими достижениями. :smiling_face_with_heart-eyes::red_heart:',
    ':red_heart: Этот день — всего лишь маленькая глава из твоей жизни, перелистни ее и забудь. Завтра будет новый день и ты сможешь написать новую главу своей жизни.',
    ':red_heart: Если тебе плохо, просто скажи мне. Даже если я не смогу помочь, я просто буду рядом с тобой. :kiss_mark:',
    ':red_heart: Когда тебе вдруг захочется сдаться просто вспомни, почему ты держался до сих пор.',
    'Пора привыкнуть, что ничего не получается сразу. Если не получилось с первой попытки, просто попробуй еще один раз. :winking_face::red_heart:',
    ':red_heart: Тебе кажется, что твоя жизнь сломана и нет возможности ее склеить, но, может быть, это повод начать стоить все заново.',
    'Сейчас в тебе говорят эмоции, но прислушайся к своему разуму, это поможет тебе сделать правильный выбор. :thumbs_up::red_heart:',
    ':red_heart: Не отчаивайся, ошибок не совершает только тот, кто ничего не делает.',
    ':red_heart: Как бы плохо тебе не было, не огорчайся. После грозы солнце светит еще ярче, так и в твоей жизни все станет хорошо.',
    'Желаю, чтобы дорога была легкой, попутчики — приятными, и чтобы все задуманное получилось.:red_heart:',
    'Желаю тебе без затруднений добраться до конечного пункта маршрута и поскорее вернуться домой, жду, скучаю.:red_heart:',
    ':red_heart: Пусть твоя дорога будет ровной и благополучной, а все задуманное поскорее исполнится, нет ничего важнее, чем возвращение домой.',
    'Желаю тебе легкой, быстрой и безопасной дороги, пусть все светофоры будут зелеными, а препятствий и задержек будет поменьше.:red_heart:',
    'В дороге не спеши и не нервничай. Спокойствие и хорошее настроение сделает твою дорогу безопасной и веселое, и она пролетит незаметно.:red_heart:',
    'Соболезную твоей утрате. Сейчас тебе тяжело, но я хочу чтобы ты знал, ты всегда можешь рассчитывать на мою поддержку.:red_heart:',
    'Позволь принести тебе мои соболезнования, у меня нет слов, чтобы выразить огорчение от твоей утраты, я буду молиться за вас.:red_heart:',
    'Мне так жаль, что тебе пришлось столкнуться с таким горем. Не представляю, что ты чувствуешь сейчас.:red_heart:',
    'Я знаю, как тяжело тебе сейчас, позволь мне поддержать тебя и быть рядом.:red_heart:',
    'Сочувствую твоей утрате, я могу для тебя что-то сделать.:red_heart:']

scheduler = AsyncIOScheduler()


class UserState(StatesGroup):
    default = State()
    awaiting = State()
    receiving = State()
    undefined = State()


hello_text = f'Приветик) Я Аня\n'\
f'Хочу поддержать тебя в трудную минуту👉👈\n\n'\
f'Я могу:\n\n'\
f'/send - начать раз в час отправлять утешающие сообщения\n'\
f'/stop - прекратить так делать\n'\
f'/add - добавить фразу, которую ты бы хотел от меня когда-то услышать\n'\
f'/delete - или удалить фразу, которая тебе не понравилась\n'\
f'/like - показать что фраза понравилась 👉👈'


async def start(msg: Message):
    async with async_session() as session:
        check = await session.execute(select(Users.name).where(Users.name == msg.from_user.username))
        await session.commit()
    if check.scalars().all() != []:
        await msg.answer(hello_text)
    else:
        await msg.answer(hello_text+'\nА пока скажи какой твой любимый цвет', reply_markup=inline_kb1)
    await UserState.undefined.set()


async def process_callback_button1(callback_query: CallbackQuery):
    data = insert(Users).values(name=callback_query.from_user.username,
                                sentences=str([w.replace('red', callback_query.data) for w in base]),
                                dislikes=str([]),
                                favourites=str([]))
    await accept(data)
    await callback_query.message.answer("Спасибо за ответ. Я это запомню☺️")
    await UserState.undefined.set()


async def add(msg: Message):
    await msg.answer('Что бы тебе хотелось услышать?')
    await UserState.awaiting.set()


async def updating(msg: Message):
    async with async_session() as session:
        phrases = await session.execute(select(Users.sentences).where(Users.name == msg.from_user.username))
        await session.commit()
    data = eval(phrases.scalars().all()[0])
    data.append(msg.text)
    upd = update(Users).where(Users.name == msg.from_user.username).values(sentences=str(data))
    await accept(upd)
    await UserState.undefined.set()
    await msg.answer('Я учту, что для тебя это важно')


async def delete(msg: Message, state: UserState.receiving):
    phr = await state.get_data()
    async with async_session() as session:
        phrases = await session.execute(select(Users.sentences).where(Users.name == msg.from_user.username))
        dislikes = await session.execute(select(Users.dislikes).where(Users.name == msg.from_user.username))
        await session.commit()
    data = eval(phrases.scalars().all()[0])
    dislikes = eval(dislikes.scalars().all()[0])
    data.remove(phr['last'])
    dislikes.append(phr['last'])
    upd = update(Users).where(Users.name == msg.from_user.username).values(sentences=str(data), dislikes=str(dislikes))
    await accept(upd)
    await msg.answer('Хорошо, больше я так не скажу')


async def like(msg: Message, state: UserState.receiving):
    phr = await state.get_data()
    async with async_session() as session:
        likes = await session.execute(select(Users.favourites).where(Users.name == msg.from_user.username))
        await session.commit()
    likes = eval(likes.scalars().all()[0])
    likes.append(phr['last'])
    upd = update(Users).where(Users.name == msg.from_user.username).values(favourites=str(likes))
    await accept(upd)
    await msg.answer('Я буду чаще так говорить 💙')


async def stop(msg: Message):
    scheduler.remove_all_jobs()
    await msg.answer('Рада, что тебе перестало это быть нужным🫂')
    await UserState.undefined.set()


async def send(msg: Message):
    await msg.answer('Выбери интервал', reply_markup=inline_kb2)
    await UserState.receiving.set()


async def choose_time(callback_query: CallbackQuery, state: UserState.receiving):
    if scheduler.get_jobs():
        scheduler.remove_all_jobs()
    async with async_session() as session:
        phrases = await session.execute(select(Users.sentences).where(Users.name == callback_query.from_user.username))
    data = eval(phrases.scalars().all()[0])
    mesg = random.choice(data)
    await callback_query.message.answer(emoji.emojize(mesg))
    await state.update_data(last=mesg)
    scheduler.add_job(choose_time, "interval", seconds=int(callback_query.data), args=(callback_query, state))


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands=['start'], state=None)
    dp.register_message_handler(send, commands=['send'], state=[UserState.undefined, UserState.receiving])
    dp.register_message_handler(add, commands=['add'], state=UserState.undefined)
    dp.register_message_handler(updating, state=UserState.awaiting)
    dp.register_message_handler(stop, commands=['stop'], state=UserState.receiving)
    dp.register_message_handler(delete, commands=['delete'], state=UserState.receiving)
    dp.register_message_handler(like, commands=['like'], state=UserState.receiving)
    dp.register_callback_query_handler(process_callback_button1, lambda c: c.data, state=UserState.undefined)
    dp.register_callback_query_handler(choose_time, lambda a: a.data, state=UserState.receiving)
