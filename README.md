
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
email="your-email@example.com"
password="your-secure-password"
```
### 3 Run the Script
Execute the Playwright automation script:
```bash
python async_main.py
```
Extracted data is stored in product.json


Day 2
The total count doesn't seem to get updated it is 1081 but there are more products loading beyond that, also earlier the reason why the seesion cookkes were not getting stored is beacuse we were using a chromium instance that doesn't launch a process from the existing chrome user states and hence no cookies were getting registred nor  restored, now I've implemnted using existing user instance with an account data which will 
store the cookies existing in chrome
