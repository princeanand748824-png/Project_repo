# Project Summary: Hospital Appointment Scheduler (PS No. 77)

## Overview
The **Hospital Appointment Scheduler** is a Python 3 console application built for clinic receptionists to manage patient appointments using a dictionary keyed by auto-generated IDs (`A101`, `A102`, ...). It supports full CRUD workflows—booking, viewing, rescheduling, and cancelling—within an interactive loop.

## What Was Built
- **`appointment_scheduler.py`**: A clean, modular single-file Python 3 program using `datetime` and `time` for date (`DD-MM-YYYY`) and time (`HH:MM`) validation, enforcing 30-minute slots from `09:00` to `16:30`, managing clinic doctors (`Dr. Mehta`, `Dr. Rao`), and preventing doctor double-bookings.
- **`README.md`**: An in-depth, interactive guide covering project concepts, business rules, setup instructions, menu walkthroughs, and all four test cases with expected outputs.
- **`SUMMARY.md`**: A concise overview of the architecture, requirements coverage, and test readiness.

## Requirements & Test Coverage
- **Console CRUD Menu**: Book (`1`), View All (`2`), Reschedule (`3`), Cancel (`4`), and Exit (`5`) in a continuous loop.
- **Validation & Conflict Rules**: Rejects invalid dates (e.g., `31-11-2026`), invalid times/slots outside `09:00`–`16:30` or off 30-minute intervals, and conflicting doctor bookings.
- **Test Cases 1–4**: Verified to handle normal booking (`A101`), boundary slot booking (`16:30`, `A102`), invalid/conflicting inputs, and rescheduling + cancellation + viewing cleanly.