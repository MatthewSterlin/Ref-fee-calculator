#!/usr/bin/env python
# coding: utf-8
# Matthew Sterling
# Program to calculate referee fees from Justin Lauer's website https://www.justinlauer.net/assignmentsPSJ.html
# Writes output to an excel file

import csv
import requests
from bs4 import BeautifulSoup
import subprocess

# URL of the webpage containing the table
url = "https://www.justinlauer.net/assignmentsPSJ.html"

# Payscale
payscale = {
    "U9": {"referee": 50, "ar1": 0, "ar2": 0},
    "U10": {"referee": 50, "ar1": 0, "ar2": 0},
    "U11": {"referee": 50, "ar1": 25, "ar2": 25},
    "U12": {"referee": 50, "ar1": 25, "ar2": 25},
    "U13": {"referee": 60, "ar1": 30, "ar2": 30},
    "U14": {"referee": 60, "ar1": 30, "ar2": 30},
    "U15": {"referee": 70, "ar1": 35, "ar2": 35},
    "U16": {"referee": 70, "ar1": 35, "ar2": 35},
    "U17": {"referee": 80, "ar1": 40, "ar2": 40},
    "U18": {"referee": 80, "ar1": 40, "ar2": 40},
    "U19": {"referee": 80, "ar1": 40, "ar2": 40}
}

# Store each official's total pay
officials_pay = {}

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the assignments table
    table = soup.find('table', width='180')
    
    if table:
        # Open a CSV file in write mode
        with open("officials_pay.csv", mode="w", newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)
            
            # Write the headers to the CSV file
            csv_writer.writerow(["Date/Time", "Age/Division", "Referee", "AR1", "AR2"])
            
            # Extract table data
            rows = table.find_all('tr')
            
            # Iterate over rows and extract data
            for row in rows[1:]:
                cols = row.find_all(['td', 'th'])
                # Remove Gender, Field, Home, and Visitor columns, remove 7v7 from AR slots
                row_data = [col.text.strip().replace('(7 v 7)', '') for i, col in enumerate(cols) if i not in [2, 4, 6, 7]]
                
                # Assign variables to row_data
                date, time, age, division, referee, ar1, ar2 = row_data
                
                # Calculate pay for each official based on age group
                referee_pay = payscale[age]["referee"]
                ar1_pay = payscale[age]["ar1"]
                ar2_pay = payscale[age]["ar2"]
                
                # Update total pay for each official
                if referee:
                    officials_pay[referee] = officials_pay.get(referee, 0) + referee_pay
                if ar1:
                    officials_pay[ar1] = officials_pay.get(ar1, 0) + ar1_pay
                if ar2:
                    officials_pay[ar2] = officials_pay.get(ar2, 0) + ar2_pay
                
                # Write the data into CSV file
                csv_writer.writerow([f"{date} {time}", f"{age} {division}", f"{referee}", f"{ar1}", f"{ar2}"])
            
            # Write the total pay for each official
            csv_writer.writerow(["Total Pay"])
            for official, total_pay in officials_pay.items():
                csv_writer.writerow([f"{official}", f"${total_pay}"])
        
        print("Data has been written to officials_pay.csv successfully.")
        
        # Opens the CSV file
        subprocess.run(["open", "officials_pay.csv"])
    else:
        print("No assignments posted.")
else:
    print("Failed to fetch the webpage. Status code:", response.status_code)
