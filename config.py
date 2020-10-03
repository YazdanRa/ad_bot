# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

# Create in-memory database
DATABASE_FILE = 'bot.db'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:24111999@/adsbot?host=127.0.0.1'
SQLALCHEMY_ECHO = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
