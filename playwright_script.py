import asyncio

async def run_booking(data):
    print("Received booking data:", data)
    await asyncio.sleep(2)  # Simulate delay
    print("Booking simulation complete.")
