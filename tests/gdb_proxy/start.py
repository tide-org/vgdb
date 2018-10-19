#!/usr/bin/env python

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 9999)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.connect(server_address)

try:
    message = b'$qSupported:multiprocess+;swbreak+;hwbreak+;qRelocInsn+;fork-events+;vfork-events+;exec-events+;vContSupported+;QThreadEvents+;no-resumed+;xmlRegisters=i386#6a'
    print >> sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
    data = sock.recv(4096)
    print >> sys.stderr, 'received "%s"' % data
    data = sock.recv(4096)
    print >> sys.stderr, 'received "%s"' % data
finally:
    print >> sys.stderr, 'closing socket'
    sock.close()
