import subprocess
import calculate_crew
import webscrape_arrival

def run_scripts_sequentially():
    print("Running webscrape_departure.py...")
    subprocess.run(['python', 'webscrape_departure.py'], check=True)

    print("Running webscrape_arrival.py...")
    subprocess.run(['python', 'webscrape_arrival.py'], check=True)
    
if __name__ == "__main__":
    run_scripts_sequentially()
    calculate_crew.calculate_passengers_and_crew()
