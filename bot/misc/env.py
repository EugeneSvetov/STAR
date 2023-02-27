from typing import Final
import os
from dotenv import load_dotenv

load_dotenv()

class TgKeys:
    TOKEN: Final = os.getenv('TOKEN')
