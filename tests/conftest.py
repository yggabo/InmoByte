import os
from dotenv import load_dotenv

load_dotenv()

os.environ['FLASK_ENV'] = 'test'