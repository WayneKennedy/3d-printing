# Hardware

Verified on the machine 2026-09-01 unless noted.

## Location

**Garage, since 2026-09-06** (previously a desk indoors). The garage roof is **clear
corrugated PVC**, so the space behaves as a greenhouse: very warm in daytime sun, cold
overnight, with ambient varying widely rather than sitting at a steady low temperature. This is
the reverse of the usual "cold garage" assumption and it matters in three places — calibration
results are only meaningful alongside the ambient they were taken at, a long print will cross a
hot/cold cycle, and filament stored here faces heat and sunlight as well as damp.

The printer sits inside a **Creality PVC enclosure**, fitted at the same time as the move. It
buffers cold nights and draughts, which is the half of the problem it can help with; it does
**nothing about solar gain**, and an enclosure inside a greenhouse can run hotter than the room
on a sunny day.

**The enclosure inverts the usual material advice.** Enclosures suit ABS/ASA. PLA and PLA+ are
the materials that dislike them: a warm chamber drives heat creep in a direct-drive hotend,
softening filament above the melt zone and jamming the extruder, and it blunts the aggressive
part cooling PLA depends on (the PLA profiles run 100 % fan).

**Standing practice, decided 2026-09-06: the front and top are left OPEN by default, and closed
only for genuinely cold sessions.** That is the right default for this machine — it prints
mostly PETG and PLA, neither of which wants a hot chamber, and the enclosure's real value here
is buffering cold nights and draughts rather than retaining heat.

This location is **temporary** — the house is a rental, the user moves later in 2026 and plans
a purpose-built garden workshop with much better temperature consistency. Work around the
garage rather than engineering solutions for it.

Measured thermal headroom at the new location (2026-09-06): the bed holds 80 °C on a **34 %
duty cycle** and the hotend 240 °C on 48 %, so there is substantial reserve against a cold
night. Measured at ~25 °C ambient with the enclosure in place. See
[calibration.md](calibration.md#verify-pid-rather-than-re-tuning-it-2026-09-06).

## Printer

- **Creality Ender-5 S1**, stock, no modifications. Bought new, then unused for ~2 years
  before this commissioning.
- Build volume **220 × 220 × 280 mm**, origin front-left.
- **Direct-drive** extruder, 0.4 mm nozzle. Retraction is therefore short (~0.8 mm), not
  Bowden-length.
- **CR-Touch** probe (configured as `[bltouch]`), offsets `x_offset: -13`, `y_offset: 27`.
- Filament runout switch on `PC15`.
- Bed leveling: 4 knurled wheels **under** the bed, `screw_thread: CW-M4`.
  Empirically confirmed: **clockwise as viewed from above raises that corner.**
- **Build surface: textured PEI on spring steel, fitted 2026-09-02.** The Ender-5 S1 uses a
  two-part surface: a magnetic base sheet on the aluminium bed, plus a removable flexible
  **spring-steel plate with textured PEI** on top. The steel plate was mislaid during the years
  the machine sat in the garage, so from commissioning until 2026-09-02 the printer was printing
  **directly onto bare rubberised magnet** — the root cause of the 2026-09-01 layer-1 failures,
  where small isolated features had nothing to key into. Replacement fitted: **235 × 235 mm**
  (plate size; build volume is 220 × 220), double-sided, textured, the standard Creality size
  shared with the Ender-3 S1 family. Textured, not smooth, is deliberate: "gold PEI" describes
  both, and smooth PEI bonds to PETG hard enough to tear its own coating off.
- **The flexible plate matters twice for print-in-place models.** It is why small isolated
  segments stay put while printing, and why they come off intact afterwards: flexing releases
  the whole footprint at once, where a scraper concentrates force at one edge and is exactly
  how a thin joint or a small segment gets snapped. Confirmed in use 2026-09-02.
- **The magnetic base sheet is sound.** Typical rating is 70–80 °C and it has held 80 °C for
  many hours at a stretch (the dragon alone was 8 h 24), so demagnetisation was a live concern.
  Checked by hand on 2026-09-02 with the bed at temperature: firm all over, no corner lift. No
  replacement needed.

### Mainboard

- **Creality CR4NS**, MCU **STM32F401**, stock **64 KiB bootloader**.
- Host link is a **CH340 USB-serial bridge** (`1a86:7523`) wired to **USART1 (PA10/PA9)** —
  *not* the STM32's native USB. Consequences are in
  [klipper-setup.md](klipper-setup.md#flashing).
- Enumerates as `/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0` when the printer is
  powered on. It disappears when the printer is switched off, and Klipper then reports
  `shutdown / Lost communication with MCU` — that is expected, not a fault.
- Factory firmware was `Marlin 2.0.8.2 (Dec 6 2022), MACHINE_TYPE:Ender-5 S1`.

## Host: `printhub`

- **Raspberry Pi 5 Model B Rev 1.1**, 8 GB RAM, NVMe root (235 GB, ~214 GB free).
- Debian 12 bookworm, MainsailOS stack. User `wkenn`.
- Services: `klipper`, `moonraker`, `nginx`, `KlipperScreen` — all enabled and active.
- Klipper `v0.13.0-439-g2cc360894` (host and MCU firmware in lockstep).
- Touchscreen: **QDtech MPI1001** (`0484:5750`), an HID multitouch panel running
  KlipperScreen. Its display blanks on idle; a tap wakes it. Cosmetic only.
- `crowsnest` (webcam daemon) is **active**; the camera was unplugged for the garage move on
  2026-09-06 and refitted the same day. When no camera is attached, `lsusb` shows only the
  touchscreen and the CH340, there is no `/dev/video0` (the `/dev/video*` nodes that remain are
  the Pi's hardware codecs), and the service fails.
- **After replugging the camera, `systemctl restart crowsnest` is not enough.** While the camera
  is absent the service restart-loops until systemd trips its rate limit —
  `Start request repeated too quickly` — and that latched failure survives the camera coming
  back. Clear the counter first:

  ```bash
  ssh wkenn@printhub 'sudo systemctl reset-failed crowsnest && sudo systemctl restart crowsnest'
  ```

  It then finds `/dev/video0` (`Sonix_Technology USB Live camera SN0001`) and starts ustreamer
  normally. Verify with `curl -s "http://localhost:8080/?action=snapshot"` — a healthy frame is
  ~200 KB of JPEG.
- No slicer GUI; PrusaSlicer's CLI (`/usr/bin/prusa-slicer`) is installed for headless
  slicing.

## Network

- Tailnet: **`100.99.147.57`**, MagicDNS `printhub`, tagged **`tag:personal`** to match the
  rest of the fleet. Tailscale SSH is enabled; the tag is what makes the tailnet SSH ACL
  apply, since ACL rules grant by tag and an untagged user-owned node is not covered.
- Wi-Fi `wlan0` holds a **`/22`** address on the house LAN. **That mask is the answer to the
  "wrong subnet" confusion** — `wlan0` and `eth0` sit in what look like two different `/24`s
  but share one `/22`, so they are the same network, not two. Check the prefix length before
  concluding an interface is on the wrong network.
- Ethernet `eth0` is **NO-CARRIER** (cable unplugged) and **does not need to be plugged in.**
  The pre-move worry that Wi-Fi would be the weak link in the garage did not materialise:
  measured there on 2026-09-06, `wlan0` sits at **-47 dBm at 433 Mbit/s** on the house SSID,
  and the
  MCU link is clean under load (`bytes_retransmit=0`, `bytes_invalid=0`, `srtt=0.003`). Wired
  remains the bulletproof fallback if a dropout ever recurs.
- Wi-Fi power-saving is **disabled** three ways after it silently dropped the Pi off the
  network for ~35 min on 2026-08-31: live (`iw dev wlan0 set power_save off`), persistently
  in NetworkManager (`powersave = disable`), and via a `wifi-powersave-off.service` boot
  unit. `iw` lives in `/usr/sbin`, which is not on the user PATH — call it by full path.
- Persistent journald logging was enabled at the same time; before that, logs were volatile
  and the outage could not be diagnosed after the fact.
