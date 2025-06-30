import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath())))

from main import app
from mangum import Mangum

handler = Mangum(app)
