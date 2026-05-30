"""Smoke tests for the ELIZA engine and DOCTOR scripts.

Run with:  python -m pytest    (or simply:  python test_eliza.py)
"""

from eliza import load_doctor


def test_scripts_load():
    for lang in ("de", "en"):
        e = load_doctor(lang)
        assert e.initials and e.finals and "xnone" in e.keys


def test_no_unresolved_group_refs():
    """A reassembled answer must never leak a literal group reference like (2)."""
    e = load_doctor("de")
    inputs = [
        "Ich bin sehr traurig",
        "Meine Mutter versteht mich nicht",
        "Ich kann nicht schlafen",
        "Bist du ein Computer?",
        "Erinnerst du dich an gestern?",
        "Alle hassen mich",
        "Ich will glücklich sein",
        "Kannst du mir helfen?",
    ]
    for text in inputs:
        reply = e.respond(text)
        assert reply, f"empty reply for: {text}"
        assert "(" not in reply and ")" not in reply, f"unresolved ref in: {reply!r}"


def test_pronoun_reflection():
    e = load_doctor("de")
    reply = e.respond("Du bist gemein")
    assert "ich" in reply.lower()  # "du bist" -> reflected to "ich ... bin"


def test_quit():
    e = load_doctor("de")
    assert e.respond("tschüss") is None


def test_assets_in_sync():
    """The embedded frontend must match the editable sources in public/."""
    import pathlib
    from eliza_web.assets import ASSETS

    public = pathlib.Path(__file__).resolve().parent / "public"
    expected = {
        "/index.html": "index.html",
        "/style.css": "style.css",
        "/app.js": "app.js",
    }
    for route, name in expected.items():
        assert route in ASSETS, f"missing embedded asset {route}"
        on_disk = (public / name).read_text(encoding="utf-8")
        assert ASSETS[route] == on_disk, (
            f"{name} changed — run: python scripts/build_assets.py"
        )


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("All smoke tests passed.")
