import redis
from urllib import parse
from logger import logger
from pprint import pprint
from flask import Flask, request

r = redis.Redis(
        host='127.0.0.1',
        port=6379,
        password='ur87',
        decode_responses=True,
        charset='UTF-8',
        encoding='UTF-8')
app = Flask(__name__)

@app.route('/set/<key>', methods=['POST'])
def set_key(key: str) -> str:
    data = request.form
    value = parse.unquote(data['value'])

    logger.info(f'receive key/value => {key}/{value}')

    if not key:
        logger.error('Key not exist')
        return 'Error'

    if len(key) > 256 or len(value) > 256:
        logger.error('Key or value too long')
        return 'Error'

    r.set(key, value)
    logger.info(f'Success set key/value => {key}/{value}')
    return 'OK'

@app.route('/get/<key>', methods=['GET'])
def get_key(key: str) -> str:
    response = r.get(key)
    logger.info(f'get key/response => {key}/{response}')
    return 'key not found!' if response is None else response

if __name__ == '__main__':
    logger.info('Server running...')
    app.run(host='127.0.0.1', port=80)