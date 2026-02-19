import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPE
)

client = gspread.authorize(creds)

PILOT_SHEET = "Pilot_Roster"
DRONE_SHEET = "Drone_Fleet"
MISSION_SHEET = "Missions"


def read_sheet(sheet_name):
    sheet = client.open(sheet_name).sheet1
    records = sheet.get_all_records()
    return pd.DataFrame(records)


def update_pilot_status(pilot_name, new_status):
    sheet = client.open(PILOT_SHEET).sheet1
    records = sheet.get_all_records()

    for i, row in enumerate(records):
        if row["name"] == pilot_name:
            # assuming status is column 5
            sheet.update_cell(i + 2, 5, new_status)
            return True

    return False
