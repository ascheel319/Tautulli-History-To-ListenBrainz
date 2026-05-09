import csv
import requests
import time

# Fill these in
TOKEN = "LISTENBRAINZ_TOKEN"
CSV_FILE = "TAUTULLI_LISTEN_HISTORY.CSV"

def main():
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f)) # Load as list to track progress
        total = len(reader)
        count = 0

        print(f"Starting upload of {total} listens...")

        for row in reader:
            payload = {
                "listen_type": "single",
                "payload": [{
                    "listened_at": int(row['listened_at']),
                    "track_metadata": {
                        "artist_name": row['artist_name'],
                        "track_name": row['track_name'],
                        "release_name": row['album_name']
                    }
                }]
            }
            headers = {'Authorization': f'Token {TOKEN}'}

            uploaded = False
            while not uploaded:
                try:
                    r = requests.post("https://api.listenbrainz.org/1/submit-listens", json=payload, headers=headers)

                    if r.status_code == 200:
                        count += 1
                        print(f"[{count}/{total}] Uploaded: {row['track_name']}")
                        uploaded = True
                        time.sleep(0.5) # Increased delay to prevent 429s

                    elif r.status_code == 429:
                        print("Rate limit hit! Sleeping for 30 seconds...")
                        time.sleep(30) # Take a long break if the server is stressed

                    else:
                        print(f"Error {r.status_code}: {r.text}")
                        uploaded = True # Skip this one if it's a different error (like bad data)

                except Exception as e:
                    print(f"Connection error: {e}. Retrying in 5 seconds...")
                    time.sleep(5)

if __name__ == "__main__":
    main()
