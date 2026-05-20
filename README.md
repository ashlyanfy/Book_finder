# AstroBook — A Telegram Bot and Web Platform for Selecting Books About Space

Website: https://astrobook-web.onrender.com/
Telegram bot: @books1_helper_bot
https://astrobook-bot.onrender.com

---

## Project Description

**AstroBook** is a hybrid chatbot and web platform for selecting books on astronomy, astrophysics, and cosmology. Users select a topic of interest through a Telegram bot or website and receive a catalog of books with descriptions, authors, and links for reading.

The project demonstrates the integration of the Telegram Bot API with Django, a task scheduler, database storage, and a fully functional web interface with 3D graphics.

---

## Features

### Telegram bot
- Commands `/start`, `/help`, `/topics`, `/remind`
- Inline buttons for selecting a topic
- Book catalog with descriptions and links
- Scheduled reading reminders (daily/weekly)
- Saving all requests to the database
- Forwarding complex questions to support
- Handling empty input and unknown commands

### Website
- Landing page with an interactive 3D planet (Three.js)
- Book catalog with topic filtering
- Language switcher RU / EN
- Responsive design

### Control panel
- Statistics: total requests, unique users, answered, pending
- Top 5 most popular requests
- Table of all requests filtered by status
- Reply to users directly from the browser – the response is automatically sent to Telegram

### Background tasks (APScheduler)
- Check reminders every minute
- Automatically send support replies every 10 seconds

---

## Book Catalog

| Topic | Number of books |
|---|---|
| 🌟 Astrophysics | 6 |
| 🌌 Cosmology | 7 |
| 🔭 Astronomy | 6 |
| 🕳️ Black Holes | 4 |
| 👨‍🚀 Space and Humanity | 5 |
| ⚛️ Quantum Physics | 3 |
| 🌀 Theory of Relativity | 3 |
| 🪐 Planets and the Solar System | 4 |
| **Total** | **38 books** |

---

## Project Structure
book_finder/
├── manage.py # Django management utility
├── requirements.txt # Project dependencies
├── .env # Environment variables (do not commit)
├── README.md # Documentation
├── db.sqlite3 # Database (created automatically)
│
├── book_finder/ # Django settings
│ ├── settings.py # Project configuration
│ ├── urls.py # Main routes
│ └── wsgi.py # WSGI entry point
│
├── catalog/ # Django Application
│ ├── models.py # Models: UserQuery, Reminder, Notification
│ ├── admin.py # Django Admin Setup
│ ├── views.py # Page Controllers
│ ├── urls.py # Application Routes
│ ├── migrations/ # Database Migrations
│ └── templates/
│ └── catalog/
│ ├── index.html # Landing Page with 3D Planet
│ ├── books.html # Book Catalog
│ └── dashboard.html # Control Panel
│
└── bot/ # Telegram bot
├── bot.py # Main bot file
├── books_data.py # Book catalog and search functions
└── scheduler.py # Task scheduler (APScheduler)

---

## ⚙️ Technologies

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11 | Primary language |
| Django | 4.2.7 | Web framework, ORM, Admin |
| pyTelegramBotAPI | 4.14.0 | Telegram Bot API |
| APScheduler | 3.10.4 | Background task scheduler |
| SQLite | — | Database |
| Three.js | r128 | 3D graphics on the website |
| python-dotenv | 1.0.0 | Environment Variables |
| Requests | 2.31.0 | HTTP Requests |

---

## 🔧 Installation and Run

### 1. Clone the repository

```bash
git clone https://github.com/username/book_finder.git
cd book_finder
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the root Project:

```env
BOT_TOKEN=your_token_from_BotFather
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
```

You can get a bot token from [@BotFather](https://t.me/BotFather) on Telegram.

Generate a Django secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 5. Apply migrations

```bash
python manage.py makemigrations catalog
python manage.py migrate
```

### 6. Create an administrator

```bash
python manage.py createsuperuser
```

### 7. Start the server (Terminal 1)

```bash
python manage.py runserver
```

### 8. Run the bot (Terminal 2)

```bash
python bot/bot.py
```

---

## 💬 Bot examples
User: /start
Bot: 👋 Hello! I'm AstroBook Bot — I'll help you find books on astronomy.
[Shows inline buttons with topics]
User: [clicks the 🌟 Astrophysics button]
Bot: 📚 Books on the topic: Astrophysics
1. A Brief History of Time (1988)
✍️ Stephen Hawking
📖 From the Big Bang to Black Holes...
🔗 Read / Buy
User: I want to read about space
Bot: 📚 Books
