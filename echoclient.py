#!/usr/bin/python

import socket
import sys
import argparse
import threading


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


def recv_echo(s):
	while True:
		server_echo = (s.recv(1024)).decode('utf-8')
		sys.stdout.write(server_echo + "\n")
		sys.stdout.flush()

	return


def send_msg(s):
	while True:
		msg = raw_input()
		if len(msg) > 0:
			s.send(msg.encode('utf-8'))

	return


def main():
	global args
	parse_arguments()
	host = args.host
	port = int(args.port)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))

	get_hello(s)

	r = threading.Thread(target=recv_echo, args=(s,))
	r.setDaemon(True)
	r.start()

	send_msg(s)

	r.join()

	return


if __name__ == '__main__':
	main()

