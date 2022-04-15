import pandas as pd
import numpy as np
import sys

current_page = 1
total_pages = 222

while current_page <= total_pages:
	# Define URL
	str1="https://www.daohouer.com/index.php?page="
	str2=str(current_page)
	str3="&hdid=&cjtype=&address="
	URL = str1+str2+str3
	
	# Read Table
	tables = pd.read_html(URL)
	
	# Transform table 
	tb=tables[0]
	tb_string=tb.to_string()
	
	# Print results
	print("URL:"+URL)
	print(tb.to_string())
	
	# Write results into file
	with open('shanghai.txt', 'a') as file:
		file.write("URL: "+URL)
		file.write(tb_string)
	
	# Increment
	current_page+= 1