import cv2
import time
import os
# Metoda Cascade z OpenCv
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
start_time = None

folder_path = "C:/Users/Oliwia/Desktop/twarze"
os.makedirs(folder_path, exist_ok=True)
existing_files = os.listdir(folder_path)
photo_count = 0

# Użycie kamery piewszej
camera = cv2.VideoCapture(0)

# Test czy kamera się otwiera, jeśli nie program się wyłącza
if not camera.isOpened():
    print("Nie można odpalić kamery")
    exit()

# Główna pętla programu, odczytywanie klatek
while True:
    ret, frame = camera.read()
    if not ret:
        print("Nie udało się odczytać kamery")
        break
    # Użycie szarego filtra dla lepszego wykrywania twarzy
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Rozmiar wykrywanych twarzy
    face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(30, 30))
    # Warunek który sprawdza czy twarz jest w kadrze, jeśli tak odpala licznik który liczy ilość sekund
    if len(face) > 0:
        if start_time == None:
            start_time = time.time()
        elapsed = time.time() - start_time
        message = f"Czas twarzy na kamerze {int(elapsed)}"
    else:
        start_time = None
        message = "Brak twarzy w kadrze"


    # Wytworzenie kółka wokół twarzy
    for (x, y, w, h) in face:
        center = (x + w // 2, y + h // 2)
        radius = w // 2
        cv2.circle(frame, center, radius, (255, 0, 32), 3)

    local = time.localtime()
    date = f"{local.tm_year}-0{local.tm_mon}-0{local.tm_mday}"
    # Nałożenie tekstu który wyświetla ilość czasu twarzy w kadrze
    cv2.putText(frame, message, (0, 20),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (125, 0, 255), 2)
    # Nałożenie tekstu który wyświetla aktualną date
    cv2.putText(frame, date, (510, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    # Pokazanie kamery
    cv2.imshow("Camera", frame)

    # Jeśli zostanie kliknięte q, program przestaje działą
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    if cv2.waitKey(1) & 0xFF == ord("p"):
        photo_path = os.path.join(folder_path, f"{photo_count:03d}.jpg")
        cv2.imwrite(photo_path, frame)
        photo_count += 1

camera.release()
cv2.destroyAllWindows()
