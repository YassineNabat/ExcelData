import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import openpyxl
import os # Useful for getting the directory of the script

class GasAppExcel:
    """
    A tkinter application to import gas pump meter readings from an Excel file,
    calculate the total liters sold per pump and station, and display the results.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Gas Station Calculator (Excel Import)")
        self.root.geometry("700x550")

        # --- Styling ---
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=10)
        style.configure('TLabel', background='#f0f0f0')
        self.root.configure(bg='#f0f0f0')
        
        # --- UI Elements ---
        ttk.Label(
            root, 
            text="Gas Station Sales Data Analyzer", 
            font=("Arial", 20, 'bold'),
            foreground='#0056b3'
        ).pack(pady=15)

        # Import Button
        ttk.Button(
            root, 
            text="Import Excel File", 
            command=self.import_excel
        ).pack(pady=10)

        # Result Box with Scrollbar
        frame = ttk.Frame(root)
        frame.pack(pady=10, padx=20)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results = tk.Text(
            frame, 
            height=20, 
            width=85, 
            wrap=tk.WORD, 
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),
            bg="#ffffff"
        )
        self.results.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.results.yview)

    # --- This function MUST be indented inside the class ---
    def import_excel(self):
        """Opens a file dialog, loads the selected Excel workbook, and extracts data."""
        # Use initialdir to start in the user's home or documents folder for convenience
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            initialdir=os.path.expanduser("~"), 
            filetypes=[("Excel Files", "*.xlsx *.xlsm *.xltx *.xltm")]
        )

        if not file_path:
            # User canceled the file selection
            return

        self.results.delete("1.0", tk.END)
        self.results.insert(tk.END, f"Attempting to read file: {file_path}\n\n")

        try:
            # data_only=True ensures we get the calculated value of a cell, not the formula.
            wb = openpyxl.load_workbook(file_path, data_only=True)
            sheet = wb.active # Use the active sheet (usually the first one)

            data = []
            
            # Assuming the first row is headers, start iteration from the second row
            for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                
                # Check for completely empty rows
                if not any(row):
                    continue

                # We expect the first 4 columns to be: Station, Pump, Initial Meter, Final Meter
                try:
                    station = row[0]
                    pump = row[1]
                    initial = row[2]
                    final = row[3]
                except IndexError:
                    messagebox.showwarning(
                        "Data Issue", 
                        f"Skipping row {row_index}: Data is incomplete (less than 4 columns)."
                    )
                    continue

                # Ensure critical fields have values and can be converted to numbers
                if station is None or pump is None or initial is None or final is None:
                    messagebox.showwarning(
                        "Data Issue", 
                        f"Skipping row {row_index}: Found empty cells in critical columns."
                    )
                    continue

                try:
                    # Clean the data types
                    data.append({
                        "station": str(station).strip(), # Keep station as string/ID
                        "pump": str(pump).strip(),       # Keep pump as string/ID
                        "initial": float(initial),
                        "final": float(final),
                    })
                except ValueError as ve:
                    messagebox.showwarning(
                        "Data Conversion Error", 
                        f"Skipping row {row_index}: Could not convert meter reading to number. Error: {ve}"
                    )
            
            # Only proceed if data was successfully loaded
            if data:
                self.calculate_from_excel(data)
            else:
                self.results.insert(tk.END, "No valid data rows were found in the file.")

        except Exception as e:
            # Catch all other possible errors (like file corruption or being opened elsewhere)
            messagebox.showerror("File Error", f"Could not process Excel file:\n{e}")

    # --- This function MUST be indented inside the class ---
    def calculate_from_excel(self, data):
        """Processes the clean data to calculate totals per station and pump."""
        
        self.results.insert(tk.END, "\n--- DETAILED PUMP READINGS ---\n")

        station_totals = {}
        grand_total = 0

        for row in data:
            station = row["station"]
            pump = row["pump"]
            initial = row["initial"]
            final = row["final"]
            
            # Simple calculation for pumped volume
            pumped = final - initial

            # Aggregate totals
            if station not in station_totals:
                station_totals[station] = 0

            station_totals[station] += pumped
            grand_total += pumped

            # Display individual reading results
            self.results.insert(
                tk.END,
                f"Station ID: {station.ljust(10)} | Pump {pump.ljust(3)} | Sold: {pumped:,.2f} liters\n"
            )

        self.results.insert(tk.END, "\n\n--- STATION SALES SUMMARY ---\n")

        # Display Summary
        for station, total in station_totals.items():
            self.results.insert(tk.END, f"Total for Station {station.ljust(10)}: {total:,.2f} liters\n")

        self.results.insert(tk.END, "\n==============================\n")
        self.results.insert(tk.END, f"GRAND TOTAL SALES: {grand_total:,.2f} liters\n")
        self.results.insert(tk.END, "==============================\n")


# --- Main Application Loop ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GasAppExcel(root)
    root.mainloop()