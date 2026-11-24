import serial


# arduino connect, timeout=0 mane game atkabe na
ser = serial.Serial("/dev/cu.usbmodem11301", 9600, timeout=0)

mn = 5
mx = 17

buf = ""
hisL = []
hisR = []
disL = 11    # left er filtered dis
disR = 11    # right


def update():
    global buf, disL, disR

    # serial e ja incoming
    if ser.in_waiting:
        buf += ser.read(ser.in_waiting).decode(errors="ignore")

        lines = buf.split("\n")
        buf = lines[-1]               # shesh adha line keep

        for l in lines[:-1]:
            parts = l.strip().split(",")    # "12,15" ke 12 ar 15 e bhag

            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():

                v1 = int(parts[0])
                v2 = int(parts[1])

                # left
                if 2 <= v1 <= 60:
                    v1 = max(mn, min(mx, v1))
                    hisL.append(v1)
                    if len(hisL) > 5:
                        hisL.pop(0)

                    disL = sorted(hisL)[len(hisL) // 2]


                # right
                if 2 <= v2 <= 60:
                    v2 = max(mn, min(mx, v2))
                    hisR.append(v2)

                    if len(hisR) > 5:
                        hisR.pop(0)
                    disR = sorted(hisR)[len(hisR) // 2]