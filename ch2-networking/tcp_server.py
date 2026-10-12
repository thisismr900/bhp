# socket module import kar rahe hain — ye Python ka built-in module hai
# jo network communication (TCP/UDP) ke liye use hota hai.
import socket

# ip = "0.0.0.0" ka matlab hai: "is laptop ke SAARE network interfaces par suno".
# Agar yahan "127.0.0.1" likhte to sirf isi laptop se connection aata (localhost).
# "0.0.0.0" likhne se WiFi (192.168.29.209) ke through dusra laptop bhi connect kar paayega.
ip = "0.0.0.0"

# port = wo "darwaza" jis par server sunega. 9998 ek free high-port hai.
# Client ko bhi isi port par connect karna hoga.
port = 9998

# Socket object banaya:
#   AF_INET    -> IPv4 address use karenge (jaise 192.168.29.209)
#   SOCK_STREAM -> TCP protocol use karenge (reliable, connection-based)
#
# socket.socket(family, type) -> do parameters hote hain:
#
#   1) FAMILY (address type - IPv4 ya IPv6):
#        socket.AF_INET   -> IPv4  (jaise 192.168.29.209)
#        socket.AF_INET6  -> IPv6  (jaise ::1 ya 2405:201:...)
#
#   2) TYPE (protocol - TCP ya UDP):
#        socket.SOCK_STREAM -> TCP (reliable, connection-based, ordered)
#        socket.SOCK_DGRAM  -> UDP (fast, connectionless, no guarantee)
#
# To char combinations bante hain:
#   IPv4 + TCP -> socket.socket(socket.AF_INET,  socket.SOCK_STREAM)   <-- yahan ye use kiya hai
#   IPv4 + UDP -> socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
#   IPv6 + TCP -> socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
#   IPv6 + UDP -> socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
#
# NOTE: UDP (SOCK_DGRAM) me kaam thoda alag hota hai -
#   - listen() aur accept() NAHI hote (kyunki connection hi nahi banta)
#   - bind() ke baad seedha recvfrom() / sendto() use karte hain
# IPv6 (AF_INET6) me address ek 4-tuple hota hai: (host, port, flowinfo, scopeid)
# jabki IPv4 me 2-tuple: (host, port)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_REUSEADDR = 1 set kiya.
# Isse hota ye hai: agar server band karke turant dobara chalayein,
# to "Address already in use" error nahi aata. Port turant reuse ho jaata hai.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind() = socket ko IP + port se jod dena.
# Ab ye socket 0.0.0.0:9998 par "reserve" ho gaya.
server.bind((ip, port))

# listen() = socket ko "listening mode" me daal dena, yaani connections accept karne ke liye ready.
# 5 = backlog, matlab ek saath max 5 pending (waiting) connections queue me reh sakte hain.
server.listen(5)

# Bas confirmation print kar rahe hain ki server chaalu ho gaya.
print(f"[*] Listening on {ip}:{port}")

# Infinite loop — server hamesha chalta rahe aur ek ke baad ek clients handle kare.
while True:
    # accept() yahan RUK jaata hai (blocking) jab tak koi client connect na kare.
    # Jaise hi client aata hai, ye 2 cheezein return karta hai:
    #   client  -> us client se baat karne ke liye naya socket
    #   address -> (client_ka_IP, client_ka_port) ka tuple
    client, address = server.accept()
    print(f"[*] Accepted connection from {address[0]}:{address[1]}")

    # recv(4096) = client ne jo bheja wo receive karo, max 4096 bytes.
    # Data hamesha BYTES me aata hai (b"...").
    request = client.recv(4096)

    # .decode() = bytes ko normal string me convert karna (taaki print kar sakein).
    # errors='replace' = agar koi byte decode na ho paaye to crash na ho, replace kar de.
    print(f"[*] Received: {request.decode(errors='replace')}")

    # client ko jawab bhejo. b"ACK" = bytes me "ACK" (acknowledgement).
    # TCP me data hamesha bytes me hi bhejte hain, isliye b"" lagaya.
    client.send(b"ACK")

    # Is client ka kaam khatam — uska socket band kar do.
    # (Server ka main socket chalta rahega, loop dobara accept() par wait karega.)
    client.close()
