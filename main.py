import requests
import time


TOKEN = "token yaz"

headers = {
    "Authorization": TOKEN,
    "User-Agent": "Mozilla/5.0"
}

def get_user_id():
    user_info = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if user_info.status_code == 200:
        return user_info.json()["id"]
    else:
        raise Exception("token yanlis")

def delete_dm(channel_id, max_deletions=1000):
    user_id = get_user_id()
    deleted_count = 0

    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    params = {"limit": 100} # Elleme

    while deleted_count < max_deletions:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Hata: {response.status_code}")
            break

        messages = response.json()
        if not messages:
            print("Tüm mesajlar silindi.")
            break

        deleted_this_batch = 0
        for msg in messages:
            if msg["author"]["id"] != user_id:
                continue  # baska hesabin mesaji

            del_url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{msg['id']}"
            del_resp = requests.delete(del_url, headers=headers)

            if del_resp.status_code == 204:
                deleted_count += 1
                deleted_this_batch += 1
                print(f"{deleted_count}. Silindi: {msg['id']}")
            else:
                print(f"Silinemedi ({del_resp.status_code}): {msg['id']}")

            time.sleep(1)  # elleme

            if deleted_count >= max_deletions:
                print("mesajlarin bitti veya rate limit")
                return

        if deleted_this_batch == 0:
            print("mesajlarin bitti.")
            break

channel_id = ""
delete_dm(channel_id, max_deletions=1000)