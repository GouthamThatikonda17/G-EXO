"""
=========================================================
Project G-EXO Reminders Tool Adapter
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from tools.models import ToolResult
import reminders

def add_reminder(date: str, time: str, message: str = "") -> ToolResult:
    """Canonical reminder contract mapping directly to storage."""

    # Enforce deterministic default if LLM yields empty message
    if not message or not str(message).strip():
        message = "Reminder"

    reminders.add_reminder(date, time, message)
    return ToolResult(
        success=True,
        message=f"Reminder added: {message} for {date} at {time}"
    )

def show_reminders() -> ToolResult:
    data = reminders.get_reminders()
    if not data:
        return ToolResult(success=True, message="You have no reminders.", data=[])

    lines = ["Your reminders:"]
    for r in data:
        status = r.get("status", "Pending")
        lines.append(f"  {r['id']}. [{status}] {r['message']} at {r['date']} {r['time']}")

    return ToolResult(success=True, message="\n".join(lines), data=data)

def complete_reminder(reminder_id: int) -> ToolResult:
    success = reminders.complete_reminder(reminder_id)
    if success:
        return ToolResult(success=True, message=f"Reminder {reminder_id} marked as completed.")
    return ToolResult(success=False, message=f"Reminder {reminder_id} not found or invalid ID.")

def delete_reminder(reminder_id: int) -> ToolResult:
    success = reminders.delete_reminder(reminder_id)
    if success:
        return ToolResult(success=True, message=f"Reminder {reminder_id} deleted.")
    return ToolResult(success=False, message=f"Reminder {reminder_id} not found or invalid ID.")

def clear_reminders() -> ToolResult:
    reminders.clear_reminders()
    return ToolResult(success=True, message="All reminders cleared.")
