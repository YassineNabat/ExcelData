import tkinter as tk
from tkinter import messagebox

# Scrollable frame with mouse wheel support
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, height=400, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
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
        if event.num == 4:  # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows / Mac
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Main gas calculator app
class GasCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gas Station Pump Calculator")
        self.root.geometry("950x550")
        self.root.config(bg="#e0e0e0")

        # Title
        tk.Label(root, text="Gas Station Pump Calculator", font=("Arial", 16, "bold"), bg="#e0e0e0").grid(row=0, column=0, columnspan=3, pady=10)

        # Number of stations input
        tk.Label(root, text="Number of Stations:", font=("Arial", 12), bg="#e0e0e0").grid(row=1, column=0, sticky="w", padx=10)
        self.num_stations_entry = tk.Entry(root, font=("Arial", 12), width=5)
        self.num_stations_entry.grid(row=1, column=1, sticky="w")
        tk.Button(root, text="Next", font=("Arial", 12), command=self.create_station_entries, bg="#4CAF50", fg="white").grid(row=1, column=2, padx=10)

        # Scrollable frame for pump inputs
        self.station_frame = ScrollableFrame(root)
        self.station_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=10, padx=10)

        self.calculate_button = None
        self.station_pump_entries = []

    # Input number of pumps per station
    def create_station_entries(self):
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

        tk.Label(self.station_frame.scrollable_frame, text="Enter number of pumps for each station:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=5)

        self.pump_entries = []
        for i in range(self.num_stations):
            tk.Label(self.station_frame.scrollable_frame, text=f"Station {i+1}:", font=("Arial", 12), bg="#f0f0f0").grid(row=i+1, column=0, sticky="w")
            entry = tk.Entry(self.station_frame.scrollable_frame, font=("Arial", 12), width=5)
            entry.grid(row=i+1, column=1, pady=2)
            self.pump_entries.append(entry)

        tk.Button(self.station_frame.scrollable_frame, text="Create Pump Table", font=("Arial", 12), command=self.create_pump_table, bg="#2196F3", fg="white").grid(row=self.num_stations+1, column=0, columnspan=2, pady=10)

    # Create pump input fields dynamically
    def create_pump_table(self):
        try:
            self.station_pumps = [int(e.get()) for e in self.pump_entries]
            if any(p < 1 for p in self.station_pumps):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter valid number of pumps for all stations")
            return

        for widget in self.station_frame.scrollable_frame.winfo_children():
            widget.destroy()
        self.station_pump_entries = []

        row_offset = 0
        for s_index, pumps in enumerate(self.station_pumps):
            # Station frame
            station_border = tk.Frame(self.station_frame.scrollable_frame, bd=2, relief="groove", padx=5, pady=5, bg="#ffffff")
            station_border.grid(row=row_offset, column=0, columnspan=4, pady=5, sticky="ew")
            row_offset += 1

            tk.Label(station_border, text=f"Station {s_index+1}", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=4, pady=2)

            # Column headers
            tk.Label(station_border, text="Pump #", font=("Arial", 11, "bold"), bg="#ffffff").grid(row=1, column=0, padx=5)
            tk.Label(station_border, text="Initial", font=("Arial", 11, "bold"), bg="#ffffff").grid(row=1, column=1, padx=5)
            tk.Label(station_border, text="Final", font=("Arial", 11, "bold"), bg="#ffffff").grid(row=1, column=2, padx=5)

            station_entries = []
            for p in range(pumps):
                bg_color = "#f9f9f9" if p % 2 == 0 else "#e6f2ff"
                tk.Label(station_border, text=f"{p+1}", bg=bg_color, width=8).grid(row=p+2, column=0)
                initial_entry = tk.Entry(station_border, width=10, bg=bg_color)
                initial_entry.grid(row=p+2, column=1, padx=5)
                final_entry = tk.Entry(station_border, width=10, bg=bg_color)
                final_entry.grid(row=p+2, column=2, padx=5)
                station_entries.append((initial_entry, final_entry))
            self.station_pump_entries.append(station_entries)

        if self.calculate_button:
            self.calculate_button.destroy()

        self.calculate_button = tk.Button(self.root, text="Calculate Totals", font=("Arial", 12), command=self.calculate_totals, bg="#FF5722", fg="white")
        self.calculate_button.grid(row=3, column=0, columnspan=3, pady=10)

    # Calculate totals
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
    app = GasCalculator(root)
    root.mainloop()
