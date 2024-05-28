import socket

def play_game(player1, player2):
    player1_score = 0
    player2_score = 0
    total_rounds = 5

    for round_num in range(1, total_rounds + 1):
        # Kirim permintaan untuk pilihan dari setiap pemain
        player1.sendall("Round {}: Pilih (gunting/batu/kertas): ".format(round_num).encode())
        choice1 = player1.recv(1024).decode().strip()

        player2.sendall("Round {}: Pilih (gunting/batu/kertas): ".format(round_num).encode())
        choice2 = player2.recv(1024).decode().strip()

        # Tentukan pemenang dari ronde tersebut
        winner = determine_winner(choice1, choice2)

        # Tampilkan hasil ronde
        player1.sendall("Hasil Round {}: Anda memilih {}, Player 2 memilih {}, {}".format(round_num, choice1, choice2, winner).encode())
        player2.sendall("Hasil Round {}: Anda memilih {}, Player 1 memilih {}, {}".format(round_num, choice2, choice1, winner).encode())

        # Perbarui skor
        if winner == "Player 1":
            player1_score += 1
        elif winner == "Player 2":
            player2_score += 1

        # Cek apakah sudah ada pemenang
        if player1_score >= 3 or player2_score >= 3:
            break

    # Tentukan pemenang permainan
    if player1_score > player2_score:
        winner = "Player 1"
    elif player2_score > player1_score:
        winner = "Player 2"
    else:
        winner = "Tidak ada pemenang, hasil seri"

    # Kirim skor akhir
    player1.sendall("Permainan selesai. Pemenang: {}. Skor: Player 1 = {}, Player 2 = {}".format(winner, player1_score, player2_score).encode())
    player2.sendall("Permainan selesai. Pemenang: {}. Skor: Player 1 = {}, Player 2 = {}".format(winner, player1_score, player2_score).encode())

def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "Seri"
    elif (choice1 == "gunting" and choice2 == "kertas") or \
         (choice1 == "kertas" and choice2 == "batu") or \
         (choice1 == "batu" and choice2 == "gunting"):
        return "Player 1"
    else:
        return "Player 2"

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8888))
    server_socket.listen(2)
    print("Menunggu koneksi player...")

    player1, addr1 = server_socket.accept()
    print("Player 1 terhubung dari", addr1)
    player1.sendall("Anda Player 1. Menunggu Player 2 untuk bergabung...".encode())

    player2, addr2 = server_socket.accept()
    print("Player 2 terhubung dari", addr2)
    player1.sendall("Anda Player 2. Permainan dimulai!".encode())
    player2.sendall("Anda Player 2. Permainan dimulai!".encode())

    play_game(player1, player2)

    player1.close()
    player2.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
