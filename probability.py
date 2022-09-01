import datetime
import numpy
import pytz

from google.cloud import bigquery

SECONDS_IN_TWO_HOURS = 2 * 60 * 60
SECONDS_IN_TEN_MIN = 10 * 60

client = bigquery.Client()

query = client.query(f"""
    SELECT number, timestamp
    FROM `bigquery-public-data.crypto_bitcoin.blocks`
    ORDER BY number DESC
""")

points = {}
total_points = 0
previous_time = datetime.datetime.now(tz=pytz.utc)
for row in query:
    total_points += 1
    time_diff = previous_time - row["timestamp"]
    previous_time = row["timestamp"]

    if time_diff.seconds not in points:
        points[time_diff.seconds] = 0
    points[time_diff.seconds] += 1

# While the data should fit a gaussian curve with a peak at ten minutes; the data did not give a normal distribution
# for me. Instead, it was modeled much better by a logarithmic curve
x = numpy.array(list(points.keys()))
y = numpy.array(list(points.values()))
a, b = numpy.polyfit(x, numpy.log(y), 1)
curve = lambda x: a * numpy.log(x) + b

points_at_two_hours = curve(SECONDS_IN_TWO_HOURS)
probability = (points_at_two_hours / total_points) * 100
print(f"There is a {probability}% chance of a block taking 2 or more hours to mine after mining the preceding block")
