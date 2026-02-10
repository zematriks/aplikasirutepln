import tkinter as tk

# Simple GUI to collect multiple longitude/latitude pairs,
# format them as a Python list of lists and allow copying to clipboard.

def main():
    coords = []

    def format_coords():
        lines = []
        for lon, lat in coords:
            # keep 8 decimal places like screenshot
            lines.append(f"  [{lon:.8f}, {lat:.8f}],")
        if lines:
            body = "\n".join(lines)
            return f"coords = [\n{body}\n]"
        else:
            return "coords = [\n]"

    def update_display():
        text = format_coords()
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, text)
        output_text.config(state="disabled")
        count_label.config(text=f"Count: {len(coords)}")

    def add_coordinate():
        lon_s = longitude_entry.get().strip()
        lat_s = latitude_entry.get().strip()
        try:
            lon = float(lon_s)
            lat = float(lat_s)
        except ValueError:
            status_label.config(text="Invalid number", fg="red")
            return
        coords.append((lon, lat))
        longitude_entry.delete(0, tk.END)
        latitude_entry.delete(0, tk.END)
        status_label.config(text=f"Last added: [{lon:.8f}, {lat:.8f}]", fg="black")
        update_display()

    def copy_to_clipboard():
        text = format_coords()
        root.clipboard_clear()
        root.clipboard_append(text)
        status_label.config(text="Copied to clipboard", fg="green")

    def clear_all():
        coords.clear()
        update_display()
        status_label.config(text="Cleared", fg="black")

    root = tk.Tk()
    root.title("Quick Coords Collector")

    input_frame = tk.LabelFrame(root, text="Add Coordinate")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    tk.Label(input_frame, text="Longitude").grid(row=0, column=0)
    tk.Label(input_frame, text="Latitude").grid(row=0, column=1)

    longitude_entry = tk.Entry(input_frame, width=18)
    latitude_entry = tk.Entry(input_frame, width=18)
    longitude_entry.grid(row=1, column=0, padx=5, pady=5)
    latitude_entry.grid(row=1, column=1, padx=5, pady=5)

    add_btn = tk.Button(input_frame, text="Add", command=add_coordinate, width=10)
    add_btn.grid(row=1, column=2, padx=5)

    controls_frame = tk.Frame(root)
    controls_frame.grid(row=1, column=0, sticky="w", padx=10)

    copy_btn = tk.Button(controls_frame, text="Copy to clipboard", command=copy_to_clipboard)
    copy_btn.grid(row=0, column=0, padx=(0,10))

    clear_btn = tk.Button(controls_frame, text="Clear", command=clear_all)
    clear_btn.grid(row=0, column=1)

    count_label = tk.Label(controls_frame, text="Count: 0")
    count_label.grid(row=0, column=2, padx=(10,0))

    status_label = tk.Label(root, text="", anchor="w")
    status_label.grid(row=3, column=0, sticky="w", padx=10, pady=(4,0))

    output_frame = tk.LabelFrame(root, text="Output")
    output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="we")

    output_text = tk.Text(output_frame, height=10, width=60, wrap="none")
    output_text.pack(fill="both", expand=True)
    output_text.config(state="disabled")

    # keyboard bindings for quicker usage
    root.bind('<Return>', lambda e: add_coordinate())

    # start with focus at longitude
    longitude_entry.focus()

    root.mainloop()


if __name__ == '__main__':
    main()

