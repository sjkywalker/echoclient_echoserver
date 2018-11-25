#!/usr/bin/python

import socket
import sys
import argparse
import threading


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

	return


def client_thread(conn):
	hello = "\n\nWelcome to my server\n\n"
	conn.send(hello.encode('utf-8'))
	while True:
		client_response = (conn.recv(1024)).decode('utf-8')
		if not client_response:
			break
		sys.stdout.write(client_response)
		sys.stdout.flush()
		conn.send(client_response.encode('utf-8'))

	conn.close()
	return


def main():
	global s
	global args
	global host
	
	parse_arguments()
	port = int(args.port)

	print "[+] Open port " + args.port
	print "[+] Broadcast option: " + str(args.broadcast) + "\n"

	create_socket(port)
	bind_socket(port)

	sessionList = []

	while True:
		try:
			conn, address = s.accept()
			print "[+] Connection established | " + "IP " + str(address[0]) + " Port " + str(address[1]) + "\n"
			session = threading.Thread(target=client_thread, args=(conn,))
			sessionList.append(session)
			session.start()

		except socket.error as msg:
			print "[-] Connection error: " + str(msg)	

	for session in sessionList:
		session.join()

	s.close()

	return


if __name__ == '__main__':
	main()

