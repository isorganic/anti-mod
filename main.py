import requests
import random
import time
import os
from colorama import Fore

channel_id = input("Masukkan ID channel: ")
waktu1 = int(input("Set Waktu Hapus Pesan: "))
waktu2 = int(input("Set Waktu Kirim Pesan: "))

# Membaca username moderator
with open("moderator.txt", "r") as f:
    moderator_username = f.readline().strip()

time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)

os.system('cls' if os.name == 'nt' else 'clear')

with open("pesan.txt", "r") as f:
    words = f.readlines()

with open("token.txt", "r") as f:
    authorization = f.readline().strip()

while True:
    channel_id = channel_id.strip()

    payload = {
        'content': random.choice(words).strip()
    }

    headers = {
        'Authorization': authorization
    }

    r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=headers)
    print(Fore.WHITE + "Pesan terkirim: ")
    print(Fore.YELLOW + payload['content'])

    response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)

    if response.status_code == 200:
        messages = response.json()
        if len(messages) == 0:
            is_running = False
            break
        else:
            time.sleep(waktu1)

            message_id = messages[0]['id']
            message_author = messages[0]['author']['username']

            # Memeriksa apakah pesan adalah balasan dari moderator
            if 'message_reference' in messages[0] and messages[0]['message_reference']:
                replied_message = messages[0]['message_reference']
                if replied_message.get('user', {}).get('username') == moderator_username:
                    # Mengirim balasan ke pesan moderator
                    reply_payload = {
                        'content': "hehe siap sir",
                        'message_reference': {'message_id': message_id}
                    }
                    reply_response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=reply_payload, headers=headers)
                    if reply_response.status_code == 200:
                        print(Fore.GREEN + f"Balasan ke pesan moderator dengan 'hehe siap sir'.")
                    else:
                        print(Fore.RED + f"Gagal membalas pesan moderator: {reply_response.status_code}")

            # Menghapus pesan yang bukan balasan dari moderator
            else:
                response = requests.delete(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}', headers=headers)
                if response.status_code == 204:
                    print(Fore.GREEN + f'Pesan dengan ID {message_id} berhasil dihapus')
                else:
                    print(Fore.RED + f'Gagal menghapus pesan dengan ID {message_id}: {response.status_code}')
    else:
        print(f'Gagal mendapatkan pesan di channel: {response.status_code}')

    time.sleep(waktu2)
