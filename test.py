#!/usr/bin/env python3
from flask import Flask, request


app = Flask('phishkiller test-server')

@app.route('/', methods=['POST'])
def test_url():
	data = request.json
	print(f'Payload:', data)
	return 'OK', 200

app.run('0.0.0.0', 8080)