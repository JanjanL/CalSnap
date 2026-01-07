import requests
import json

def duckling(text_list:list):
    """
    Parses date and time information from the given text using the Duckling API.

    The function sends a POST request to the Duckling API to parse natural language 
    text into structured time data. It extracts date and time information, formats 
    it, and returns the start and end times.
    """

    # Initialize variables
    date = None
    start_time = None
    end_time = None
    time_number = 0
    timezone = "Asia/Hong_Kong"

    def slice_time(time):
        start_index = time.index('T') + 1
        result = time[start_index:]
        return result

    # 1) Post requests for data prasing
    response = requests.post('http://localhost:8000/parse',
                            data={"text": [text_list], "locale": "zh_HK", "tz": timezone})

    # 2) Store and process parsed date
    if response.status_code == 200:
        parsed_data = response.json()

        # Optionally, write parsed data to a file
        with open('output1.json', 'w') as f:
            json.dump(parsed_data, f)

        for i in parsed_data:
            if i["dim"] == "time":
                if i["value"]["grain"] == "day":
                    date = i["value"]["value"] # output -> '2026-01-20T00:00:00.000+08:00'

                if i["value"]["grain"] == "minute":

                    if time_number == 0 and start_time is None:
                        start_time = i["value"]["value"] # output -> '2026-01-07T10:30:00.000+08:00'
                        start_time = slice_time(start_time)
                        time_number += 1

                    else:
                        end_time = i["value"]["value"] # output -> '2026-01-07T12:30:00.000+08:00'
                        end_time = slice_time(end_time)
    
        # 3) Time formatting
        start_time = date.replace("00:00:00.000-08:00",start_time)
        end_time = date.replace("00:00:00.000-08:00",end_time)

    
    else:
        print("Error:", response.status_code)
    
    return start_time, end_time