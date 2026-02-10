import tkinter as tk
import folium
import openrouteservice as ors

# --- 1. The GUI Function ---
def get_user_coordinates():
    # This list lives inside the function
    coords = []

        lines = []
        for lon, lat in coords:
            lines.append(f"  [{lon:.8f}, {lat:.8f}],")
        
        if lines:
            # FIX: changed 'coord' to 'lines' below
            body = "\n".join(lines) 
            return f"coords = [\n{body}\n]"
        else:
            return "coords = [\n]"

    def update_display():
    def format_coords():
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
        
        # Add to the list
        coords.append([lon, lat]) 
        
        longitude_entry.delete(0, tk.END)
        latitude_entry.delete(0, tk.END)
        status_label.config(text=f"Last added: [{lon:.8f}, {lat:.8f}]", fg="black")
        update_display()
        longitude_entry.focus()

    def clear_all():
        coords.clear()
        update_display()
        status_label.config(text="Cleared", fg="black")

    # GUI Setup
    root = tk.Tk()
    root.title("Quick Coords Collector")

    input_frame = tk.LabelFrame(root, text="Add Coordinate")
    input_frame.pack(padx=10, pady=10)

    tk.Label(input_frame, text="Longitude").grid(row=0, column=0)
    tk.Label(input_frame, text="Latitude").grid(row=0, column=1)

    longitude_entry = tk.Entry(input_frame, width=15)
    latitude_entry = tk.Entry(input_frame, width=15)
    longitude_entry.grid(row=1, column=0, padx=5)
    latitude_entry.grid(row=1, column=1, padx=5)

    add_btn = tk.Button(input_frame, text="Add", command=add_coordinate)
    add_btn.grid(row=1, column=2, padx=5)

    # Output display
    output_text = tk.Text(root, height=8, width=50)
    output_text.pack(padx=10, pady=5)
    output_text.config(state="disabled")
    
    count_label = tk.Label(root, text="Count: 0")
    count_label.pack()
    
    status_label = tk.Label(root, text="")
    status_label.pack()

    # Bind Enter key
    root.bind('<Return>', lambda e: add_coordinate())
    longitude_entry.focus()

    # Start the loop
    print("Please enter coordinates. Close the window to generate the map...")
    root.mainloop()
    
    # --- CRITICAL FIX: Return the data ---
    return coords

# --- 2. Main Execution Flow ---

# Call the function and catch the result in a variable named 'coords'
# The script will PAUSE here until you close the popup window.
coords = get_user_coordinates()

# Check if user actually entered data
if not coords:
    print("No coordinates entered. Exiting.")
else:
    print(f"Processing {len(coords)} coordinates...")

    # --- 3. Your Routing Logic ---
    
    # DEFINE vehicle_start manually if it's not defined elsewhere
    # Assuming start is the first coordinate entered, or set your own:
    if len(coords) > 0:
        vehicle_start = coords[0] 
    else:
        vehicle_start = [104.7610533, -2.9944282]

    # Map Setup
    m = folium.Map(location=list(reversed(vehicle_start)), tiles='cartodbpositron', zoom_start=13)

    # Add Markers
    for coord in coords:
        folium.Marker(location=list(reversed(coord))).add_to(m)

    folium.Marker(location=list(reversed(vehicle_start)), icon=folium.Icon(color="red")).add_to(m)

    # Vehicles setup
    vehicles = [
        ors.optimization.Vehicle(id=0, profile='driving-car', start=vehicle_start, end=vehicle_start, capacity=[5]),
        ors.optimization.Vehicle(id=1, profile='driving-car', start=vehicle_start, end=vehicle_start, capacity=[5])
    ]

    # Jobs setup (Fixed naming issue in list comprehension)
    jobs = [ors.optimization.Job(id=index, location=c, amount=[1]) for index, c in enumerate(coords)]

    # Optimization (Mocked client call - assuming 'client' is already defined in your notebook)
    # optimized = client.optimization(jobs=jobs, vehicles=vehicles, geometry=True)
    
    # NOTE: Since I cannot run the ORS client here, the map 'm' currently shows the markers only.
    # Uncomment your optimization line above to draw lines.
    
    # Display map
    display(m)
