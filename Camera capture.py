import numpy as np
import cv2
from pyzbar import pyzbar
from PIL import Image

YSTART = 16
XSTART = 96
GREEN = np.array([0, 255, 0])

cap = cv2.VideoCapture(0)

i = 1

while True:
    ret, frame = cap.read()

    inner = frame[YSTART:YSTART + 448, XSTART:XSTART + 448].copy()
    frame[YSTART - 2:YSTART + 448 + 2, XSTART - 2:XSTART + 448 + 2] = GREEN
    frame[YSTART:YSTART + 448, XSTART:XSTART + 448] = inner

    barcodes = pyzbar.decode(inner)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect

        cv2.rectangle(inner, (x, y), (x + w, y + h), (255, 0, 0), 2)

        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        text = f"Data: {barcode_data} (Type: {barcode_type})"
        cv2.putText(inner, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        print(f"{barcode_data} ( {barcode_type})")

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w'):
        inner_rgb = cv2.cvtColor(inner, cv2.COLOR_BGR2RGB)

        im = Image.fromarray(inner_rgb)
        im = im.resize((224, 224))
        im.save(f'out{i:04d}.png')
        print(f"图像已保存为 out{i:04d}.png")
        i += 1

cap.release()
cv2.destroyAllWindows()
