import os
from dotenv import load_dotenv

load_dotenv()

os.environ['FLASK_ENV'] = 'test'
os.environ['DB_HOST'] = os.getenv('DB_HOST', 'mariadb')
os.environ['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_TEST_NAME', 'app_db_test')}"
)