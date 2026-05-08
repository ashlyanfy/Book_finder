# Каталог книг по теме космоса и астрономии — источник для бота и сайта.

BOOKS_CATALOG = {
    'астрофизика': [
        {
            'title':  'Краткая история времени',
            'author': 'Стивен Хокинг',
            'link':   'https://loveread.ec/book-comments.php?book=73472',
            'desc':   'Классика популярной науки — от Большого взрыва до чёрных дыр.',
        },
        {
            'title':  'Астрофизика с высокой скоростью',
            'author': 'Нил Деграсс Тайсон',
            'link':   'https://loveread.ec/book-comments.php?book=74153',
            'desc':   'Вся астрофизика в одной небольшой и увлекательной книге.',
        },
        {
            'title':  'Элегантная вселенная',
            'author': 'Брайан Грин',
            'link':   'https://litlife.club/books/11038/read?page=1',
            'desc':   'Теория суперструн и скрытые измерения пространства-времени.',
        },
    ],
    'космология': [
        {
            'title':  'Высший замысел',
            'author': 'Стивен Хокинг, Леонард Млодинов',
            'link':   'https://loveread.ec/book-comments.php?book=73085',
            'desc':   'Современный взгляд на устройство и происхождение Вселенной.',
        },
        {
            'title':  'Параллельные миры',
            'author': 'Митио Каку',
            'link':   'https://loveread.ec/contents.php?id=73078',
            'desc':   'Мультивселенная, дополнительные измерения и будущее космоса.',
        },
        {
            'title':  'Первые три минуты',
            'author': 'Стивен Вайнберг',
            'link':   'https://loveread.ec/book-comments.php?book=87281',
            'desc':   'Классическое описание ранней Вселенной от нобелевского лауреата.',
        },
    ],
    'астрономия': [
        {
            'title':  'Космос',
            'author': 'Карл Саган',
            'link':   'https://loveread.ec/book-comments.php?book=73378',
            'desc':   'Великая книга о месте человека во Вселенной.',
        },
        {
            'title':  'Голубая точка. Космическое будущее человечества',
            'author': 'Карл Саган',
            'link':   'https://loveread.ec/book-comments.php?book=73380',
            'desc':   'Размышления о Земле как «бледной голубой точке» в космосе.',
        },
        {
            'title':  'Очерки о Вселенной',
            'author': 'Иосиф Шкловский',
            'link':   'https://litlife.club/books/99100/read?page=1',
            'desc':   'Классический советский научпоп от выдающегося астрофизика.',
        },
    ],
    'чёрные дыры': [
        {
            'title':  'Чёрные дыры и складки времени',
            'author': 'Кип Торн',
            'link':   'https://litlife.club/books/265797/read',
            'desc':   'История исследования чёрных дыр от автора Interstellar.',
        },
        {
            'title':  'Природа пространства и времени',
            'author': 'Стивен Хокинг, Роджер Пенроуз',
            'link':   'https://eanbur.unatlib.ru/items/59a1effa-9876-4076-ae81-c7ee337cab9e',
            'desc':   'Диалог двух гигантов о квантовой гравитации и сингулярностях.',
        },
        {
            'title':  'Смерть звезды и рождение чёрной дыры',
            'author': 'Игорь Новиков',
            'link':   'https://libcat.ru/knigi/nauka-i-obrazovanie/prochaya-nauchnaya-literatura/220390-igor-novikov-chyornye-dyry-i-vselennaya.html',
            'desc':   'Подробный разбор эволюции звёзд от российского астрофизика.',
        },
    ],
    'космонавтика': [
        {
            'title':  'Несущий огонь',
            'author': 'Майкл Коллинз',
            'link':   'https://www.livelib.ru/book/1001299244-carrying-the-fire-an-astronauts-journey-majkl-kollinz',
            'desc':   'Воспоминания пилота командного модуля «Аполлон-11».',
        },
        {
            'title':  'Дорога в космос',
            'author': 'Юрий Гагарин',
            'link':   'https://epizodsspace.airbase.ru/bibl/gagarin/doroga/gagarin-doroga_v_kosmos-61.pdf',
            'desc':   'Мемуары первого человека, побывавшего в космосе.',
        },
        {
            'title':  'Руководство астронавта по жизни на Земле',
            'author': 'Крис Хэдфилд',
            'link':   'https://loveread.ec/contents.php?id=45849',
            'desc':   'Канадский астронавт о жизни, работе и приоритетах в космосе.',
        },
    ],
}

# Синонимы — пользовательский ввод → ключ темы.
TOPIC_ALIASES = {
    'астро':       'астрофизика',
    'космос':      'астрономия',
    'звёзды':      'астрономия',
    'звезды':      'астрономия',
    'планеты':     'астрономия',
    'вселенная':   'космология',
    'мультивселенная': 'космология',
    'большой взрыв':   'космология',
    'дыр':         'чёрные дыры',
    'дыры':        'чёрные дыры',
    'космонавт':   'космонавтика',
    'астронавт':   'космонавтика',
    'гагарин':     'космонавтика',
    'аполлон':     'космонавтика',
}


def find_topic(user_input: str) -> str | None:
    """Ищет тему по тексту пользователя."""
    text = user_input.lower().strip()
    for topic in BOOKS_CATALOG:
        if topic in text:
            return topic
    for alias, topic in TOPIC_ALIASES.items():
        if alias in text:
            return topic
    return None


def format_book_list(topic: str) -> str:
    """Форматирует список книг по теме для Telegram."""
    books = BOOKS_CATALOG.get(topic, [])
    if not books:
        return ''
    lines = [f'*Книги по теме: {topic.capitalize()}*\n']
    for i, book in enumerate(books, start=1):
        lines.append(
            f'*{i}. {book["title"]}*\n'
            f'Автор: {book["author"]}\n'
            f'{book["desc"]}\n'
            f'[Читать / купить]({book["link"]})\n'
        )
    return '\n'.join(lines)
