import tkinter as tk
from tkinter import messagebox

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, height=450, width=1200, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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
        self.station_entries = []

        # Make scrollable frame columns expandable
        for col in range(5):
            self.station_frame.scrollable_frame.grid_columnconfigure(col, weight=1)

    def create_station_entries(self):
        for widget in self.station_frame.scrollable_frame.winfo_children():
            widget.destroy()
        self.station_entries = []

        try:
            self.num_stations = int(self.num_stations_entry.get())
            if self.num_stations < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Entrez un nombre valide de stations")
            return

        tk.Label(self.station_frame.scrollable_frame, text="Entrez le nombre de pompes pour chaque catégorie par station:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=5, pady=5)

        self.pump_inputs = []
        for i in range(self.num_stations):
            tk.Label(self.station_frame.scrollable_frame, text=f"Station {i+1}", font=("Arial", 12), bg="#f0f0f0").grid(row=i+1, column=0, sticky="w", padx=5)
            tk.Label(self.station_frame.scrollable_frame, text="Pompes Essence:", bg="#f0f0f0").grid(row=i+1, column=1, sticky="w", padx=5)
            essence_entry = tk.Entry(self.station_frame.scrollable_frame, width=10)
            essence_entry.grid(row=i+1, column=2, sticky="w", padx=5)
            tk.Label(self.station_frame.scrollable_frame, text="Pompes Gasoil:", bg="#f0f0f0").grid(row=i+1, column=3, sticky="w", padx=5)
            gasoil_entry = tk.Entry(self.station_frame.scrollable_frame, width=10)
            gasoil_entry.grid(row=i+1, column=4, sticky="w", padx=5)
            self.pump_inputs.append((essence_entry, gasoil_entry))

        tk.Button(self.station_frame.scrollable_frame, text="Créer le tableau des pompes", font=("Arial", 12), command=self.create_pump_table, bg="#2196F3", fg="white").grid(row=self.num_stations+1, column=0, columnspan=5, pady=10)

    def create_pump_table(self):
        self.station_pumps = []
        try:
            for e_entry, g_entry in self.pump_inputs:
                essence_pumps = int(e_entry.get())
                gasoil_pumps = int(g_entry.get())
                if essence_pumps < 0 or gasoil_pumps < 0:
                    raise ValueError
                self.station_pumps.append((essence_pumps, gasoil_pumps))
        except ValueError:
            messagebox.showerror("Erreur", "Entrez des nombres valides pour les pompes")
            return

        for widget in self.station_frame.scrollable_frame.winfo_children():
            widget.destroy()

        self.station_entries = []
        self.price_entries = []

        for s_index, (essence_pumps, gasoil_pumps) in enumerate(self.station_pumps):
            frame = tk.Frame(self.station_frame.scrollable_frame, bd=2, relief="groove", padx=5, pady=5, bg="#fff")
            frame.grid(row=s_index, column=0, pady=5, sticky="ew")

            # Make columns expandable
            for col in range(4):
                frame.grid_columnconfigure(col, weight=1)

            tk.Label(frame, text=f"Station {s_index+1}", font=("Arial", 12, "bold"), bg="#fff").grid(row=0, column=0, columnspan=4, pady=2)
            tk.Label(frame, text="Prix par litre Essence:", bg="#fff").grid(row=1, column=0, sticky="w", padx=5)
            price_essence = tk.Entry(frame, width=12)
            price_essence.grid(row=1, column=1, sticky="w", padx=5)
            tk.Label(frame, text="Prix par litre Gasoil:", bg="#fff").grid(row=1, column=2, sticky="w", padx=5)
            price_gasoil = tk.Entry(frame, width=12)
            price_gasoil.grid(row=1, column=3, sticky="w", padx=5)
            self.price_entries.append((price_essence, price_gasoil))

            pumps_entries = []

            # Column headers
            tk.Label(frame, text="N° Pompe", bg="#fff", font=("Arial", 10, "bold")).grid(row=2, column=0)
            tk.Label(frame, text="Initial", bg="#fff", font=("Arial", 10, "bold")).grid(row=2, column=1)
            tk.Label(frame, text="Final", bg="#fff", font=("Arial", 10, "bold")).grid(row=2, column=2)
            tk.Label(frame, text="Catégorie", bg="#fff", font=("Arial", 10, "bold")).grid(row=2, column=3)

            r = 3
            for p in range(essence_pumps):
                tk.Label(frame, text=f"{p+1}", bg="#f9f9f9").grid(row=r, column=0)
                initial = tk.Entry(frame, width=12, bg="#f9f9f9")
                initial.grid(row=r, column=1)
                final = tk.Entry(frame, width=12, bg="#f9f9f9")
                final.grid(row=r, column=2)
                tk.Label(frame, text="Essence", bg="#f9f9f9").grid(row=r, column=3)
                pumps_entries.append((initial, final, "Essence"))
                r += 1
            for p in range(gasoil_pumps):
                tk.Label(frame, text=f"{p+1}", bg="#e6f2ff").grid(row=r, column=0)
                initial = tk.Entry(frame, width=12, bg="#e6f2ff")
                initial.grid(row=r, column=1)
                final = tk.Entry(frame, width=12, bg="#e6f2ff")
                final.grid(row=r, column=2)
                tk.Label(frame, text="Gasoil", bg="#e6f2ff").grid(row=r, column=3)
                pumps_entries.append((initial, final, "Gasoil"))
                r += 1
            self.station_entries.append(pumps_entries)

        if self.calculate_button:
            self.calculate_button.destroy()
        self.calculate_button = tk.Button(self.root, text="Calculer Totaux", font=("Arial", 12),
                                          command=self.calculate_totals, bg="#FF5722", fg="white")
        self.calculate_button.grid(row=3, column=0, columnspan=5, pady=10)

    def calculate_totals(self):
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
            result_text += (f"Totaux Généraux:\n"
                            f"  Essence: {grand_essence_liters} L, Chiffre d'affaires: {grand_essence_revenue} DH\n"
                            f"  Gasoil: {grand_gasoil_liters} L, Chiffre d'affaires: {grand_gasoil_revenue} DH")
            messagebox.showinfo("Totaux", result_text)
        except ValueError:
            messagebox.showerror("Erreur", "Remplissez tous les champs avec des nombres valides")

if __name__ == "__main__":
    root = tk.Tk()
    app = GasCalculator(root)
    root.mainloop()
