import redis
from flask import Flask , request
# from logger import logger
from pprint import pprint
import urllib.parse


r = redis.Redis(
		host='127.0.0.1',
		port=6379, 
		decode_responses = True, 
		charset = 'UTF-8',
		encoding = 'UTF-8'
	)

app = Flask(__name__)

@app.route('/set/<key>', methods=['POST'])
def set_key(key: str) ->str:
	data = request.get_data()

	# value = data
	# logger.info(f'get key/value => {key}/{value}')
	# print(data)
	# print(data.decode("utf-8"))
	# print(type(data.decode("utf-8")))
	# print(data.decode("utf-8").split("=")[1])
	value=data.decode("utf-8").split("=")[1]
	
	value = urllib.parse.unquote(value)
	print(key)
	print(value)

	# print(value)

	if not key or not value:
		return 'Error'

	if len(key)>300 or len(value) > 300:
		return 'too long'

	r.set(key,value)
	return 'OK'

@app.route('/get/<key>',methods=['GET'])
def get_key(key: str) ->str:
	response = r.get(key)
	return response if response else 'key not found!'

if __name__ == '__main__':
	app.debug=True
	app.run(host='127.0.0.1',port=80)














