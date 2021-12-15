from ctypes import *

# load the library
lib = cdll.LoadLibrary('/usr/lib/x86_64-linux-gnu/liblxi.so')
  
# define functions
def init():
    lib.lxi_init()

def connect(address, port: int, name, timeout: int, protocol: int):
    lib.lxi_connect.argtypes = POINTER(c_byte), c_int, POINTER(c_byte), c_int, c_int
    lib.lxi_connect.restype = c_int
    address_bytes = str.encode(address)
    name_bytes = str.encode(name)
    device = lib.lxi_connect(cast(c_char_p(address_bytes), POINTER(c_byte)), c_int(port), cast(c_char_p(name_bytes), POINTER(c_byte)), c_int(timeout), c_int(protocol))
    return device

def send(device: int, message, length: int, timeout: int):
    lib.lxi_send.argtypes = c_int, POINTER(c_byte), c_int, c_int
    lib.lxi_send.restype = c_int
    message_bytes = str.encode(message)
    status = lib.lxi_send(c_int(device), cast(c_char_p(message_bytes), POINTER(c_byte)), c_int(length), c_int(timeout))
    return status

def receive(device: int, length: int, timeout: int):
    lib.lxi_receive.argtypes = c_int, c_char_p, c_int, c_int
    lib.lxi_receive.restype = c_int
    message_p = c_char_p(bytes("", "utf-8") * length)
    status = lib.lxi_receive(c_int(device), message_p, c_int(length), c_int(timeout))
    message = str(message_p.value)
    return status, message

def disconnect(device: int):
    lib.lxi_disconnect.argtypes = (c_int,)
    lib.lxi_disconnect.restype = c_int
    status = lib.lxi_disconnect(device)
    return status
