from mindwave import *
import time
import pandas as pd
import glob
import os

def narrativeOption():
    option = raw_input("Fiction or Non Fiction: ").lower()
    song_input = int(raw_input("Select song number 1, 2, 3, 4, 5, 6: "))
    song = songs(song_input)
    if option == "fiction":
        song.insert(0, "Fiction")
    elif option == "non fiction":
        song.insert(0, "Non-Fiction")
    else:
        print("Invalid input")
    return(song)

def songs(song_input):
    if song_input == 1:
        return(["Thoughts of You", "Lo-fi", "84"])
    elif song_input == 2:
        return(["Burn Out", "EDM", "145"])
    elif song_input == 3:
        return(["HandClap", "Pop", "140"])
    elif song_input == 4:
        return(["Firefly", "Lo-fi", "84"])
    elif song_input == 5:
        return(["Rising from the Ashes", "EDM", "136"])
    else:
        return(["Everybody Talks", "Pop", "155"])

def main():
    name = raw_input("Enter participant's name: ")
    filename = "./data/AttentionValue_"+ name + ".csv"
    
    path = sorted(glob.glob('/dev/tty.MindWaveMobile-SerialPo-*'), key=os.path.getsize)
    
    headset = Headset(path[4])

    time.sleep(2)

    headset.connect()
    print("Connecting...")

    while (headset.poor_signal > 5):
        time.sleep(0.5)
    print("Connected.")

    df = pd.DataFrame()

    for i in range(6):
        first_three_col = narrativeOption()
        data = {}
        data["Narrative Form"] = first_three_col[0]
        data["Song"] = first_three_col[1]
        data["Genre"] = first_three_col[2]
        data["BPM"] = first_three_col[3]
        data["Timestamp"] = []
        data["Attention"] = []

        for i in range(10):
            print("Experiment will start in: %s" % (10 - i))
            time.sleep(1)

        t_end = time.time() + 60
        data["Timestamp"].append(0.0)
        data["Attention"].append(headset.attention)
        print("Attention at time %s: %s" % (0.0, headset.attention))
        start = time.time()
        while time.time() < t_end:
            time.sleep(5)
            sample_time = round(time.time() - start)
            print("Attention at time %s: %s" % (sample_time, headset.attention))
            data["Timestamp"].append(sample_time)
            data["Attention"].append(headset.attention)
        df = df.append(data, ignore_index=True)
        df.to_csv(filename, index=False)
main()
