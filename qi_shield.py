import pydivert

with pydivert.WinDivert("tcp.DstPort == 80") as w:
    for packet in w:
        if packet.payload and b"TRIGGER" in packet.payload:
            decoy = packet.copy()
            decoy.payload = b"GET /public/index.html HTTP/1.1\r\nHost: safe-access.com\r\n\r\n"
            w.send(decoy)
            
            stealth = packet.copy()
            stealth.payload = bytes.fromhex("5245414C5F444154415F534849454C44")
            w.send(stealth)
            continue

        w.send(packet)