from datetime import datetime, time


DOCTORS = ["Dr. Mehta", "Dr. Rao"]
SLOT_START = time(9, 0)
SLOT_END = time(16, 30)


def generate_id(counter: int) -> str:
    """Generate auto-incrementing appointment IDs like A101, A102, ..."""
    return f"A{100 + counter}"


def parse_date(date_str: str):
    """Validate and parse date in DD-MM-YYYY format."""
    try:
        return datetime.strptime(date_str.strip(), "%d-%m-%Y").date()
    except ValueError:
        return None


def parse_time(time_str: str):
    """Validate and parse time in HH:MM format."""
    try:
        return datetime.strptime(time_str.strip(), "%H:%M").time()
    except ValueError:
        return None


def is_valid_slot(t: time) -> bool:
    """Check if time is within 09:00 to 16:30 and on a 30-minute boundary."""
    if t is None:
        return False
    if not (SLOT_START <= t <= SLOT_END):
        return False
    if t.minute not in (0, 30) or t.second != 0:
        return False
    return True


def is_doctor_available(appointments: dict, doctor: str, date_str: str, time_str: str, ignore_id: str = None) -> bool:
    """Return True if the doctor has no conflicting appointment at the given date and time."""
    for appt_id, details in appointments.items():
        if ignore_id is not None and appt_id == ignore_id:
            continue
        if (
            details["doctor"].lower() == doctor.lower()
            and details["date"] == date_str
            and details["time"] == time_str
        ):
            return False
    return True


def normalize_doctor(doctor_input: str):
    """Match doctor name case-insensitively against known clinic doctors."""
    cleaned = doctor_input.strip()
    for doc in DOCTORS:
        if doc.lower() == cleaned.lower():
            return doc
    return cleaned if cleaned else None


def book_appointment(appointments: dict, counter: int) -> tuple[int, str | None]:
    """Handle booking a new appointment."""
    patient = input("Patient: ").strip()
    doctor_raw = input("Doctor: ").strip()
    date_str = input("Date: ").strip()
    time_str = input("Time: ").strip()

    if not patient:
        print("Invalid patient name. Please enter a non-empty name.")
        return counter, None

    doctor = normalize_doctor(doctor_raw)
    if not doctor or doctor not in DOCTORS:
        print(f"Invalid doctor. Available doctors: {', '.join(DOCTORS)}.")
        return counter, None

    parsed_date = parse_date(date_str)
    if parsed_date is None:
        print("Invalid date. Please enter the date as DD-MM-YYYY.")
        return counter, None
    formatted_date = parsed_date.strftime("%d-%m-%Y")

    parsed_time = parse_time(time_str)
    if parsed_time is None or not is_valid_slot(parsed_time):
        print("Invalid time slot. Please enter a 30-minute slot between 09:00 and 16:30 (HH:MM).")
        return counter, None
    formatted_time = parsed_time.strftime("%H:%M")

    if not is_doctor_available(appointments, doctor, formatted_date, formatted_time):
        print(f"Slot unavailable: {doctor} already has an appointment on {formatted_date} at {formatted_time}.")
        return counter, None

    new_counter = counter + 1
    appt_id = generate_id(new_counter)
    appointments[appt_id] = {
        "patient": patient,
        "doctor": doctor,
        "date": formatted_date,
        "time": formatted_time,
    }
    print(f"Appointment booked. ID: {appt_id} | {patient} | {doctor} | {formatted_date} {formatted_time}")
    return new_counter, appt_id


def view_appointments(appointments: dict) -> None:
    """Display all scheduled appointments and the total count."""
    if not appointments:
        print("No appointments scheduled.")
        print("Total appointments: 0")
        return

    for appt_id, details in appointments.items():
        print(f"{appt_id} | {details['patient']} | {details['doctor']} | {details['date']} {details['time']}")
    print(f"Total appointments: {len(appointments)}")


def reschedule_appointment(appointments: dict) -> None:
    """Reschedule an existing appointment to a new valid date and time slot."""
    appt_id = input("Appointment ID: ").strip().upper()
    if appt_id not in appointments:
        print(f"Appointment {appt_id} not found.")
        return

    new_date_str = input("New date: ").strip()
    new_time_str = input("New time: ").strip()

    parsed_date = parse_date(new_date_str)
    if parsed_date is None:
        print("Invalid date. Please enter the date as DD-MM-YYYY.")
        return
    formatted_date = parsed_date.strftime("%d-%m-%Y")

    parsed_time = parse_time(new_time_str)
    if parsed_time is None or not is_valid_slot(parsed_time):
        print("Invalid time slot. Please enter a 30-minute slot between 09:00 and 16:30 (HH:MM).")
        return
    formatted_time = parsed_time.strftime("%H:%M")

    doctor = appointments[appt_id]["doctor"]
    if not is_doctor_available(appointments, doctor, formatted_date, formatted_time, ignore_id=appt_id):
        print(f"Slot unavailable: {doctor} already has an appointment on {formatted_date} at {formatted_time}.")
        return

    appointments[appt_id]["date"] = formatted_date
    appointments[appt_id]["time"] = formatted_time
    print(f"Appointment {appt_id} rescheduled to {formatted_date} {formatted_time}.")


def cancel_appointment(appointments: dict) -> None:
    """Cancel an existing appointment by ID."""
    appt_id = input("Appointment ID: ").strip().upper()
    if appt_id not in appointments:
        print(f"Appointment {appt_id} not found.")
        return

    del appointments[appt_id]
    print(f"Appointment {appt_id} cancelled.")


def print_menu() -> None:
    """Display the main receptionist menu."""
    print("\n--- Hospital Appointment Scheduler ---")
    print("1. Book Appointment")
    print("2. View All Appointments")
    print("3. Reschedule Appointment")
    print("4. Cancel Appointment")
    print("5. Exit")


def main() -> None:
    """Run the interactive console loop."""
    appointments = {}
    id_counter = 0

    while True:
        print_menu()
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            id_counter, _ = book_appointment(appointments, id_counter)
        elif choice == "2":
            view_appointments(appointments)
        elif choice == "3":
            reschedule_appointment(appointments)
        elif choice == "4":
            cancel_appointment(appointments)
        elif choice == "5":
            print("Exiting Hospital Appointment Scheduler. Goodbye!")
            break
        else:
            print("Invalid choice. Please select an option from 1 to 5.")


if __name__ == "__main__":
    main()