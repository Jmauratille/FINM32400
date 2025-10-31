# Assignment 3: Explore files using linux command line utilities

# Question 1

wc -l /opt/assignment3/executions.csv > a3_line_count.txt

# Question 2

wc -l /opt/assignment1/trading.fix >> a3_line_count.txt

# Question 3

grep 'MSFT' /opt/assignment3/executions.csv | head -n 10 > a3_msft_count.txt

# Question 4

grep 'MSFT' /opt/assignment1/trading.fix | head -n 10 >> a3_msft_count.txt

# Question 5

cut -d, -f4 /opt/assignment3/executions.csv | sort | uniq > a3_unique_symbols.txt

# Question 6

cut -d, -f4 /opt/assignment3/executions.csv | sort | uniq -c > a3_symbols_count.txt

# Question 7

cut -d, -f4 /opt/assignment3/executions.csv | grep '^NVDA$' > a3_only_nvda.txt

# Question 8

cut -d, -f4 /opt/assignment3/executions.csv | grep -v '^NVDA$' > a3_all_except_nvda.txt
