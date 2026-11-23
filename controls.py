import serial


# arduino connect, timeout=0 mane game atkabe na
ser = serial.Serial("/dev/cu.usbmodem11401", 9600, timeout=0)

mn = 5  # mn = 5, mx = 17 best, ager(3, 15)
mx = 17

buf = ""          # adha line gulo ekhane jomabe
history = []      # last kothok ta reading ekhane thakbe
distance = 15     # filter howa distance (cm)


def update():
    global buf, distance

    # serial e ja ashche shob poro
    if ser.in_waiting:
        buf += ser.read(ser.in_waiting).decode(errors="ignore")

        lines = buf.split("\n")
        buf = lines[-1]               # shesh adha line lgbe na

        for l in lines[:-1]:
            l = l.strip()
            if l.isdigit():
                v = int(l)
                # print(v)
                if 2 <= v <= 60:      # 0 ba onek boro number ignore

                    # range er baire gele either top or bottom, mane far end e atkibo
                    v = max(mn, min(mx, v))

                    history.append(v)
                    if len(history) > 5:
                        history.pop(0)    # puran ta bad

                    # filter read, avg mane median ta 
                    distance = sorted(history)[len(history) // 2]