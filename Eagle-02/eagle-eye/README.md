# Eagle Eye

Dashboard di controllo e monitoraggio del progetto **Eagle 02** (team Eagle).

> ⚠️ **Work in progress.** Questa è una versione di test (`eagle_eye_01_test`): l'interfaccia è completa, ma la maggior parte dei pulsanti non è ancora collegata alla logica reale. Lo sviluppo avviene su branch separati e viene portato su `main` solo quando è stabile.

## Cosa fa

- **Dashboard a schermo intero** (Tkinter) con layout fisso 2560×1440, scalato e centrato in base alla finestra.
- **Grafico AI**: andamento dei valori di confidenza dell'inferenza (ultimi 100 punti), con soglia regolabile (`CONF THRESHOLD`) e pulsanti START / PAUSE.
- **Joystick**: lettura di un controller USB (pygame) con visualizzazione dei due stick analogici, dead zone configurabile e log di pulsanti e hat switch.
- **Pannelli di controllo**: pulsanti per controllo robot, strategia, torretta, registrazione e overlay. Ogni click passa da `backend/button_logic.py`, dove va inserita la logica reale.
- **Log input**: ultimi eventi del controller e dei click, con timestamp.

## Requisiti

- Python 3.11
- Tkinter (incluso con Python su Windows/macOS; su Linux: `sudo apt install python3-tk`)
- `pygame` (vedi `requirements.txt`)

## Installazione

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Avvio

```bash
python main.py
```

- `F11` attiva/disattiva lo schermo intero
- `Esc` esce dallo schermo intero
- Il grafico AI parte in pausa: premere **START** per avviarlo

### Test senza modello reale

Per vedere il grafico in funzione con dati finti (random walk):

```bash
python -m tests.ai_feed
```

Il modello reale deve chiamare `model.push(valore)` con il valore di inferenza (0..1); la cartella `tests/` serve solo per prove e può essere eliminata.

## Struttura

```
eagle-eye/
├── main.py              # punto d'ingresso: collega backend e finestra
├── requirements.txt
├── backend/
│   ├── ai_model.py      # valori di confidenza, soglia, stato run/pausa
│   ├── joystick_model.py# posizione e dead zone dei due stick
│   ├── controller.py    # lettura del controller USB (pygame)
│   ├── input_events.py  # formattazione testi del log
│   ├── input_log.py     # ultime righe di log
│   └── button_logic.py  # callback dei pulsanti (da implementare)
├── frontend/
│   ├── app.py, window.py, view.py, viewport.py, theme.py, fonts.py
│   ├── buttons/         # layout, pannello e logica dei pulsanti
│   ├── inputs/          # campo soglia
│   ├── static/          # griglia e testi fissi
│   └── widgets/         # grafico AI, vista joystick, log input
└── tests/
    └── ai_feed.py       # dati finti per il grafico (solo test)
```

## Configurazione rapida

- **Assi degli stick**: se non corrispondono al tuo controller, modifica `STICK_AXES` in `backend/controller.py`.
- **Nomi dei pulsanti del controller**: `BUTTON_NAMES` in `backend/controller.py`.
- **Soglia di default**: `DEFAULT_THRESHOLD` in `main.py`.
- **Aggiungere un pulsante**: in `frontend/buttons/layout.py`, **in fondo** a `BUTTONS` (gli id sono le posizioni, non vanno cambiati).

## Workflow di sviluppo

1. Si lavora su un branch (`feature/...`).
2. Si testa in locale.
3. Si fa il merge su `main` solo a versione funzionante.

## Team

Progetto **Eagle 02** — team **Eagle**.
