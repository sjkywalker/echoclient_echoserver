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

		print "[+] Binding socket to port: " + str(port) + "\n"
		
		s.bind((host, port))

		s.listen(5)

	except socket.error as msg:
		print "[-] Socket binding error: " + str(msg)

	return


def client_thread(conn, address):
	global connList

	hello  = "\n" + "**************************\n"
	hello +=        "*  Welcome to my server  *" + "\n"
	hello +=        "**************************" + "\n"
	hello += "\n" + "Your message will echo back" + "\n\n"
	conn.send(hello.encode('utf-8'))

	while True:
		client_response = (conn.recv(1024)).decode('utf-8')

		if not client_response:
			break

		sys.stdout.write("[+] From ({0}:{1}): ".format(str(address[0]), str(address[1])) + client_response + "\n")
		sys.stdout.flush()

		if args.broadcast:
			for conn_ in connList:
				conn_.send(client_response.encode('utf-8'))
		else:
			conn.send(client_response.encode('utf-8'))

	connList.remove(conn)
	conn.close()

	print "[*] Connection closed: ({0}:{1})".format(str(address[0]), str(address[1]))
	print "[*] {0} Live session(s)".format(len(connList)) + "\n"

	return


def main():
	global s
	global args
	global host
	global connList

	parse_arguments()
	port = int(args.port)

	print "[+] Open port " + args.port
	print "[+] Broadcast option: " + str(args.broadcast) + "\n"

	create_socket(port)
	bind_socket(port)

	connList = []
	sessionList = []

	while True:
		try:
			conn, address = s.accept()
			connList.append(conn)
			print "[+] Connection established: ({0}:{1})".format(str(address[0]), str(address[1]))
			print "[*] {0} Live session(s)".format(len(connList)) + "\n"
			session = threading.Thread(target=client_thread, args=(conn, address))
			session.setDaemon(True)
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

