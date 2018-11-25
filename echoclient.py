#!/usr/bin/python

import socket
import sys
import argparse
import thread


def parse_arguments():
	global args

	parser = argparse.ArgumentParser(description='Activate echoclient')
	parser.add_argument('host', help='host server to connect')	
	parser.add_argument('port', help='port number to connect')
	args = parser.parse_args()

	return


def get_hello(s):
	server_hello = (s.recv(1024)).decode('utf-8')
	sys.stdout.write(server_hello)
	sys.stdout.flush()

	return


def send_msg(s):
	while True:
		msg = raw_input()
		if len(str.encode(msg)) > 0:
			s.send(str.encode(msg))
			server_echo = (s.recv(1024)).decode('utf-8')
			sys.stdout.write(server_echo)
			sys.stdout.flush()

	return


def main():
	global args
	parse_arguments()
	host = args.host
	port = int(args.port)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))

	get_hello(s)
	send_msg(s)

	return


if __name__ == '__main__':
	main()

