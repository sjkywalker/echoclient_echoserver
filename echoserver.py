#!/usr/bin/python

import socket
import sys
import argparse
import thread

def parse_arguments():
	global args

	parser = argparse.ArgumentParser(description='Activate echoserver')
	
	parser.add_argument('port', help='port number to open on server')
	parser.add_argument('-b', '--broadcast', help='broadcast echo to all clients', action='store_true')

	args = parser.parse_args()


def create_socket(port):
	try:
		global host
		global s

		host = 'localhost'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		print "[+] Created socket"
	
	except socket.error as msg:
		print "[-] Socket creation error: " + str(msg)


def bind_socket(port):
	try:
		global host
		global s

		print "[+] Binding socket to port: " + str(port)
		
		s.bind((host, port))
		s.listen(5)

	except socket.error as msg:
		print "[-] Socket binding error: " + str(msg)


def send_hello(conn):
	hello = "\n\nWelcome to my server\n\n"
	conn.send(hello.encode('utf-8'))
	return


def echo_msg(conn):
	while True:
		client_response = (conn.recv(1024)).decode('utf-8')
		sys.stdout.write(client_response)
		sys.stdout.flush()

		conn.send(client_response.encode('utf-8'))

	return


def accept_connection(port):
	try:
		global host
		global s

		conn, address = s.accept()

		print "[+] Connection established | " + "IP " + str(address[0]) + " Port " + str(address[1] + "\n")

		send_hello(conn)
		echo_msg(conn)

		conn.close()

	except socket.error as msg:
		print "[-] Connection error: " + str(msg)

	return



def main():
	global args
	parse_arguments()
	port = int(args.port)

	print "[+] Open port " + args.port
	print "[+] Broadcast option: " + str(args.broadcast) + "\n"

	create_socket(port)
	bind_socket(port)
	accept_connection(port)
	
	return


if __name__ == '__main__':
	main()

