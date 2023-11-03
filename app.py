# encoding: utf-8

import os
import urllib.request
import xmltodict
import json
import logging
import glob

# Environment Variables
STATION_NAME = os.environ['STATION_NAME']
PROGRAM_TITLE = os.environ['PROGRAM_TITLE']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
USER = os.environ['USER']
DIRNAME = os.environ['DIRNAME']
TIME_TABLE = os.environ['TIME_TABLE'] #'https://radiko.jp/v3/program/today/JP13.xml'

# Constant
SHELL = './rec_radiko_ts.sh'
BASE = 'https://radiko.jp/#!/ts/{code}/{time}'

# Setup Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)

# Start
logger.info('START')

# Get Program
logger.info('GET PROGRAM')
request = urllib.request.Request(TIME_TABLE)
with urllib.request.urlopen(request) as response:
    xml = response.read()
    parsed_xml = xmltodict.parse(xml)

# Parse
logger.info('PARSE')
try:
    station = list(filter(lambda x: x['@id'] == STATION_NAME, parsed_xml['radiko']['stations']['station']))[0]
    programs = station['progs']['prog']
    program = list(filter(lambda x: PROGRAM_TITLE in x['title'], programs))[0]
    url = BASE.format(code=STATION_NAME, time=program['@ft'])
    logger.info(f'URL: {url}')
except Exception as e:
    logger.error(e)

# Download
logger.info('DOWNLOAD')
os.system(f'{SHELL} -u {url}')
os.system('ls -hl')

# Convert to MP3
filenames = glob.glob('*.m4a')
filename = filenames[0].split('.')[0]
logger.info(filename)
command_convert = f'ffmpeg -i {filename}.m4a -ab 64k {filename}.mp3'
logger.info(command_convert)
os.system(command_convert)

# Send by SCP
logger.info('SEND BY SCP')
command_mkdir = f'sshpass -e ssh -o StrictHostKeyChecking=no -p {PORT} mkdir -p {DIRNAME}'
logger.info(command_mkdir)
os.system(command_mkdir)
command_scp = f'sshpass -e scp -o StrictHostKeyChecking=no -P {PORT} {filename}.mp3 {USER}@{HOST}:{DIRNAME}/'
logger.info(command_scp)
os.system(command_scp)

# End
logger.info('END')