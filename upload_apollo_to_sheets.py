import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# from datetime import datetime

# === CONFIG ===
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = "14aIycAY2Fe3dzhvJ-hMa3hne7WOTnJoI0i_VWirzFbE"
CSV_FILE = "apollo-contacts.csv"

# ===load Apollo export===
df = pd.read_csv(CSV_FILE)

# ===clean up data===
df = df[df["Email Status"] == "Verified"]

# Keep only the columns we need
df = df[["First Name", "Last Name", "Email", "Company", "Title"]]

# Add personalization fields
df["Full Name"] = df["First Name"] + " " + df["Last Name"]
df["Custom Message"] = "Loved your work at " + df["Company"]
df["Status"] = ""
df["Sent On"] = ""


# ==Connect to Google Sheets ===
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
client = gspread.authorize(creds)

# Open google sheet
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# === Upload to Sheet ===
# Clear existing content
sheet.clear()


# Upload header + rows
sheet.update([df.columns.tolist()] + df.values.tolist())

print(f"✅ Uploaded {len(df)} cleaned contacts to '{SPREADSHEET_ID}' successfully.")
