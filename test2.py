import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import openpyxl


class GasAppExcel:
    def __init__(self, root):
        self.root = root
        self.root.title("Gas Station Calculator (Excel Import)")
        self.root.geometry("700x500")

        ttk.Label(root, text="Gas Station Calculator", font=("Arial", 18)).pack(pady=10)

        # Import Button
        ttk.Button(root, text="Import Excel File", command=self.import_excel).pack(pady=10)

        # Result Box
        self.results = tk.Text(root, height=20, width=80)
        self.results.pack(pady=10)

def import_excel(self):
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xlsm *.xltx *.xltm")]
    )

    if not file_path:
        return

    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        sheet = wb.active

        data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Skip empty rows
            if not row or row[0] is None:
                continue

            # Take only the first 4 columns safely
            station, pump, initial, final = row[:4]

            # Skip incomplete rows
            if station is None or pump is None or initial is None or final is None:
                continue

            data.append({
                "station": int(station),
                "pump": int(pump),
                "initial": float(initial),
                "final": float(final),
            })

        self.calculate_from_excel(data)

    except Exception as e:
        messagebox.showerror("Error", f"Could not read Excel file:\n{e}")


    def calculate_from_excel(self, data):
        self.results.delete("1.0", tk.END)

        station_totals = {}
        grand_total = 0

        for row in data:
            station = row["station"]
            pump = row["pump"]
            pumped = row["final"] - row["initial"]

            if station not in station_totals:
                station_totals[station] = 0

            station_totals[station] += pumped
            grand_total += pumped

            self.results.insert(
                tk.END,
                f"Station {station} - Pump {pump}: {pumped} liters\n"
            )

        self.results.insert(tk.END, "\n==============================\n")

        for station, total in station_totals.items():
            self.results.insert(tk.END, f"Total for Station {station}: {total} liters\n")

        self.results.insert(tk.END, "==============================\n")
        self.results.insert(tk.END, f"Grand Total: {grand_total} liters\n")
        self.results.insert(tk.END, "==============================\n")


root = tk.Tk()
app = GasAppExcel(root)
root.mainloop()
