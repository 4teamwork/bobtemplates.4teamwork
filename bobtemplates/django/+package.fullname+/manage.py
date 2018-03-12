import os
import sys
from dotenv import load_dotenv

basedir = os.path.dirname(os.path.abspath(__file__))
envfile = os.path.join(basedir, '.env')

if not os.path.isfile(envfile):
    envfile = os.path.join(basedir, '.env.development')

load_dotenv(envfile)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
