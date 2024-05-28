import socket

def play_game(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

        if "Pilih" in message:
            choice = input("Masukkan pilihan (gunting/batu/kertas): ")
            client_socket.sendall(choice.encode())
        elif "Permainan selesai" in message:
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8888))

    welcome_message = client_socket.recv(1024).decode()
    print(welcome_message)

    play_game(client_socket)

    client_socket.close()

if __name__ == "__main__":
    start_client()
