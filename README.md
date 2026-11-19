# projectAchill

Testskripte für das Sprachmodell **Julia-1** von SupersonicLabs. Die Skripte lassen das Modell Szenenbeschreibungen eines Roboters auswerten (Position des Ziels, Entfernung, Hindernis) und vergleichen die Antworten mit der richtigen Lösung.

## Voraussetzungen

- Python 3 (inkl. `pip`)
- Internetverbindung für den Download des Modells

## Installation

Alle Befehle werden im Projektordner ausgeführt.

### 1. Virtuelle Umgebung anlegen

Eine virtuelle Umgebung (`.venv`) hält die Pakete dieses Projekts getrennt von deiner restlichen Python-Installation.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Wenn die Umgebung aktiv ist, steht `(.venv)` vor der Eingabezeile.

### 2. Modell herunterladen

Zuerst wird `huggingface_hub` installiert, damit wird anschließend das Modell von Hugging Face in den Ordner `Julia-1` geladen:

```bash
python -m pip install huggingface_hub
```

```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download('SupersonicLabs/Julia-1', local_dir='Julia-1')"
```

### 3. Paket installieren

Das heruntergeladene Modell enthält das Python-Paket `julia`, das von den Skripten importiert wird. Es wird im Entwicklungsmodus (`-e`) installiert:

```bash
python -m pip install -e ./Julia-1
```

> **Tipp für Linux:** Vorher die CPU-Version von PyTorch installieren. So wird nicht die deutlich größere GPU-Version heruntergeladen:
>
> ```bash
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> ```

## Projekt ausführen

1. Virtuelle Umgebung aktivieren (bei jedem neuen Terminal nötig):

   ```bash
   source .venv/bin/activate
   ```

   Unter Windows: `.venv\Scripts\Activate.ps1`

2. Gewünschtes Skript starten:

   ```bash
   python "Dateiname.py"
   ```

   Zum Beispiel:

   ```bash
   python test_julia.py
   ```

### Enthaltene Skripte

| Datei | Beschreibung |
|---|---|
| `test_julia.py` | Basistest des Modells mit Szenenbeschreibungen |
| `test_hard.py` | Schwierigere Testfälle |
| `test_hard2.py` | Weitere schwierige Testfälle |
