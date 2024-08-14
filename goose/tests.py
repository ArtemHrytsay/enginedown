from django.test import TestCase
from pathlib import Path

import os


path = Path(__file__).parent.absolute()
os.chdir(path)

print(path)
