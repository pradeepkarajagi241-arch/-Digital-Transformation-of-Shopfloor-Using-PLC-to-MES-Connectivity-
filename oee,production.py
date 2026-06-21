import mysql.connector
import random
import time

# Production Class
class Production:
    def __init__(self, machine_id, production_count):
        self.machine_id = machine_id
        self.production_count = production_count

    def total_production(self):
        return self.production_count


# OEE Class
class OEE:
    def __init__(self, cycle_time, runtime, total_time, good_count, total_count):
        self.cycle_time = cycle_time
        self.runtime = runtime
        self.total_time = total_time
        self.good_count = good_count
        self.total_count = total_count

    def availability(self):
        return self.runtime / self.total_time

    def performance(self):
        return (self.cycle_time * self.total_count) / self.runtime

    def quality(self):
        return self.good_count / self.total_count

    def oee(self):
        return self.availability() * self.performance() * self.quality()


# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pradeep@123",
    database="oee_db"
)

cursor = conn.cursor()

print("OEE Monitoring Started...")
print("Press Ctrl + C to stop.\n")

try:
    while True:

        # Simulated PLC Data
        production_count = random.randint(50, 200)
        runtime = random.randint(100, 200)
        total_time = random.randint(runtime, 250)
        good_count = random.randint(40, production_count)
        total_count = production_count
        cycle_time = random.randint(1, 10)

        # Create Objects
        prod = Production(1, production_count)

        oee = OEE(
            cycle_time,
            runtime,
            total_time,
            good_count,
            total_count
        )

        # Calculate Values
        production = prod.total_production()
        availability = oee.availability()
        performance = oee.performance()
        quality = oee.quality()
        oee_value = oee.oee()

        # Display Values
        print(f"\nProduction: {production}")
        print(f"Availability: {availability:.2f}")
        print(f"Performance: {performance:.2f}")
        print(f"Quality: {quality:.2f}")
        print(f"OEE: {oee_value:.2f}")

        # Insert into MySQL
        query = """
        INSERT INTO oee_data
        (production_count, availability, performance, quality, oee)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            production,
            availability,
            performance,
            quality,
            oee_value
        )

        cursor.execute(query, values)
        conn.commit()

        print("Data inserted successfully!")

        # Wait 5 seconds
        time.sleep(5)

except KeyboardInterrupt:
    print("\nMonitoring Stopped.")

finally:
    cursor.close()
    conn.close()