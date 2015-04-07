from contextlib import contextmanager
import socket


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ret = s.getsockname()[0]

    s.close()
    return ret


def msg(act, **d):
    ret = {'act': act}
    ret.update(d)

    return ret


class UnexpectedMessage(Exception):
    pass


def recv_msg(socket, act, **d):
    msg = socket.recv_json()
    assert 'act' in msg

    if msg['act'] != act:
        raise UnexpectedMessage('Required %s, received %s.' % (act, msg['act']))

    return [v(msg[k]) for k, v in d.items()]


def unpack_ret(m):
    if m['act'] == 'ret':
        return m['status'], m['payload']
    else:
        return m


import zmq
def ack_gen(ctx):
    def ack(addr, socket_type=zmq.PAIR, **additional_info):
        socket = ctx.socket(socket_type)
        socket.connect(addr)
        socket.send_json(msg(act='ack', **additional_info))
        socket.close()

    return ack


def wait_for_ack_gen(ctx, local_ip=None):
    def wait_for_ack(ip=local_ip, port=None,
                     socket_type=zmq.PAIR,
                     **additional_info):
        socket = ctx.socket(socket_type)
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)

        if not ip:
            ip = get_local_ip()

        if not port:
            port = socket.bind_to_random_port('tcp://%s' % ip)
        else:
            socket.bind('tcp://%s:%s' % (ip, port))

        def _(timeout=3 * 1000):
            if poller.poll(timeout):
                m = socket.recv_json()
                socket.close()

                assert 'act' in m
                assert 'ack' == m['act']

                for k, v in additional_info.items():
                    if k not in m:
                        return False
                    if v != m[k]:
                        return False

                return True

        return port, _

    return wait_for_ack

import logging

import lzma
import zipfile
import base64
import io
import os
def flat_b64archive(dir_path, excluded, compress=True):
    zip_dummy = io.BytesIO()

    with zipfile.ZipFile(zip_dummy, 'w') as zf:
        for name in os.listdir(dir_path):
            if name in excluded:
                continue

            zf.write(os.path.join(dir_path, name), name)

    if compress:
        xz = lzma.compress(zip_dummy.getvalue())
    else:
        xz = zip_dummy.getvalue()

    conf_b64 = base64.b64encode(xz)

    return str(conf_b64, encoding='ascii')


def flat_b64extract(s, dir_path, decompress=True):
    conf_zip_xz = base64.b64decode(bytes(s, encoding='ascii'))

    if decompress:
        conf_zip = lzma.decompress(conf_zip_xz)
    else:
        conf_zip = conf_zip_xz

    with zipfile.ZipFile(io.BytesIO(conf_zip)) as zf:
        zf.extractall(dir_path)


def temp_socket_gen(ctx, local_ip):
    def temp_socket(push_addr, msg,
                    push_type=zmq.PUSH,
                    temp_socket_type=zmq.PAIR):
        push_socket = ctx.socket(push_type)
        push_socket.connect(push_addr)

        sck = ctx.socket(temp_socket_type)
        port = sck.bind_to_random_port('tcp://%s' % local_ip)

        new_msg = {'addr': 'tcp://%s:%s' % (local_ip, port)}
        new_msg.update(msg)

        push_socket.send_json(new_msg)
        push_socket.close()

        ret = sck.recv_json()
        sck.close()

        return ret

    return temp_socket


def logger():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s:%(asctime)s:%(filename)s: '
                               '%(message)s')
    return logging.getLogger(__name__)

