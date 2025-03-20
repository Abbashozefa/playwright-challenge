import json
import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv
load_dotenv()

async def check_session():
    # Check if session storage exists.
    try:
        with open("session.json", "r") as file:
            return True
    except FileNotFoundError:
        return False

async def login(page, context):
    # Logs into the website and saves session.
    await page.goto("https://hiring.idenhq.com/")  

    await page.fill("input#email", os.getenv('email'))  
    await page.fill("input#password", os.getenv('password'))
    await page.click("button[type='submit']")
    await page.wait_for_selector("text=Sign Out")  # Wait for login confirmation

    # Save session state
    await context.storage_state(path="session.json")
    print("Session saved.")

async def scroll_and_load(page):
    """Scrolls down until all lazy-loaded content is loaded."""
    
    previous_height = None
    while True:
        # Get current page height
        
        height = await page.evaluate("document.body.scrollHeight")
        
        if previous_height == height:
            break  # Stop if no new content loads
        
        
        previous_height = height
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000) 
        
async def navigate_and_extract(page):
    """Navigates to the product table through menu options."""
    await page.goto("https://hiring.idenhq.com/challenge")
    await page.click("text=Menu")  # Click 'Menu' button
    await page.click("text=Data Management")  # Select 'Data Management'
    await page.click("text=Inventory")  # Click 'Inventory'
    await page.click("text=View All Products")  # Open the product table
    await page.click("text=Load Product Table")


    """Extracts product data from the table including lazy load handling."""
    products = []
    await scroll_and_load(page)
    while True:
        # await page.wait_for_selector(".grid.grid-cols-2.md:grid-cols-3.lg:grid-cols-4.gap-4", timeout=10000)
        await page.wait_for_selector(".rounded-lg.border.bg-card.text-card-foreground.shadow-sm.overflow-hidden.animate-fade-in", timeout=10000)

        cards = await page.locator(".rounded-lg.border.bg-card.text-card-foreground.shadow-sm.overflow-hidden.animate-fade-in").all()
        
        for card in cards:
            print(card)
            card_1=await page.locator(".rounded-lg.border.bg-card.text-card-foreground.shadow-sm.overflow-hidden.animate-fade-in").all()
            product = {
                "name": await card.locator(".h-12.flex.items-center.justify-center.font-medium.text-white").text_content(),
                "id": await card.locator("span.font-medium").first.text_content(),
                "color": await card.locator("div.flex.items-center.justify-between:nth-of-type(2) span.font-medium").text_content(),
                "material": await card.locator("div.flex.items-center.justify-between:nth-of-type(3) span.font-medium").text_content(),
                "warranty": await card.locator("div.flex.items-center.justify-between:nth-of-type(4) span.font-medium").text_content(),
            }
            products.append(product)
    
            
        return products

async def save_data(data):
    # Saves extracted data to JSON file.
    with open("products.json", "w") as file:
        json.dump(data, file, indent=2)
    print("Data saved to products.json")

async def main():
    """Main async function to run the Playwright automation."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  
        context = await browser.new_context(storage_state="session.json" if await check_session() else None)
        page = await context.new_page()

        await page.goto("https://hiring.idenhq.com/challenge")  # Replace with actual URL

        if not await page.locator("text=Sign Out").is_visible():
            print("Session not found, logging in...")
            await login(page, context)
        else:
            print("Using existing session.")
        # await page.goto("https://hiring.idenhq.com/challenge")
        # await navigate_to_product_table(page)
        # product_data = await extract_product_data(page)
        product_data =await navigate_and_extract(page)
        await save_data(product_data)

        await browser.close()

# Run the script
asyncio.run(main())
