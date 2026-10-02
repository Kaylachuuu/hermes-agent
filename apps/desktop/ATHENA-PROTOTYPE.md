# Remote agent, local Desktop prototype

Experimental implementation for a stock remote Hermes backend with client-local
terminal/filesystem, browser, and native PC capabilities. The standalone backend
plugin is https://github.com/Kaylachuuu/hermes-desktop-bridge.

The client source is based on upstream `10c6188de188871f64a88dd95bc6b262adb0c307`.
This is a review prototype, not a production-ready permission boundary.

## Boundaries

The backend retains conversations, configuration, identity, and memory. An
external TerminalEnvironmentProvider and execution middleware route ordinary
terminal/file calls through the existing server-request transport. Native
execution remains in Electron; renderer forwarding does not expose general Node
access to UI plugins. No additional inbound execution service is opened.

PC/browser inspection and actions have native approval prompts and optional
conversation grants. Cross-device terminal requests require destination
enrollment and origin-side approval. Ed25519 receipts bind the destination,
enrollment, chat and exact command; expiry, tampering and replay are refused.
Device registrations are currently exclusive origin/target roles. Bidirectional
registration changes are unfinished and are not included in this snapshot.

## Validation as of 2026-10-02

- Latest-upstream renderer and native TypeScript checks passed.
- Latest-upstream Windows build and ARM64 Linux build/package checks passed.
- Focused remote IPC, Settings, login, signature, browser-policy and driver tests
  passed; standalone plugin regression suite: 51 tests passed against the stock
  remote backend revision used by the prototype.
- Earlier client revisions passed live Windows, Linux and Intel Mac terminal/file
  checks, Firefox isolated browsing on all three, and Chromium/Edge checks on
  Windows/Linux. These live results do not replace acceptance of updated builds.
- Raspberry Pi 5 ARM64: first prototype connected to the canonical gateway and
  executed normal terminal calls on the Pi. Updated client passed Unicode file
  roundtrip and Firefox prepare/navigate/read/click through Example Domain to IANA.
- Linux Wayland window discovery/accessibility worked, but exact-window capture
  remained unproven. General Linux PC input is not claimed verified.
- Safari isolated adapter is experimental source only; live Mac acceptance and
  access to existing signed-in Safari windows are unfinished.

## Remaining work before upstream adoption

Execution-specific negotiation, native authorization of the ordinary terminal
bridge, request deduplication, process-tree cancellation, streaming/bounded
transfer semantics, and ownership races still need production review. Prototype
launch environment options should become supported locally scoped settings.
Chrome/Firefox custom app-path settings and registered-device bidirectional
control are not complete. Firefox Sync has not been verified.

Use a separate prototype user-data directory. Do not replace a user's canonical
backend files or disable Electron's sandbox to launch an unpacked Linux build.

## October 2 morning checkpoint

New Desktop chats receive plugin-owned guidance distinguishing ordinary terminal/file
access on the conversation-owning device from cross-device tools. The former needs
no destination ID; the latter requires target_device and command. List enrolled IDs
with desktop_devices and {"action":"list"}. Existing chats retain their saved
system prompts. All 51 regression checks passed against the stock backend.

Scopuli live checks confirmed hostname/OS/cwd, reading local project source and
creating directories. Quote paths containing spaces; the reported mkdir failure was
resolved by shell quoting without a bridge code change.

Normal per-user application launchers were installed on Scopuli, Intel Mac and
Raspberry Pi, with profile backups and correct gateway history confirmed on all
three. Windows shortcuts supply the working profile/private driver to its installed
client. The Mac Applications launcher opens the unchanged client in Application
Support with its working profile and driver. The Pi menu entry uses the existing
profile-aware launcher and AppArmor-approved executable path; sandboxing remains
on. Old Windows test builds were archived and original backend data preserved.
These installations do not constitute published production installers. Windows/Mac
retained their tested builds; Pi uses the updated upstream build.
