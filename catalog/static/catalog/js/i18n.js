(function () {
  const DICT = {
    ru: {
      nav_home: 'Главная', nav_catalog: 'Каталог', nav_dashboard: 'Панель',
      nav_cta: 'Открыть бота',

      hero_title_1: 'Книги, которые',
      hero_title_2: 'расширяют горизонт',
      hero_lead: 'Подбираем литературу по астрофизике, философии, биологии и не только. Спросите бота — или загляните в каталог прямо сейчас.',
      hero_cta_primary: 'Открыть каталог',
      hero_cta_secondary: 'Запустить бота',
      hero_hint: 'Перетащите Юпитер, чтобы покрутить',

      stat_topics: 'тем', stat_books: 'книг', stat_247: 'в Telegram',

      section_topics_title: 'Темы каталога',
      section_topics_lead: 'Выберите направление — мы подскажем книги по нему.',
      feature_bot_title: 'Бот в Telegram',
      feature_bot_text: 'Напишите тему — получите подборку книг с описанием и ссылкой.',
      feature_site_title: 'Каталог на сайте',
      feature_site_text: 'Все темы в одном месте, удобный фильтр и быстрый просмотр.',
      feature_stats_title: 'Аналитика запросов',
      feature_stats_text: 'В панели управления видно, что ищут пользователи и какие темы в топе.',

      books_title: 'Книги по темам',
      books_lead: 'Выберите тему или пролистайте все подборки сразу.',
      filter_all: 'Все', book_link: 'Читать',
      empty_topic: 'По выбранной теме пока ничего нет.',

      dashboard_title: 'Панель управления',
      dashboard_lead: 'Статистика по запросам пользователей в Telegram-боте.',
      dash_total: 'всего запросов', dash_users: 'уникальных пользователей',
      dash_answered: 'отвечено', dash_pending: 'ожидают', dash_support: 'в поддержке',
      dash_recent: 'Последние запросы',
      th_when: 'Когда', th_user: 'Пользователь', th_query: 'Запрос', th_status: 'Статус',
      empty_queries: 'Запросов пока нет.',

      footer_copy: '© AstroBook · подбор книг',
      footer_made: 'Django + Three.js',

      'topic_астрофизика': 'Астрофизика',
      'topic_космология':  'Космология',
      'topic_астрономия':  'Астрономия',
      'topic_чёрные дыры': 'Чёрные дыры',
      'topic_космонавтика': 'Космонавтика',
    },
    en: {
      nav_home: 'Home', nav_catalog: 'Catalog', nav_dashboard: 'Dashboard',
      nav_cta: 'Open the bot',

      hero_title_1: 'Books that',
      hero_title_2: 'expand your horizon',
      hero_lead: 'We curate books on astrophysics, philosophy, biology and beyond. Ask the bot — or browse the catalog right now.',
      hero_cta_primary: 'Browse catalog',
      hero_cta_secondary: 'Launch the bot',
      hero_hint: 'Drag Jupiter to rotate it',

      stat_topics: 'topics', stat_books: 'books', stat_247: 'on Telegram',

      section_topics_title: 'Catalog topics',
      section_topics_lead: 'Pick a direction — we will suggest books for it.',
      feature_bot_title: 'Telegram bot',
      feature_bot_text: 'Send a topic — get a list of books with descriptions and links.',
      feature_site_title: 'Web catalog',
      feature_site_text: 'All topics in one place with a clean filter and quick browsing.',
      feature_stats_title: 'Query analytics',
      feature_stats_text: 'Dashboard shows what users search for and which topics trend.',

      books_title: 'Books by topic',
      books_lead: 'Pick a topic or scroll through all collections.',
      filter_all: 'All', book_link: 'Read',
      empty_topic: 'Nothing here yet for this topic.',

      dashboard_title: 'Dashboard',
      dashboard_lead: 'Statistics on user queries from the Telegram bot.',
      dash_total: 'total queries', dash_users: 'unique users',
      dash_answered: 'answered', dash_pending: 'pending', dash_support: 'support',
      dash_recent: 'Latest queries',
      th_when: 'When', th_user: 'User', th_query: 'Query', th_status: 'Status',
      empty_queries: 'No queries yet.',

      footer_copy: '© AstroBook · book recommendations',
      footer_made: 'Django + Three.js',

      'topic_астрофизика': 'Astrophysics',
      'topic_космология':  'Cosmology',
      'topic_астрономия':  'Astronomy',
      'topic_чёрные дыры': 'Black holes',
      'topic_космонавтика': 'Space exploration',
    },
  };

  const KEY = 'astrobook.lang';
  const initial = localStorage.getItem(KEY) ||
    (navigator.language || '').slice(0, 2).toLowerCase();
  let lang = DICT[initial] ? initial : 'ru';

  function apply(l) {
    lang = l;
    localStorage.setItem(KEY, l);
    document.documentElement.lang = l;
    const dict = DICT[l];
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const v = dict[el.dataset.i18n];
      if (v != null) el.textContent = v;
    });
    document.querySelectorAll('.lang-switch [data-lang]').forEach((b) => {
      b.classList.toggle('is-active', b.dataset.lang === l);
    });
  }

  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.lang-switch [data-lang]');
    if (btn) apply(btn.dataset.lang);
  });

  apply(lang);
})();
