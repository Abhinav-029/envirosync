import pandas as pd
import time
import os
import random
import csv
from datetime import datetime


DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)  # creates folder if it doesn't exist

def p(filename):
    return os.path.join(DATA_DIR, filename)

def init_system():
    if not os.path.exists(p("rules.csv")):
        pd.DataFrame({
            'parameter': ['ac_on_temp', 'ac_off_temp', 'heater_on_temp', 'heater_off_temp'],
            'value':     [30, 24, 18, 22]
        }).to_csv(p("rules.csv"), index=False)


        if not os.path.exists(p("current_temp.txt")):
            with open(p("current_temp.txt"), "w") as f:
                f.write("28.0")

        if not os.path.exists(p("current_ac_state.txt")):
            with open(p("current_ac_state.txt"), "w") as f:
                f.write("OFF")

        if not os.path.exists(p("fan_state.txt")):
            with open(p("fan_state.txt"), "w") as f:
                f.write("OFF")

        if not os.path.exists(p("light_intensity.txt")):
            with open(p("light_intensity.txt"), "w") as f:
                f.write(str(random.randint(50, 400)))

        if not os.path.exists(p("light_intensity.txt")):
            with open(p("light_intensity.txt"), "w") as f:
                f.write(str(random.randint(50, 400)))

        if not os.path.exists(p("light_state.txt")):
            with open(p("light_state.txt"), "w") as f:
                f.write("Normal")

        if not os.path.exists(p("occupancy.txt")):
            with open(p("occupancy.txt"), "w") as f:
                f.write("0")

        if not os.path.exists(p("heater_state.txt")):
            with open(p("heater_state.txt"), "w") as f:
                f.write("OFF")
        
        if not os.path.exists(p("ac_temp_state.txt")):
            with open(p("ac_temp_state.txt"), "w") as f:
                f.write("")

        print("✅ System initialized successfully")

init_system()

df = pd.read_csv('data/rules.csv')
rules = dict(zip(df['parameter'], df['value']))
ac_on_temp = int(rules['ac_on_temp'])


def save_current_temp(n):
    with open(p("current_temp.txt"), "w") as f:
        f.write(str(n))

def update_crr_temp():
    with open(p("current_temp.txt"), "r") as f:
        crr_temp = f.read()
        crr_temp = float(crr_temp)
    change = random.uniform(-1.5, 1.5)
    new_temp = round(max(0, min(45, crr_temp + change)), 1)
    save_current_temp(new_temp)

def fetch_room_temp():
    with open(p("current_temp.txt"), "r") as f:
        current_temperature = f.read()
    return float(current_temperature)

def update_ac_state(ac):
    with open(p("current_ac_state.txt"), "w") as f:
        f.write(ac)
    
def fetch_ac_state():
    with open(p("current_ac_state.txt"), "r") as f:
        state = f.read()
    
    return state

def ac_on_off(room_temp):
    prev_state = fetch_ac_state()

    if room_temp > int(rules['ac_on_temp']):
        new_state = "ON"
        reason = "Room Temperature Rise"
    elif room_temp < int(rules['ac_off_temp']):
        new_state = "OFF"
        reason = "Room Temperature Normal"
    else:
        new_state = prev_state
        reason = "Maintaining previous state"

    # log only if state changed
    if new_state != prev_state:
        with open(p('history.txt'), 'a', encoding="utf-8") as f:
            f.write(f"{time.strftime('%B %d, %Y %H:%M:%S')}: AC was Turned {new_state}\n")
            f.write(f"Reason: {reason} ({room_temp}°C)\n\n")

    update_ac_state(new_state)
    return new_state

def show_history():

    if not os.path.exists(p("history.txt")):
        print("No History Found")
        return
    
    with open(p('history.txt'), 'r', encoding="utf-8") as f:
        raw_history = f.read()
        if len(raw_history) > 20:
            history_list = raw_history.split("\n\n")
            for task in history_list[-3:]:
                    print(f"{task}\n")
        else:
             print("No History Found")
        # print(history_list)

def adjust_fan_speed(room_temp):
    if room_temp < 15:
        fan = "OFF"
        reason = "Low room temperature"

    elif 15 <= room_temp <= 25:
        fan = "LOW"
        reason = "Moderate temperature"

    elif 25 < room_temp <= 35:
        fan = "MEDIUM"
        reason = "High temperature"

    else:
        fan = "HIGH"
        reason = "Very high temperature"

    
    if os.path.exists(p("fan_state.txt")):
        with open(p("fan_state.txt"), "r") as f:
            prev_state = f.read()
    else:
        prev_state = ""

    if fan != prev_state:
        with open(p("fan_state.txt"), "w") as f:
            f.write(fan)

        with open(p('history.txt'), 'a', encoding="utf-8") as f:
            f.write(f"{time.strftime('%B %d, %Y %H:%M:%S')}: Fan Speed Set to {fan}\n")
            f.write(f"Reason: {reason} ({room_temp}°C)\n\n")

    return fan

def set_ac_temp(room_temp, ac_state):

    
    if ac_state != "ON":
        return None, "AC is OFF"

    if room_temp < 25:
        ac_temp = 22
        reason = "Comfortable temperature"

    elif 25 <= room_temp < 35:
        ac_temp = 20
        reason = "Moderate room temperature"

    elif 35 <= room_temp < 45:
        ac_temp = 18
        reason = "High room temperature"

    else:
        ac_temp = 16
        reason = "Very high room temperature"

    if os.path.exists(p("ac_temp_state.txt")):
        with open(p("ac_temp_state.txt"), "r") as f:
            prev_temp = f.read()
    else:
        prev_temp = ""

    # log only if temp setting changed
    if str(ac_temp) != prev_temp:

        with open(p("ac_temp_state.txt"), "w") as f:
            f.write(str(ac_temp))

        with open(p("history.txt"), "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%B %d, %Y %H:%M:%S')}: AC temperature set to {ac_temp}°C\n")
            f.write(f"Reason: {reason} ({room_temp}°C)\n\n")

    return ac_temp, reason

def init_light_intensity():
    light = random.randint(0, 500)
    with open(p("light_intensity.txt"), "w") as f:
        f.write(str(light))
    return light

def update_light_intensity():
    
    with open(p("light_intensity.txt"), "r") as f:
        crr_light_intensity = (float(f.read()))

    change_in_light = random.uniform(-40, 40)
    new_light = max(0, min(500, crr_light_intensity + change_in_light))

    with open(p("light_intensity.txt"), "w") as f:
        f.write(str(round(new_light)))
    
def fetch_light_intensity():
    with open(p("light_intensity.txt"), "r") as f:
        light = f.read()

    return float(light)

def light_control():
    lux = fetch_light_intensity()

    if lux < 50:
        state = "Bright"
        reason = f"Room too dark ({lux} lx)"

    elif lux < 150:
        state = "Normal"
        reason = f"Dim Lighting ({lux} lx)"

    elif lux < 300:
        state = "DIM"
        reason = f"Comfort Lighting ({lux} lx)"
    
    else:
        state = "OFF"
        reason = f"Sufficient DayLight"

    if os.path.exists(p("light_state.txt")):
        with open(p("light_state.txt"), "r") as f:
            prev_state = f.read()
    else:
        prev_state = ""

    if state != prev_state:
        with open(p("light_state.txt"), "w") as f:
            f.write(state)

        with open(p("history.txt"), "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%B %d, %Y %H:%M:%S')}: Light State Changed to {state}\n")
            f.write(f"Reason: {reason}\n\n")

    return state

def light_controller():

    update_light_intensity()

    lux = fetch_light_intensity()

    state = light_control()

    return lux, state

def init_occupancy():
    presence = 0
    with open(p("occupancy.txt"), "w") as f:
        f.write(str(presence))

def update_occupancy(presence):
    with open(p("occupancy.txt"), "w") as f:
        f.write(str(presence))

def fetch_occupancy():
    with open(p("occupancy.txt"), "r") as f:
        return int(f.read())
    
def log_occupancy(occupancy, status, empty_duration):
    
    if os.path.exists(p("occupancy_state.txt")):
        with open(p("occupancy_state.txt"), "r") as f:
            prev_state = f.read()
    else:
        prev_state = ""

    current_state = f"{occupancy}-{status}"

    if current_state != prev_state:
        with open(p("occupancy_state.txt"), "w") as f:
            f.write(current_state)

        with open(p("history.txt"), "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%B %d, %Y %H:%M:%S')}: Occupancy = {occupancy}\n")
            f.write(f"Status: {status}\n")
            f.write(f"Empty Duration: {empty_duration} sec\n\n")

    
def log_temperature(temp):
    file_exists = os.path.exists(p("temp_log.csv"))

    with open(p("temp_log.csv"), "a") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Time", "Temperature"])

        writer.writerow([datetime.now().strftime("%H:%M:%S"), temp])


def log_light(lux):
    file_exists = os.path.exists(p("light_log.csv"))

    with open(p("light_log.csv"), "a") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Time", "Light"])
        
        writer.writerow([datetime.now().strftime("%H:%M:%S"), lux])



last_seen_time = time.time()
EMPTY_THRESHOLD = 10

def occupancy_logic(room_temp):
    global last_seen_time

    occupancy = fetch_occupancy()

    if occupancy == 1:
        empty_duration = 0
        last_seen_time = time.time()
        status = "Occupied"

    else:
        empty_duration = int(time.time() - last_seen_time)

        if empty_duration >= EMPTY_THRESHOLD:
            status = "Shutdown"

            if empty_duration == EMPTY_THRESHOLD:
                update_ac_state("OFF")

                with open(p("fan_state.txt"), "w") as f:
                    f.write("OFF")

                with open(p("light_state.txt"), "w") as f:
                    f.write("OFF")
        else:
            status = "Waiting"

    log_occupancy(occupancy, status, empty_duration)

    return {
        "occupancy": occupancy,
        "status": status,
        "empty_duration": empty_duration
    }

def smart_controller():
    update_crr_temp()
    update_light_intensity()

    room_temp = fetch_room_temp()
    lux = fetch_light_intensity()

    log_temperature(room_temp)
    log_light(lux)
    occ_data = occupancy_logic(room_temp)
    occupancy = occ_data["occupancy"]
    status = occ_data["status"]
    empty_duration = occ_data["empty_duration"]

    if status == "Shutdown":
        ac = "OFF"
        fan = "OFF"
        ac_temp = None
        light = "OFF"

    elif occupancy == 1:
        ac = ac_on_off(room_temp)
        fan = adjust_fan_speed(room_temp)
        ac_temp, _ = set_ac_temp(room_temp, ac)
        light = light_control()

    else:
        ac = fetch_ac_state()
        fan = adjust_fan_speed(room_temp)
        ac_temp = None
        light = light_control()

    return {
        "occupancy": occupancy,
        "status": status,
        "empty_duration": empty_duration,
        "room_temp": room_temp,
        "light_intensity": lux,
        "ac": ac,
        "fan": fan,
        "ac_temp": ac_temp,
        "light": light
    }

