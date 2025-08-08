import requests
import os

# --- Config ---
BASEROW_API_TOKEN = os.getenv("BASEROW_API_TOKEN")
BASEROW_TABLE_ID = "12345"  # ID de ta table
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")  # URL du webhook n8n

# --- Headers Baserow ---
baserow_headers = {
    "Authorization": f"Token {BASEROW_API_TOKEN}"
}

# --- Étape 1 : Récupérer toutes les rows ---
def get_rows():
    url = f"https://api.baserow.io/api/database/rows/table/{BASEROW_TABLE_ID}/?user_field_names=true"
    rows = []
    while url:
        r = requests.get(url, headers=baserow_headers)
        r.raise_for_status()
        data = r.json()
        rows.extend(data["results"])
        url = data.get("next")
    return rows

# --- Étape 2 : Filtrer par status ---
def filter_check_email(rows):
    return [{"id": row["id"], "email": row["Email"]} for row in rows if row.get("Status") == "check email"]

# --- Étape 3 : Envoyer vers le webhook n8n ---
def send_to_n8n(data):
    r = requests.post(N8N_WEBHOOK_URL, json={"records": data})
    r.raise_for_status()
    print(f"✅ Données envoyées à n8n ({len(data)} enregistrements)")

# --- Main ---
if __name__ == "__main__":
    all_rows = get_rows()
    to_check = filter_check_email(all_rows)

    if to_check:
        send_to_n8n(to_check)
    else:
        print("⚠️ Aucun enregistrement avec status 'check email'")