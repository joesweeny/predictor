"""Hook for running console module as a script"""

from predictor.console.console import cli
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    root = os.path.join(os.path.dirname(__file__), '../..')
    load_dotenv(os.path.join(root, '.env'))
    cli()
