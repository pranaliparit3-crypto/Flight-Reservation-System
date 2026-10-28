import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# Flight records are stored as a list of dictionaries.
flights = [
    {
        "flight_no": "AI101",
        "airline": "Air India",
        "source": "Pune",
        "destination": "Delhi",
        "departure": "08:30",
        "arrival": "10:45",
        "fare": 4500,
        "seats": 12,
    },
        {
        "flight_no": "AI112",
        "airline": "Air India",
        "source": "Pune",
        "destination": "Kolhapur",
        "departure": "10:00",
        "arrival": "13:00",
        "fare": 2000,
        "seats": 12,
    },
    {
        "flight_no": "6E204",
        "airline": "IndiGo",
        "source": "Pune",
        "destination": "Delhi",
        "departure": "11:15",
        "arrival": "13:25",
        "fare": 3800,
        "seats": 8,
    },
    {
        "flight_no": "SG302",
        "airline": "SpiceJet",
        "source": "Pune",
        "destination": "Delhi",
        "departure": "19:05",
        "arrival": "21:20",
        "fare": 3450,
        "seats": 10,
    },
    {
        "flight_no": "AI205",
        "airline": "Air India",
        "source": "Mumbai",
        "destination": "Bengaluru",
        "departure": "09:00",
        "arrival": "10:40",
        "fare": 4100,
        "seats": 7,
    },
    {
        "flight_no": "6E411",
        "airline": "IndiGo",
        "source": "Mumbai",
        "destination": "Bengaluru",
        "departure": "17:20",
        "arrival": "19:00",
        "fare": 3600,
        "seats": 9,
    },
    {
        "flight_no": "UK520",
        "airline": "Vistara",
        "source": "Delhi",
        "destination": "Mumbai",
        "departure": "14:10",
        "arrival": "16:00",
        "fare": 5200,
        "seats": 11,
    },
    {
        "flight_no": "9W118",
        "airline": "Jet Airways",
        "source": "Bengaluru",
        "destination": "Pune",
        "departure": "07:50",
        "arrival": "09:30",
        "fare": 3900,
        "seats": 6,
    },
]

# Booking records are stored in memory while the application is running.
bookings = []
booking_counter = 1001


def linear_search_flights(source_filter="", destination_filter=""):
    """Find flights by source and destination using Linear Search."""
    result = []

    for flight in flights:
        source_matches = (
            not source_filter
            or flight["source"].casefold() == source_filter.casefold()
        )
        destination_matches = (
            not destination_filter
            or flight["destination"].casefold() == destination_filter.casefold()
        )

        if source_matches and destination_matches:
            result.append(flight)

    return result


def bubble_sort_flights(flight_list, sort_by):
    """Return a sorted copy of flights using Bubble Sort."""
    result = flight_list.copy()
    n = len(result)

    for i in range(n - 1):
        swapped = False

        for j in range(n - i - 1):
            left = result[j][sort_by]
            right = result[j + 1][sort_by]

            if sort_by == "airline":
                left = left.casefold()
                right = right.casefold()
            elif sort_by in ("departure", "arrival"):
                left = datetime.strptime(left, "%H:%M")
                right = datetime.strptime(right, "%H:%M")

            if left > right:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        # Stop early if this pass made no swaps.
        if not swapped:
            break

    return result


def get_current_flights():
    """Get flights matching the entered route and selected sort option."""
    source = source_var.get().strip()
    destination = destination_var.get().strip()
    sort_option = sort_var.get()

    # Linear Search filters the flights by route.
    result = linear_search_flights(source, destination)

    sort_keys = {
        "Fare (Low to High)": "fare",
        "Departure Time": "departure",
        "Arrival Time": "arrival",
        "Airline Name": "airline",
    }

    # Bubble Sort sorts the filtered flight list.
    return bubble_sort_flights(result, sort_keys.get(sort_option, "fare"))


def refresh_flight_table(show_message=False):
    """Refresh the flight table using the current search and sort values."""
    result = get_current_flights()

    for row in flight_table.get_children():
        flight_table.delete(row)

    for flight in result:
        flight_table.insert(
            "",
            "end",
            values=(
                flight["flight_no"],
                flight["airline"],
                flight["source"],
                flight["destination"],
                flight["departure"],
                flight["arrival"],
                f'{flight["fare"]:,}',
                flight["seats"],
            ),
        )

    status_var.set(f"{len(result)} flight(s) displayed.")

    if show_message and not result:
        messagebox.showinfo(
            "Search Result",
            "No flights found for the selected source and destination.",
        )


def search_flights():
    """Validate search fields and display matching flights."""
    source = source_var.get().strip()
    destination = destination_var.get().strip()

    if not source or not destination:
        messagebox.showwarning(
            "Missing Route",
            "Please enter both source and destination to search for a route.",
        )
        return

    refresh_flight_table(show_message=True)


def reset_filters():
    """Clear route filters and show all flights."""
    source_var.set("")
    destination_var.set("")
    sort_var.set("Fare (Low to High)")
    refresh_flight_table()


def book_selected_flight():
    """Book one or more seats on the selected flight."""
    global booking_counter

    selected_items = flight_table.selection()
    if not selected_items:
        messagebox.showwarning(
            "Selection Required", "Please select a flight from the table first."
        )
        return

    selected_values = flight_table.item(selected_items[0], "values")
    flight_no = selected_values[0]

    # Find the selected flight record in the list.
    selected_flight = None
    for flight in flights:
        if flight["flight_no"] == flight_no:
            selected_flight = flight
            break

    if selected_flight is None:
        messagebox.showerror("Flight Error", "The selected flight was not found.")
        return

    passenger_name = passenger_name_var.get().strip()
    if not passenger_name:
        messagebox.showwarning("Missing Name", "Please enter the passenger name.")
        return

    try:
        seat_count = int(seat_count_var.get())
    except ValueError:
        messagebox.showwarning(
            "Invalid Seats", "Please enter the number of seats as a whole number."
        )
        return

    if seat_count <= 0:
        messagebox.showwarning(
            "Invalid Seats", "The number of seats must be greater than zero."
        )
        return

    if selected_flight["seats"] < seat_count:
        messagebox.showwarning(
            "Seats Unavailable",
            f'Only {selected_flight["seats"]} seat(s) are available '
            f'for flight {selected_flight["flight_no"]}.',
        )
        return

    total_cost = selected_flight["fare"] * seat_count
    booking = {
        "booking_id": f"BK{booking_counter}",
        "passenger": passenger_name,
        "flight_no": selected_flight["flight_no"],
        "airline": selected_flight["airline"],
        "source": selected_flight["source"],
        "destination": selected_flight["destination"],
        "seats": seat_count,
        "fare": selected_flight["fare"],
        "total_cost": total_cost,
    }

    booking_counter += 1
    bookings.append(booking)
    selected_flight["seats"] -= seat_count

    passenger_name_var.set("")
    seat_count_var.set("1")

    refresh_flight_table()
    refresh_booking_table()

    messagebox.showinfo(
        "Booking Confirmed",
        f'Booking successful!\n\n'
        f'Booking ID: {booking["booking_id"]}\n'
        f'Passenger: {booking["passenger"]}\n'
        f'Flight: {booking["flight_no"]}\n'
        f'Route: {booking["source"]} -> {booking["destination"]}\n'
        f'Seats: {booking["seats"]}\n'
        f'Total Cost: Rs. {booking["total_cost"]:,}',
    )


def refresh_booking_table():
    """Display all bookings in the booking table."""
    for row in booking_table.get_children():
        booking_table.delete(row)

    for booking in bookings:
        booking_table.insert(
            "",
            "end",
            values=(
                booking["booking_id"],
                booking["passenger"],
                booking["flight_no"],
                booking["airline"],
                booking["source"],
                booking["destination"],
                booking["seats"],
                f'{booking["total_cost"]:,}',
            ),
        )


# ----------------------- Main Window -----------------------

root = tk.Tk()
root.title("Flight Reservation System - Searching and Sorting")
root.geometry("1180x790")
root.minsize(1000, 680)
root.configure(bg="#f3f6fb")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
style.configure("Treeview", rowheight=25, font=("Arial", 9))
style.configure("Treeview.Heading", font=("Arial", 9, "bold"))

main_frame = tk.Frame(root, bg="#f3f6fb", padx=18, pady=16)
main_frame.pack(fill="both", expand=True)

# Header
header_frame = tk.Frame(main_frame, bg="#f3f6fb")
header_frame.pack(fill="x", pady=(0, 12))

tk.Label(
    header_frame,
    text="FLIGHT RESERVATION SYSTEM",
    font=("Arial", 22, "bold"),
    fg="#0d3b66",
    bg="#f3f6fb",
).pack(anchor="w")

tk.Label(
    header_frame,
    text="DSA Mini Project | Linear Search and Bubble Sort",
    font=("Arial", 11),
    fg="#4b5563",
    bg="#f3f6fb",
).pack(anchor="w", pady=(4, 0))

# Search and sorting controls
search_frame = tk.LabelFrame(
    main_frame,
    text="Search and Sort Flights",
    bg="white",
    fg="#0d3b66",
    padx=12,
    pady=10,
)
search_frame.pack(fill="x", pady=(0, 10))

source_var = tk.StringVar()
destination_var = tk.StringVar()
sort_var = tk.StringVar(value="Fare (Low to High)")
status_var = tk.StringVar(value="Ready.")

tk.Label(
    search_frame, text="From:", bg="white", font=("Arial", 10, "bold")
).grid(row=0, column=0, padx=5, pady=6, sticky="w")

tk.Entry(
    search_frame, textvariable=source_var, width=16, font=("Arial", 10)
).grid(row=0, column=1, padx=5, pady=6)

tk.Label(
    search_frame, text="To:", bg="white", font=("Arial", 10, "bold")
).grid(row=0, column=2, padx=5, pady=6, sticky="w")

tk.Entry(
    search_frame, textvariable=destination_var, width=16, font=("Arial", 10)
).grid(row=0, column=3, padx=5, pady=6)

tk.Label(
    search_frame, text="Sort By:", bg="white", font=("Arial", 10, "bold")
).grid(row=0, column=4, padx=5, pady=6, sticky="w")

ttk.Combobox(
    search_frame,
    textvariable=sort_var,
    values=[
        "Fare (Low to High)",
        "Departure Time",
        "Arrival Time",
        "Airline Name",
    ],
    state="readonly",
    width=19,
).grid(row=0, column=5, padx=5, pady=6)

tk.Button(
    search_frame,
    text="Search",
    command=search_flights,
    bg="#0d6efd",
    fg="white",
    padx=14,
).grid(row=0, column=6, padx=5, pady=6)

tk.Button(
    search_frame,
    text="Show All / Reset",
    command=reset_filters,
    bg="#6c757d",
    fg="white",
    padx=10,
).grid(row=0, column=7, padx=5, pady=6)

# Flight table
flight_frame = tk.LabelFrame(
    main_frame,
    text="Available Flights",
    bg="white",
    fg="#0d3b66",
    padx=8,
    pady=8,
)
flight_frame.pack(fill="both", expand=True)

flight_columns = (
    "Flight No.",
    "Airline",
    "From",
    "To",
    "Departure",
    "Arrival",
    "Fare (Rs.)",
    "Seats",
)

flight_table = ttk.Treeview(
    flight_frame, columns=flight_columns, show="headings", height=8
)

flight_widths = {
    "Flight No.": 100,
    "Airline": 135,
    "From": 105,
    "To": 115,
    "Departure": 100,
    "Arrival": 100,
    "Fare (Rs.)": 110,
    "Seats": 85,
}

for column in flight_columns:
    flight_table.heading(column, text=column)
    flight_table.column(column, width=flight_widths[column], anchor="center")

flight_scroll = ttk.Scrollbar(
    flight_frame, orient="vertical", command=flight_table.yview
)
flight_table.configure(yscrollcommand=flight_scroll.set)
flight_table.pack(side="left", fill="both", expand=True)
flight_scroll.pack(side="right", fill="y")

# Booking input section
booking_frame = tk.LabelFrame(
    main_frame,
    text="Book Selected Flight",
    bg="white",
    fg="#0d3b66",
    padx=12,
    pady=10,
)
booking_frame.pack(fill="x", pady=(10, 0))

tk.Label(
    booking_frame, text="Passenger Name:", bg="white", font=("Arial", 10, "bold")
).grid(row=0, column=0, padx=5, pady=6, sticky="w")

passenger_name_var = tk.StringVar()
tk.Entry(
    booking_frame, textvariable=passenger_name_var, width=25, font=("Arial", 10)
).grid(row=0, column=1, padx=5, pady=6)

tk.Label(
    booking_frame, text="Seats:", bg="white", font=("Arial", 10, "bold")
).grid(row=0, column=2, padx=5, pady=6, sticky="w")

seat_count_var = tk.StringVar(value="1")
tk.Entry(
    booking_frame, textvariable=seat_count_var, width=8, font=("Arial", 10)
).grid(row=0, column=3, padx=5, pady=6)

tk.Button(
    booking_frame,
    text="Book Flight",
    command=book_selected_flight,
    bg="#198754",
    fg="white",
    padx=18,
).grid(row=0, column=4, padx=8, pady=6)

# Booking records table
booking_records_frame = tk.LabelFrame(
    main_frame,
    text="Booking Records",
    bg="white",
    fg="#0d3b66",
    padx=8,
    pady=8,
)
booking_records_frame.pack(fill="both", expand=True, pady=(10, 0))

booking_columns = (
    "Booking ID",
    "Passenger",
    "Flight No.",
    "Airline",
    "From",
    "To",
    "Seats",
    "Total Cost (Rs.)",
)

booking_table = ttk.Treeview(
    booking_records_frame, columns=booking_columns, show="headings", height=4
)

booking_widths = {
    "Booking ID": 95,
    "Passenger": 130,
    "Flight No.": 100,
    "Airline": 120,
    "From": 90,
    "To": 100,
    "Seats": 70,
    "Total Cost (Rs.)": 130,
}

for column in booking_columns:
    booking_table.heading(column, text=column)
    booking_table.column(column, width=booking_widths[column], anchor="center")

booking_scroll = ttk.Scrollbar(
    booking_records_frame, orient="vertical", command=booking_table.yview
)
booking_table.configure(yscrollcommand=booking_scroll.set)
booking_table.pack(side="left", fill="both", expand=True)
booking_scroll.pack(side="right", fill="y")

# Status bar
tk.Label(
    root,
    textvariable=status_var,
    relief="sunken",
    anchor="w",
    padx=8,
    pady=4,
    bg="#e5e7eb",
).pack(fill="x", side="bottom")

# Show all flights and an empty booking table at startup.
refresh_flight_table()
refresh_booking_table()

root.mainloop()
