# Klipper setup

## Config layout

`~/printer_data/config/printer.cfg` is Klipper's official Ender-5 S1 sample
(`printer-creality-ender5-s1-2023.cfg`) plus:

- `[include mainsail.cfg]` and `[include timelapse.cfg]`
- `START_PRINT` / `END_PRINT` macros, with `PRINT_START` / `PRINT_END` aliases
- the `SAVE_CONFIG` autosave block holding PID values, bed mesh and probe Z-offset

The sample's `[mcu] serial:` path already matched the detected CH340 device, so no edit was
needed. Timestamped backups from each `SAVE_CONFIG` sit alongside it as
`printer-2026MMDD_HHMMSS.cfg`.

A snapshot is in [`../reference/printer.cfg`](../reference/printer.cfg).

## Macros

`START_PRINT` takes `EXTRUDER_TEMP` / `BED_TEMP` and **defaults to PETG 240/80**, so a bare
call is always valid. It does: set both heaters → `G28` → `BED_MESH_PROFILE LOAD=default` →
wait for temps → prime line along the front edge → small retract.

`END_PRINT`: heaters off, fan off, retract 2 mm, Z+10, present the bed at Y220, motors off.

`PRINT_START` / `PRINT_END` are pass-through aliases so OrcaSlicer's generic-Klipper profile
works whichever naming it emits.

## Flashing

The board shipped with Marlin. Getting Klipper on it has two hard constraints:

1. The USB port is a **CH340 serial bridge**, so there is **no USB-DFU path**.
2. The stock **Creality 64 KiB bootloader** only accepts firmware from **microSD**, via a
   `/STM32F4_UPDATE/klipper.bin` file.

Build settings (from the sample's header, confirmed — these are the STM32F401 defaults):
STM32F401, **64 KiB bootloader offset (`0x8010000`)**, 8 MHz crystal, serial on **USART1
(PA10/PA9)**.

### SD card procedure

- Card must be **≤32 GB** (a 16 GB card worked; old Creality bootloaders choke on large/fast
  cards).
- Format **FAT32 with 4 KiB clusters** — the 32 KiB factory cluster size is a known
  compatibility failure.
- Write `klipper.bin` into `/STM32F4_UPDATE/`.
- Insert with the printer **off**, then **cold boot**. The bootloader only checks the card at
  power-on, never on hot-insert. It flashes in ~15–20 s and renames the file so it does not
  re-flash.
- The stock LCD going **blank/frozen afterwards is correct** — that is Klipper, which has no
  Creality screen firmware.

**The failure that cost a day:** the card was being inserted **upside down**. The Ender-5 S1's
mainboard slot is oriented counter-intuitively. The tell was the printer's own PRINT browser
showing no files; once seated correctly the `STM32F4_UPDATE` folder appeared there.

### Consequence

Flashing via SD left the **Creality bootloader in place**. Future MCU firmware updates —
which Mainsail will occasionally prompt for after a Klipper update — use **the same SD
method**. Keep that microSD with the printer.

A no-bootloader build (`0x8000000`) and `stm32flash` were staged as a USB fallback, requiring
the BOOT0 pad jumpered high at power-on. It was never needed and is not the current state.
