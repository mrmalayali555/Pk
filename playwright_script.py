import asyncio
from playwright.async_api import async_playwright
import os
import traceback # Import for better error logging

# --- Start of content from goethe_booker.py (Codes and book_slot function) ---
location_codes = {
    "Bangalore": "ban",
    "Chennai": "che",
    "Kolkata": "kol",
    "Mumbai": "mum",
    "New Delhi": "new",
    "Pune": "pun"
}

level_codes = {
    "Goethe-Zertifikat A1": "gzsd1",
    "Goethe-Zertifikat A2": "gzsd2",
    "Goethe-Zertifikat B1": "gzb1",
    "Goethe-Zertifikat B2": "gzb2",
    "Goethe-Zertifikat C1": "gzc1",
    "Goethe-Zertifikat C2": "gzc2"
}

async def book_slot(playwright, email, password, level, location, start_date, end_date, max_retries=3):
    retries = 0
    while retries < max_retries:
        browser = None
        context = None

        try:
            browser = await playwright.chromium.launch(
                # Change headless=False to headless=True for deployment on Railway
                headless=True, # IMPORTANT: Set to True for server deployment!
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                # Add pre_payment_state.json cookies if needed for persistent session
                # If pre_payment_state.json contains actual cookies for login, load them here
                # Example (you might need to adjust based on exact content of your json):
                # storage_state={"cookies": [{"name": "cookie_name", "value": "cookie_value", ...}]}
            )
            page = await context.new_page()

            # The Goethe website's initial URL
            await page.goto("https://www.goethe.de/ins/in/en/sta/coe/prf.html") # Assuming this is the initial page

            # Your existing logic from goethe_booker.py goes here
            # I'm extracting key parts based on the snippet provided, you'll need to fill in specifics for your actual website structure.

            # Example: Selecting location and level (replace with actual selectors)
            # await page.select_option('select#location-dropdown', value=location_codes.get(location))
            # await page.select_option('select#level-dropdown', value=level_codes.get(level))
            # await page.click('button#search-button')

            # --- Add all your detailed Playwright steps here from your goethe_booker.py ---
            # This is where your precise automation steps for navigating the Goethe website
            # and making selections (dates, times) will go.
            # E.g., await page.fill("#username", email)
            # E.g., await page.fill("#password", password)
            # E.g., await page.click("text=Login")
            # E.g., await page.click(f"button[data-date='{start_date}']") # Example for date selection
            # E.g., await page.click(f"div.time-slot:has-text('{hour:02d}:{minute:02d}')") # Example for time selection

            # Placeholder for actual automation
            print(f"Playwright navigated to initial page for {level} in {location}.")
            print("Remaining Goethe booking steps need to be filled in here.")
            await asyncio.sleep(5) # Simulate work

            print("Goethe automation completed (placeholder).")
            return True # Indicate success

        except Exception as e:
            print(f"Attempt {retries+1} failed: {e}")
            print(traceback.format_exc()) # Print full traceback for debugging
            if browser:
                await browser.close() # Ensure browser is closed on failure
            retries += 1
            await asyncio.sleep(5) # Wait before retrying
    print("Max retries reached. Booking failed.")
    return False

# --- End of content from goethe_booker.py ---


async def run_booking(data):
    print("Received booking data in run_booking:", data)

    user_file_path = data.get('user_file')
    if not user_file_path or not os.path.exists(user_file_path):
        print(f"Error: User file not found at {user_file_path}")
        return

    email = None
    password = None
    try:
        with open(user_file_path, 'r') as f:
            lines = f.readlines()
            if lines:
                user_credentials = lines[0].strip().split(',')
                if len(user_credentials) == 2:
                    email = user_credentials[0]
                    password = user_credentials[1]
                else:
                    print("Error: Invalid format in users.txt. Expected 'email,password'")
            else:
                print("Error: users.txt is empty.")
    except Exception as e:
        print(f"Failed to read user credentials from {user_file_path}: {e}")
        return

    if not email or not password:
        print("Error: Email or password not found from users.txt.")
        return

    print(f"Attempting booking for {email}...")

    async with async_playwright() as p:
        success = await book_slot(
            p,
            email,
            password,
            data['level'],
            data['location'],
            data['start_date'],
            data['end_date']
        )
        if success:
            print("Overall Booking Process Completed Successfully.")
        else:
            print("Overall Booking Process Failed after retries.")
