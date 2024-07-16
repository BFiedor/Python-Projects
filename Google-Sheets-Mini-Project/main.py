import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "18Sh9MxVBn1_yayQAtWKD1dOYLzJgwroOsM__XwfTYiE" #ID after /d/ and before /edit in a Google Sheets address
workbook = client.open_by_key(sheet_id)

#Printing out Sheet Titles for Google Sheets
#sheets = map(lambda x: x.title, workbook.worksheets())
#print(list(sheets))

#Updating a Sheet Title in GoogleSheets
#sheet = workbook.worksheet("Sheet1")
#sheet.update_title("Hello World")

#Updating Cell Values, (row, column, updated value)
#sheet = workbook.worksheet("Hello World")
#sheet.update_cell(1, 1, "Hello world this is changed")

#Acquiring the value of a cell
#sheet = workbook.worksheet("Hello World")
#value = sheet.acell("A1").value
#print(value)

#Finding a Value if cell row and col are unknown
#sheet = workbook.worksheet("Hello World")
#cell = sheet.find("Find Me")
#print(cell.row, cell.col)

#Perform Formatting on a cell or group of cells
#sheet = workbook.worksheet("Hello World")
#sheet.format("A1", {"textFormat": {"bold": True}})

values = [
    ["Name", "Price", "Quantity"],
    ["Basketball", 29.99, 1],
    ["Jeans", 39.99, 4],
    ["Soap", 7.99, 3]
]

worksheet_list = map(lambda x: x.title, workbook.worksheets())
new_worksheet_name = "Values"

if new_worksheet_name in worksheet_list:
    sheet = workbook.worksheet(new_worksheet_name)
else:
    sheet = workbook.add_worksheet(new_worksheet_name, rows=10, cols=10)
    
sheet.clear()

sheet.update(f"A1:C{len(values)}", values)

sheet.update_cell(len(values)+1, 2, "=sum(B2:B4)")
sheet.update_cell(len(values)+1, 3, "=sum(C2:C4)")

sheet.format("A1:C1", {"textFormat": {"bold": True}})

