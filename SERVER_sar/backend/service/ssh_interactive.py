# -*- coding: utf-8 -*-  
import os
import socket
import sys
import traceback

import paramiko

from reposity import models

try:
    import interactive
except ImportError:
    from . import interactive


def manual_auth(t, username, password):
    t.auth_password(username, password)


def ssh_session(bind_host_user, user_obj):
    # now connect
    hostname = bind_host_user.host.ip_addr
    port = bind_host_user.host.port
    username = bind_host_user.host_user.username
    password = bind_host_user.host_user.password
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception as e:
        print('*** Connect failed: ' + str(e))
        traceback.print_exc()
        sys.exit(1)

    try:
        t = paramiko.Transport(sock)
        try:
            t.start_client()
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            sys.exit(1)

        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print('*** Unable to open host keys file')
                keys = {}

        # check server's host key -- this is important.
        key = t.get_remote_server_key()
        if hostname not in keys:
            print('*** WARNING: Unknown host key!')
        elif key.get_name() not in keys[hostname]:
            print('*** WARNING: Unknown host key!')
        elif keys[hostname][key.get_name()] != key:
            print('*** WARNING: Host key has changed!!!')
            sys.exit(1)
        else:
            print('*** Host key OK.')

        if not t.is_authenticated():
            manual_auth(t, username, password)
        if not t.is_authenticated():
            print('*** Authentication failed. :(')
            t.close()
            sys.exit(1)

        chan = t.open_session()
        chan.get_pty()  # terminal
        chan.invoke_shell()
        print('*** Here we go!\n')

        session_obj = models.SessionLog.objects.create(account=user_obj.account,
                                                       host_user_bind=bind_host_user)
        interactive.interactive_shell(chan, session_obj)
        chan.close()
        t.close()

    except Exception as e:
        print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)
