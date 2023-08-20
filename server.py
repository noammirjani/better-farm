import socket
import struct
from PIL import Image
import io

HOST, PORT = "0.0.0.0", 8000

def receive_image():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("Server is running and listening for incoming connections...")

    while True:
        conn, addr = s.accept()
        with conn:
            image_len = struct.unpack('<L', conn.recv(struct.calcsize('<L')))[0]
            image_stream = io.BytesIO()
            image_stream.write(conn.recv(image_len))
            image_stream.seek(0)
            img = Image.open(image_stream)
            img.show()  # You can save or process the image as needed

        conn.close()

if __name__ == "__main__":
    receive_image()
