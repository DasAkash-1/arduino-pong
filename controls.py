import serial


# arduino connect, timeout=0 mane game atkabe na
ser = serial.Serial("/dev/cu.usbmodem11301", 9600, timeout=0)

mn = 5
mx = 17

buf = ""          # adha line gulo ekhane jomabe
history1 = []     # left er last kothok ta reading
history2 = []     # right er last kothok ta reading
distance1 = 11    # left filter howa distance
distance2 = 11    # right filter howa distance


def update():
    global buf, distance1, distance2

    # serial e ja ashche shob poro
    if ser.in_waiting:
        buf += ser.read(ser.in_waiting).decode(errors="ignore")

        lines = buf.split("\n")
        buf = lines[-1]               # shesh adha line ta rekhe dao

        for l in lines[:-1]:
            parts = l.strip().split(",")    # "12,15" ke 12 ar 15 e bhag

            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                v1 = int(parts[0])
                v2 = int(parts[1])

                # left
                if 2 <= v1 <= 60:
                    v1 = max(mn, min(mx, v1))
                    history1.append(v1)
                    if len(history1) > 5:
                        history1.pop(0)
                    distance1 = sorted(history1)[len(history1) // 2]

                # right
                if 2 <= v2 <= 60:
                    v2 = max(mn, min(mx, v2))
                    history2.append(v2)
                    if len(history2) > 5:
                        history2.pop(0)
                    distance2 = sorted(history2)[len(history2) // 2]