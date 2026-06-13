# Zzz

A small, free keep-awake utility + its download website.
Domain: **zzz-app.com**

> Zzz keeps your computer awake — no sleep, no screensaver, no screen lock —
> by sending a harmless F15 keypress every few minutes. Windows & macOS.

## Project layout

```
zzz/
├── app/                # the desktop tray app (Python)
│   ├── zzz.py          # tray app: toggle on/off, interval ~2/3-4/5 min
│   ├── requirements.txt
│   └── README.md       # run + PyInstaller build instructions
└── site/
    └── index.html      # landing page (self-contained, SEO-ready)
```

## Current status

- App: working. Tray icon (green = active / grey = idle), interval submenu,
  starts active. Built with pynput + pystray + Pillow.
- Site: working single-file landing page. Dark "night" theme, struck-through
  "Zzz" wordmark, auto-detects visitor OS for the download button, FAQ,
  donation section. SEO meta/keywords/Open Graph in place.

## Before going live — 3 things to fill in (search `TODO` in site/index.html)

1. **Download URLs** — replace `github.com/USERNAME/zzz/releases/...` with the
   real links to your uploaded `Zzz-Setup.exe` and `Zzz-mac.zip`.
2. **Donation link** — replace `ko-fi.com/USERNAME` with your real
   Ko-fi / Buy Me a Coffee / PayPal.me link. (Decision still open.)
3. **Version label** — update `v1.0` if needed.

## Build the app (do this on each OS)

See `app/README.md`. Short version:
`pip install pyinstaller` then `pyinstaller --windowed --name Zzz zzz.py`.

## Deploy the site

Easiest: Cloudflare Pages or Netlify — drag the `site/` folder, connect
`zzz-app.com`, HTTPS is automatic (required for any future `.app` domain,
nice-to-have here). Or serve `index.html` with Nginx on the Hetzner VPS.

## Open ideas / next steps

- Decide donation platform and drop in the link.
- Optional: align the tray icon art with the website's struck-through "Zzz"
  wordmark instead of the current coffee cup.
- Optional: set up a GitHub repo + Releases to host the downloads.
- Optional: add a screenshot/GIF of the tray menu to the landing page hero.

## Honest scope note

Zzz is for personal devices. It will generally NOT defeat lock policies on
managed corporate laptops (MDM/Intune/GPO), and IT can detect/block it. Keep
the messaging as a productivity utility, not a way around workplace security.
