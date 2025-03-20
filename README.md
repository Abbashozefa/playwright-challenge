
# Playwright Automation

## Overview
This project automates a web process using **Playwright with Python**. It logs in using credentials stored in a `.env` file, manages user sessions, extracts data, and saves the results to `product.json`.

---

##  Setup Instructions

### 1 Install Dependencies
Ensure you have Python **3.8+** installed. Then, install the required packages:
```bash
pip install -r requirements.txt
```
Additionally, install Playwright dependencies:
```bash
playwright install
```
### 2 Set Up Environment Variables
Create a .env file in the project directory and add:
```bash
EMAIL=your-email@example.com
PASSWORD=your-secure-password
```
### 3 Run the Script
Execute the Playwright automation script:
```bash
python async_main.py
```
Extracted data is stored in product.json
