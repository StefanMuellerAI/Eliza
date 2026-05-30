# ELIZA — Seminar-Demo

Eine interaktive Website mit **ELIZA**, dem Chatbot, den **Joseph Weizenbaum**
1966 am MIT geschrieben hat. Die Demo nutzt **dieselbe Technologie wie das
Original** — Schlüsselwörter, Zerlegungs- und Zusammensetzungsregeln
(*decomposition / reassembly*), **kein** maschinelles Lernen, **kein** LLM.

Gedacht als anschauliche Demonstration für Seminare: Man sieht unmittelbar,
wie überzeugend reine Mustererkennung wirken kann — und wo ihre Grenzen liegen.

![Architektur](https://img.shields.io/badge/Backend-Python-blue) ![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange) ![Deploy](https://img.shields.io/badge/Deploy-Vercel-black)

---

## Live ausprobieren

Nach dem Deploy (siehe unten) einfach die URL öffnen und ELIZA schreiben,
z. B. *„Ich fühle mich oft traurig"* oder *„Meine Mutter versteht mich nicht."*

Über den Umschalter in der Seitenleiste lässt sich zwischen dem **deutschen
Skript** und Weizenbaums **englischem Original-DOCTOR** wechseln.

---

## Wie ELIZA funktioniert

1. **Pre-Substitution** – Eingabe normalisieren (z. B. *wieso → warum*).
2. **Schlüsselwörter ranken** – jedes Wort kann ein gewichtetes Keyword sein
   (*computer* = 50, *familie* = 2 …). Das höchstgewichtete gewinnt.
3. **Decomposition** – die Eingabe wird gegen Muster wie
   `* ich bin * @traurig *` geprüft; `*` sind Platzhalter, `@traurig` ist eine
   Synonymgruppe.
4. **Reassembly** – aus dem Treffer wird eine Antwort gebaut, z. B.
   *„Es tut mir leid zu hören, dass du (3) bist."* Die Gruppe `(3)` wird durch
   den gemerkten Eingabeteil ersetzt.
5. **Post-Substitution** – dabei werden Pronomen gespiegelt
   (*ich → du*, *mein → dein*, *mich → dich* …) — der Kern der ELIZA-Illusion.
6. **Gedächtnis & Variation** – ELIZA wiederholt Antworten nicht stumpf und
   merkt sich frühere Aussagen für später.

> **Didaktischer Hinweis:** Die Pronomen-Spiegelung im Deutschen ist absichtlich
> einfach gehalten (z. B. wird *meine/mein* zu *dein*). Genau solche rauen Kanten
> hatte schon Weizenbaums Original — ein guter Anlass, im Seminar über die
> Grenzen regelbasierter Sprachverarbeitung zu sprechen.

---

## Projektstruktur

```
.
├── api/
│   └── respond.py        # Vercel Serverless Function (Python) – die Chat-API
├── eliza/
│   ├── engine.py         # Pattern-Matching-Engine (decomposition/reassembly)
│   ├── doctor_de.txt     # Deutsches DOCTOR-Skript
│   └── doctor_en.txt     # Weizenbaums englisches Original-Skript
├── public/
│   ├── index.html        # Chat-Oberfläche
│   ├── style.css
│   └── app.js
├── cli.py                # ELIZA im Terminal ausprobieren
├── vercel.json
└── requirements.txt      # (leer – nur Python-Standardbibliothek)
```

Die API ist bewusst **zustandslos**: Das Frontend hält das Gespräch und schickt
bei jeder Anfrage alle bisherigen Nutzer-Nachrichten mit. Der Server spielt sie
durch eine frische ELIZA-Instanz und antwortet auf die letzte — so bleibt
ELIZAs Verhalten erhalten, ohne dass der Server Sitzungen speichern muss.

---

## Lokal ausprobieren

**Im Terminal (ganz ohne Webserver):**

```bash
python cli.py        # deutsches Skript
python cli.py en     # englisches Original
```

**Die komplette Website lokal** (benötigt die [Vercel CLI](https://vercel.com/docs/cli)):

```bash
npm i -g vercel
vercel dev
```

Dann <http://localhost:3000> öffnen.

---

## Auf Vercel deployen

1. Dieses Repository zu GitHub pushen.
2. Auf [vercel.com](https://vercel.com) → **Add New… → Project** → das Repo
   importieren.
3. Keine Einstellungen nötig – Vercel erkennt das statische Frontend in
   `public/` und die Python-Function in `api/` automatisch. **Deploy** klicken.

Alternativ per CLI:

```bash
vercel        # Preview-Deploy
vercel --prod # Produktion
```

---

## Quellen & Lizenz

- J. Weizenbaum, *„ELIZA — A Computer Program For the Study of Natural Language
  Communication Between Man And Machine"*, CACM 9(1), 1966.
- Engine angelehnt an [wadetb/eliza](https://github.com/wadetb/eliza) (MIT).

Lizenz: [MIT](LICENSE) · siehe [NOTICE.md](NOTICE.md) für die Attribution.
