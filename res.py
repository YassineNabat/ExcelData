import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook

# ... (Keep ScrollableFrame class the same)

class GasCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculatrice de Station-Service")
        self.root.geometry("1300x600")
        self.root.config(bg="#e0e0e0")

        tk.Label(root, text="Calculatrice des Pompes de Station-Service", font=("Arial", 16, "bold"), bg="#e0e0e0").grid(row=0, column=0, columnspan=5, pady=10)

        tk.Label(root, text="Nombre de stations:", font=("Arial", 12), bg="#e0e0e0").grid(row=1, column=0, sticky="w", padx=10)
        self.num_stations_entry = tk.Entry(root, font=("Arial", 12), width=5)
        self.num_stations_entry.grid(row=1, column=1, sticky="w")
        tk.Button(root, text="Suivant", font=("Arial", 12), command=self.create_station_entries, bg="#4CAF50", fg="white").grid(row=1, column=2, padx=10)

        self.station_frame = ScrollableFrame(root)
        self.station_frame.grid(row=2, column=0, columnspan=5, sticky="nsew", pady=10, padx=10)

        self.calculate_button = None
        self.excel_button = None
        self.station_entries = []

        for col in range(5):
            self.station_frame.scrollable_frame.grid_columnconfigure(col, weight=1)

    # ... (Keep create_station_entries() and create_pump_table() the same)

    def calculate_totals(self):
        self.results = []  # Save results to export to Excel
        grand_essence_liters = 0
        grand_gasoil_liters = 0
        grand_essence_revenue = 0
        grand_gasoil_revenue = 0

        result_text = ""
        try:
            for s_index, pumps in enumerate(self.station_entries):
                price_essence = float(self.price_entries[s_index][0].get())
                price_gasoil = float(self.price_entries[s_index][1].get())
                total_essence = 0
                total_gasoil = 0
                revenue_essence = 0
                revenue_gasoil = 0
                for initial_entry, final_entry, category in pumps:
                    initial = float(initial_entry.get())
                    final = float(final_entry.get())
                    liters = final - initial
                    if category == "Essence":
                        total_essence += liters
                        revenue_essence += liters * price_essence
                    else:
                        total_gasoil += liters
                        revenue_gasoil += liters * price_gasoil
                grand_essence_liters += total_essence
                grand_gasoil_liters += total_gasoil
                grand_essence_revenue += revenue_essence
                grand_gasoil_revenue += revenue_gasoil
                result_text += (f"Station {s_index+1}:\n"
                                f"  Essence: {total_essence} L, Chiffre d'affaires: {revenue_essence} DH\n"
                                f"  Gasoil: {total_gasoil} L, Chiffre d'affaires: {revenue_gasoil} DH\n\n")
                self.results.append([f"Station {s_index+1}", total_essence, revenue_essence, total_gasoil, revenue_gasoil])

            result_text += (f"Totaux Généraux:\n"
                            f"  Essence: {grand_essence_liters} L, Chiffre d'affaires: {grand_essence_revenue} DH\n"
                            f"  Gasoil: {grand_gasoil_liters} L, Chiffre d'affaires: {grand_gasoil_revenue} DH")
            self.results.append(["Totaux Généraux", grand_essence_liters, grand_essence_revenue, grand_gasoil_liters, grand_gasoil_revenue])
            messagebox.showinfo("Totaux", result_text)

            # Show button to save Excel
            if not self.excel_button:
                self.excel_button = tk.Button(self.root, text="Exporter vers Excel", font=("Arial", 12),
                                              command=self.export_to_excel, bg="#4CAF50", fg="white")
                self.excel_button.grid(row=4, column=0, columnspan=5, pady=10)

        except ValueError:
            messagebox.showerror("Erreur", "Remplissez tous les champs avec des nombres valides")

    def export_to_excel(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Stations"
        ws.append(["Station", "Essence (L)", "Chiffre d'affaires Essence (DH)", "Gasoil (L)", "Chiffre d'affaires Gasoil (DH)"])

        for row in self.results:
            ws.append(row)

        try:
            wb.save("Gas_Station_Report.xlsx")
            messagebox.showinfo("Succès", "Les résultats ont été exportés vers Gas_Station_Report.xlsx")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier Excel:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GasCalculator(root)
    root.mainloop()
