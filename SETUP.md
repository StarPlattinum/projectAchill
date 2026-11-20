# RoboMaster S1 – System-1 Setup & Log

Dokumentation der Hardware-Anbindung für das Praktikum "System und KI-Sicherheit".
Ziel: System-1 (Julia-Decision-Model) läuft auf dem PC, entscheidet anhand des
Kamerabilds und steuert den RoboMaster S1 über WLAN.

Stand: 2026-11-20 — **Hardware-Pipeline läuft** (Verbindung, Kamera, Fahren).

---

## 1. Ausgangslage / Problem

- Offizielles Python-SDK unterstützt nur RoboMaster **EP**, nicht den **S1**.
- Beim S1 muss das SDK per Root-Hack freigeschaltet und das EP-SDK aufgespielt werden.
- Unsere Firmware ist **gepatcht**: der klassische Root-Snippet wird von DJI geblockt
  (Konsole zeigt dann `Exception: Thank you for making us progress together`).

## 2. Root freischalten (einmalig, über USB)

1. `adb` installiert (Android Platform Tools), per USB an den **Intelligent Controller**
   (Einheit oben auf dem Turm, microUSB-Port).
2. In der RoboMaster-App: Lab → DIY Programming → Python, folgenden Snippet ausführen.
   **Wichtig:** `subprocess` wird als `'sub'+'process'` zusammengesetzt, um DJIs
   String-Filter zu umgehen — nur so läuft es auf gepatchter Firmware durch.

   ```python
   def root_me(module):
       __import__ = rm_define.__dict__['__builtins__']['__import__']
       return __import__(module, globals(), locals(), [], 0)

   builtins = root_me('builtins')
   sub_process = root_me('sub' + 'process')
   proc = sub_process.Popen('/system/bin/adb_en.sh', shell=True,
                            executable='/system/bin/sh',
                            stdout=sub_process.PIPE, stderr=sub_process.PIPE)
   ```

3. Erfolg = Konsole zeigt `Execution Complete`. App **offen lassen**.
4. Prüfen: `adb devices` zeigt das Gerät, `adb shell` gibt eine Root-Shell
   (`root@xw607_dz_ap0002_v4:/ #`).

## 3. SDK aufspielen ("Flashen")

Vorher **Original sichern**:
```
adb pull /data/dji_scratch/bin/dji_scratch.py .\backup\
```
(Der `sdk`-Ordner existiert vor dem Flash noch nicht — normal.)

SDK-Paket: `s1_SDK` aus dem `dora-robomaster`-Datensatz (Hugging Face), enthält
`dji_scratch/`, `upload.sh`, `patch.sh`, `dji.json`, `dji_hdvt_uav`.

**Hinweis:** `./upload.sh` in Git Bash hing bei uns (MinTTY verträgt sich nicht mit
`adb.exe`). Deshalb die Befehle direkt in PowerShell ausführen:

```powershell
cd <pfad>\s1_sdk_hack
$adb = "<pfad>\platform-tools\adb.exe"

& $adb shell rm -rf /data/dji_scratch/sdk
& $adb push dji_scratch\sdk /data/dji_scratch/.
& $adb push dji_scratch\bin\dji_scratch.py /data/dji_scratch/bin/.
& $adb push dji.json /data/.
& $adb push dji_hdvt_uav /data/.
& $adb shell chmod 755 /data/dji_hdvt_uav
& $adb push patch.sh /data/.
```

Gegencheck: `& $adb shell ls /data/dji_scratch/` → `sdk` muss jetzt gelistet sein.

**Neustart:** S1 aus/an. **Zwei Startmelodien statt einer** = Flash aktiv.
Der Flash liegt auf `/data` und bleibt dauerhaft — kein erneutes Rooten/Flashen nötig.

## 4. PC-Seite (Python-SDK)

```powershell
cd C:\Users\PC\projectAchill
py -m venv robovenv            # "python" wird vom Windows-Store-Alias abgefangen -> "py"
.\robovenv\Scripts\activate
pip install robomaster-sdk-modern
```

## 5. Verbindung & Hello World

- S1 + Laptop im **gleichen Netz** (Hotspot/Router = `sta`) oder direkt
  ins S1-WLAN (`RMS1-...` = `ap`).
- **RoboMaster-App vorher schließen** — sonst belegt sie den Discovery-Port
  (`WinError 10048`) und die Verbindung schlägt fehl.

`hello_robo.py`:
```python
import cv2
from robomaster import robot

ep = robot.Robot()
ep.initialize(conn_type="sta")      # "ap" für Direkt-Modus
print("verbunden")

cam = ep.camera
cam.start_video_stream(display=False)
img = cam.read_cv2_image(timeout=5)
cv2.imwrite("frame.jpg", img)
cam.stop_video_stream()
print("Bild gespeichert: frame.jpg")

ep.chassis.move(x=0.5, y=0, z=0, xy_speed=0.5).wait_for_completed()
print("gefahren")

ep.close()
```
Ausführen: `python hello_robo.py` → `verbunden` / `frame.jpg` / `gefahren`.

## 6. Wieder-Anfangen (Checkliste)

1. S1 an, auf zwei Töne hören.
2. S1 + Laptop ins gleiche Netz (oder Direkt-Modus).
3. **RoboMaster-App schließen** (Port!).
4. `.\robovenv\Scripts\activate`
5. `python hello_robo.py`

## 7. Stolpersteine (damit wir sie nicht nochmal suchen)

- Gepatchte Firmware → `'sub'+'process'`-Trick nötig.
- Git Bash hängt bei `adb` → Pushes in PowerShell machen.
- `python` nicht gefunden → `py` nutzen (Store-Alias).
- `WinError 10048` / Verbindung schlägt fehl → RoboMaster-App schließen.
- Hotspot blockt Geräte-zu-Geräte (Client-Isolation) → Direkt-Modus `ap`.

## 8. Backup / Rückweg

- `backup\dji_scratch.py` = Original vor dem Flash. Aufbewahren (ins Repo kopieren).
- Bei Problemen: Original zurückpushen + Neustart.

## 9. Nächste Schritte

- [ ] Hello World zu Dauerschleife ausbauen (Frame alle n Sekunden holen).
- [ ] Zustands-Extraktion aus dem Frame (Position / Abstand / Hindernis).
- [ ] Julia-Ausgabe auf `chassis.move(x, y, z, ...)` mappen.
- [ ] Mock-`robot.move(x, y)` durch echtes SDK-Backend ersetzen.
- [ ] Repo out-of-the-box deploybar machen (requirements, Startskript).
