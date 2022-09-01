from google.cloud import bigquery
import datetime
import pytz

SECONDS_IN_TWO_HOURS = 2 * 60 * 60

client = bigquery.Client()

query = client.query("""
    SELECT number, timestamp
    FROM `bigquery-public-data.crypto_bitcoin.blocks`
    ORDER BY number
""")

previous_time = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)

total = 0
for row in query:
    time_diff = row["timestamp"] - previous_time
    if time_diff.seconds > SECONDS_IN_TWO_HOURS:
        total += 1
    previous_time = row["timestamp"]

print(f"Total consecutive blocks mines more than 2 hours apart: {total}")
