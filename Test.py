import tkinter as tk
from tkinter import messagebox

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, height=400)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Bind mouse wheel ---
        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows / Mac
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)    # Linux scroll down

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.num == 4:  # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows / Mac
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class GasCalculatorFlexible:
    def __init__(self, root):
        self.root = root
        self.root.title("Gas Station Pump Calculator")
        self.root.geometry("900x500")

        # Step 1: Enter number of stations
        tk.Label(root, text="Number of Stations:").grid(row=0, column=0, sticky="w")
        self.num_stations_entry = tk.Entry(root)
        self.num_stations_entry.grid(row=0, column=1, sticky="w")
        tk.Button(root, text="Next", command=self.create_station_entries).grid(row=0, column=2, padx=10)

        # Scrollable frame for dynamic pump input fields
        self.station_frame = ScrollableFrame(root)
        self.station_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)

        self.calculate_button = None
        self.station_pump_entries = []

    # Step 2: Input number of pumps per station
    def create_station_entries(self):
        # Clear previous pump entries
        for widget in self.station_frame.scrollable_frame.winfo_children():
            widget.destroy()
        self.station_pump_entries = []

        try:
            self.num_stations = int(self.num_stations_entry.get())
            if self.num_stations < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number of stations")
            return

        tk.Label(self.station_frame.scrollable_frame, text="Enter number of pumps for each station:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        self.pump_entries = []
        for i in range(self.num_stations):
            tk.Label(self.station_frame.scrollable_frame, text=f"Station {i+1}:").grid(row=i+1, column=0, sticky="w")
            entry = tk.Entry(self.station_frame.scrollable_frame)
            entry.grid(row=i+1, column=1, pady=2)
            self.pump_entries.append(entry)

        tk.Button(self.station_frame.scrollable_frame, text="Create Pump Table", command=self.create_pump_table).grid(row=self.num_stations+1, column=0, columnspan=2, pady=10)

    # Step 3: Create pump input fields dynamically
    def create_pump_table(self):
        # Step 3a: Read pump counts BEFORE destroying widgets
        try:
            self.station_pumps = [int(e.get()) for e in self.pump_entries]
            if any(p < 1 for p in self.station_pumps):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter valid number of pumps for all stations")
            return

        # Step 3b: Clear previous widgets after reading
        for widget in self.station_frame.scrollable_frame.winfo_children():
            widget.destroy()
        self.station_pump_entries = []

        # Step 3c: Create Entry fields for each pump
        row_offset = 0
        for s_index, pumps in enumerate(self.station_pumps):
            tk.Label(self.station_frame.scrollable_frame, text=f"Station {s_index+1}", font=("Arial", 12, "bold")).grid(row=row_offset, column=0, pady=5, sticky="w")
            row_offset += 1
            station_entries = []
            for p in range(pumps):
                tk.Label(self.station_frame.scrollable_frame, text=f"Pump {p+1} Initial:").grid(row=row_offset, column=0, padx=5, pady=2)
                initial_entry = tk.Entry(self.station_frame.scrollable_frame, width=10)
                initial_entry.grid(row=row_offset, column=1, padx=5)
                tk.Label(self.station_frame.scrollable_frame, text="Final:").grid(row=row_offset, column=2, padx=5)
                final_entry = tk.Entry(self.station_frame.scrollable_frame, width=10)
                final_entry.grid(row=row_offset, column=3, padx=5)
                station_entries.append((initial_entry, final_entry))
                row_offset += 1
            self.station_pump_entries.append(station_entries)

        # Step 4: Add calculate button
        if self.calculate_button:
            self.calculate_button.destroy()

        self.calculate_button = tk.Button(self.root, text="Calculate Totals", command=self.calculate_totals)
        self.calculate_button.grid(row=2, column=0, columnspan=3, pady=10)

    # Step 5: Calculate totals
    def calculate_totals(self):
        grand_total = 0
        result_text = ""
        try:
            for s_index, station in enumerate(self.station_pump_entries):
                station_total = 0
                for initial_entry, final_entry in station:
                    initial = float(initial_entry.get())
                    final = float(final_entry.get())
                    station_total += final - initial
                grand_total += station_total
                result_text += f"Station {s_index+1} total: {station_total} liters\n"
            result_text += f"\nGrand Total: {grand_total} liters"
            messagebox.showinfo("Totals", result_text)
        except ValueError:
            messagebox.showerror("Error", "Please fill in all entries with valid numbers")

if __name__ == "__main__":
    root = tk.Tk()
    app = GasCalculatorFlexible(root)
    root.mainloop()
