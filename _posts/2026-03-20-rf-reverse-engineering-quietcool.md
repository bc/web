---
layout: default
title: "Reverse Engineering the TabCat V2 Cat Tracker RF Protocol"
description: "Investigating the 2.4 GHz RF protocol of the TabCat V2 pet tracker using SDR, FCC filings, and PCB teardown."
date: 2026-03-20
excerpt: "FCC filing deep dive, PCB teardown, and SDR signal capture of a 2.4 GHz proprietary cat tracking beacon. Silicon Labs EFR32FG22 chip identification, GFSK demodulation, and some mystery signals I still can't explain."
---

# Reverse Engineering the TabCat V2 Cat Tracker RF Protocol

<p class="post-meta"><time>March 20, 2026</time></p>

<div style="position: relative; padding-bottom: 34.5%; height: 0; overflow: hidden; border-radius: 8px; margin: 1rem 0;">
<video autoplay loop muted playsinline preload="auto" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; background: #0c0e12; border-radius: 8px;">
<source src="/assets/posts/rf-reverse-engineering-quietcool/spectrum_animation.mp4" type="video/mp4">
</video>
</div>

<figure>
<img src="/assets/posts/rf-reverse-engineering-quietcool/cat_kit_beacon.jpeg" alt="Kit the cat wearing her TabCat tracking beacon" style="border-radius: 8px; max-height: 420px; width: 100%; object-fit: cover;">
<figcaption>Kit with her TabCat beacon. Unbothered.</figcaption>
</figure>

## Why

My cat Kit goes outside. After a few too many evenings of not knowing where she was, I got a [TabCat V2](https://us.tabcat.com/products/cat-tracker-tabcat-v2) — a little RF tag on her collar and a handheld unit that beeps louder as you get closer. It actually works.

Of course I had to open it. What frequency? What protocol? What chip? Could I build my own receiver? Here's how far I got.

## FCC Filings

Every wireless device in the US needs an FCC ID. The TabCat has two:

| Component | FCC ID | Frequency | Granted |
|-----------|--------|-----------|---------|
| Handset | [TUW-PH](https://fcc.report/FCC-ID/TUW-PH) | 2435.0 MHz | 2022-07-20 |
| Tag | [TUW-BT](https://fcc.report/FCC-ID/TUW-BT) | 2435.0 MHz | 2022-07-21 |

> **2435 MHz, proprietary spread spectrum**
>
> **2435 MHz** — smack in the 2.4 GHz ISM band, but not Bluetooth, not Zigbee, not WiFi. The FCC classifies it as "low power transmitters using spread spectrum techniques" (Part 15C, scope A4). That's a useful clue — it means the modulation is probably OQPSK DSSS or frequency-hopping, not simple narrowband FSK. Made by **Loc8tor Ltd** in London, tested by UL International UK.

The interesting documents (block diagram, schematics, BOM, operational description) are all marked confidential. So the FCC gives us frequency and the modulation family, but nothing about the actual protocol. Time to open it up.

[Full FCC filing](https://fcc.report/FCC-ID/TUW-BT)

## PCB Teardown

The PCB is tiny — thumbnail-sized. One main IC, a crystal, some antenna pads, and battery contacts.

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin: 1.5rem 0;">
<figure style="margin: 0; text-align: center;">
<img src="/assets/posts/rf-reverse-engineering-quietcool/pcb_overview.jpeg" alt="Full PCB" style="border-radius: 6px; width: 100%; aspect-ratio: 1; object-fit: cover;">
<figcaption style="font-size: 0.85em; color: #666;">Full board</figcaption>
</figure>
<figure style="margin: 0; text-align: center;">
<img src="/assets/posts/rf-reverse-engineering-quietcool/chip_detail.jpeg" alt="IC and crystal" style="border-radius: 6px; width: 100%; aspect-ratio: 1; object-fit: cover;">
<figcaption style="font-size: 0.85em; color: #666;">IC + crystal</figcaption>
</figure>
<figure style="margin: 0; text-align: center;">
<img src="/assets/posts/rf-reverse-engineering-quietcool/chip_closeup.jpg" alt="Chip markings" style="border-radius: 6px; width: 100%; aspect-ratio: 1; object-fit: cover;">
<figcaption style="font-size: 0.85em; color: #666;">Chip markings</figcaption>
</figure>
</div>

### The Chip

The IC markings:

```
G22
C224HG
C01K92
2132
```

I think this is a **Silicon Labs EFR32FG22C224** — the proprietary-wireless variant of their Wireless Gecko Series 2 line. The reasoning:

- **G22** — the xG22 family (EFR32*x*G22)
- **C224** — ordering code for the 2.4 GHz radio config
- **2132** — date code, week 32 of 2021
- **C01K92** — lot/trace code

> **Does the chip match the signal? Yes.**
>
> I checked the [EFR32FG22 specs](https://www.silabs.com/wireless/proprietary/efr32fg22-series-2-2-4-ghz-socs). It supports exactly what we'd expect given the FCC filing and the signals we captured:
>
> - **GFSK** up to 2 Mbps — matches the wider-bandwidth beacon pings
> - **OQPSK DSSS** at 250 kbps, -102.3 dBm sensitivity — this is the "spread spectrum" from the FCC classification, and DSSS would enable the direction-finding (precise time-of-arrival)
> - **RFSense with selective OOK** — ultra-low-power wake-up mode. The mystery bursts at the end of my capture might be this
>
> The FG22 is specifically a proprietary-only part — no BLE or Zigbee stack, just custom firmware on Silicon Labs' [RAIL](https://www.silabs.com/developers/rail-radio-abstraction-interface-layer-sdk) API. Cortex-M33, 512 KB flash, QFN32 (4x4 mm), +6 dBm TX, 1.8-3.8V.

One thing I want to flag: **I can't find "C224HG" in any Silicon Labs documentation.** The "HG" is probably an abbreviated flash/RAM/package designator that they print on the chip but don't put in public ordering guides. Searching the full marking string online gives nothing. If you know how to read SiLabs package markings, please get in touch.

## RF Capture

Now that I know the frequency (2435 MHz), I set up an SDR capture. A normal RTL-SDR maxes out around 1.7 GHz, so you need a HackRF, a downconverter, or something else that covers 2.4 GHz. I used a wideband SDR at 2 MHz sample rate centered on 2435 MHz.

```python
# Parameters from FCC filing TUW-BT
CENTER_FREQ = 2_435_000_000   # 2435 MHz
SAMPLE_RATE = 2_000_000       # 2 MHz BW
GAIN        = 40

sdr.sample_rate = SAMPLE_RATE
sdr.center_freq = CENTER_FREQ
sdr.gain = GAIN

samples = sdr.read_samples(1024)
amplitude = np.abs(samples)

if np.max(amplitude) > THRESHOLD:
    log_burst(timestamp, amplitude)
```

### Spectrogram

You can see the protocol immediately. The handset sends a **beacon ping**, the tag responds with a **shorter, weaker burst**, then there's a gap of about 500-700ms before the next pair. Clean and regular — until the end.

<figure>
<img src="/assets/posts/rf-reverse-engineering-quietcool/spectrogram_annotated.png" alt="Annotated spectrogram" style="border-radius: 6px;">
<figcaption>Blue = handset pings. Green = tag responses. Yellow = the mystery signals at the end.</figcaption>
</figure>

### FFT Comparison

Looking at the frequency content of each signal type, you can see three distinct signatures. The handset ping is wider and louder, the tag response is narrower and quieter, and the mystery signals are barely distinguishable from the noise floor:

<figure>
<img src="/assets/posts/rf-reverse-engineering-quietcool/fft_comparison.png" alt="FFT comparison" style="border-radius: 6px;">
<figcaption>Handset ping (left), tag response (center), mystery signal (right).</figcaption>
</figure>

### Amplitude Over Time

<figure>
<img src="/assets/posts/rf-reverse-engineering-quietcool/amplitude_envelope.png" alt="Signal amplitude envelope" style="border-radius: 6px;">
<figcaption>The threshold cleanly separates real bursts from noise — except for those last two blips.</figcaption>
</figure>

### Protocol Pattern

<figure>
<img src="/assets/posts/rf-reverse-engineering-quietcool/protocol_diagram.png" alt="Protocol diagram" style="border-radius: 6px;">
<figcaption>Ping, response, gap, repeat. Three clean pairs, then something shows up without a corresponding ping.</figcaption>
</figure>

## Spectrum Animation

Full capture played back at 60fps. Left is the spectrogram waterfall, right is the FFT at each moment. You can see the signal bursts light up both views simultaneously:

<div style="position: relative; padding-bottom: 34.5%; height: 0; overflow: hidden; border-radius: 8px; margin: 1rem 0;">
<video controls loop muted playsinline preload="metadata" poster="/assets/posts/rf-reverse-engineering-quietcool/spectrogram_annotated.png" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; background: #000;">
<source src="/assets/posts/rf-reverse-engineering-quietcool/spectrum_animation.mp4" type="video/mp4">
</video>
</div>

*Spectrogram waterfall + live FFT, 60fps. Full capture is 6 seconds.*

### Timing

Some numbers to give a sense of scale. Each handset beacon ping lasts about **120ms**. The tag response is shorter — around **80ms**. Between each ping-response pair there's a gap of roughly **500-700ms** where neither device transmits. The mystery bursts at the end are much shorter, maybe **20-40ms** each.

At the sample level, each FFT window covers **256&micro;s** (512 samples at 2 MHz). So a single 120ms beacon ping contains about **470 FFT frames** — plenty of data to work with if you want to look at how the signal evolves within a single transmission.

### From Spectrogram to Bits

Getting from "I can see a signal on the spectrogram" to "I can read the actual data" is a few steps. The FG22 supports GFSK, where information is encoded as small frequency shifts around the carrier. To extract bits:

1. **Isolate the burst.** Use the amplitude envelope to find where the signal starts and stops. Threshold the IQ magnitude, grab that window.
2. **Shift to baseband.** Multiply by a complex exponential at the carrier offset to center the signal at 0 Hz. For the handset ping, that's about +50 kHz from our SDR center.
3. **FM demodulate.** GFSK is a form of FM. Take the instantaneous frequency: `freq = diff(angle(iq)) * fs / (2*pi)`. Positive frequency deviation = 1, negative = 0.
4. **Clock recovery.** Find the bit rate by looking at the shortest symbol transitions. At 250 kbps (which the FG22 supports for OQPSK DSSS), each bit is **4&micro;s**. At 1 Mbps GFSK, each bit is **1&micro;s**.
5. **Sample at bit centers.** Once you know the clock, sample the demodulated frequency at each bit midpoint to get the bitstream.

```python
# Step 2-3: shift to baseband and FM-demodulate
carrier_offset = 50_000  # Hz, estimated from FFT peak
t_burst = np.arange(len(burst)) / SAMPLE_RATE
baseband = burst * np.exp(-2j * np.pi * carrier_offset * t_burst)

# FM demod: instantaneous frequency from phase derivative
phase = np.angle(baseband)
freq = np.diff(np.unwrap(phase)) * SAMPLE_RATE / (2 * np.pi)

# Step 4: bits are where freq is above/below zero
bits_raw = (freq > 0).astype(int)

# Step 5: resample at bit rate (e.g. 250 kbps = 4us/bit)
bit_period = int(SAMPLE_RATE / 250_000)  # 8 samples per bit
bit_centers = np.arange(bit_period // 2, len(bits_raw), bit_period)
bits = bits_raw[bit_centers]
```

I haven't actually gotten clean bits out of this yet — I don't know the exact bit rate, and without knowing the packet framing (preamble, sync word, CRC) it's hard to tell where valid data starts and ends. This is where the RAIL SDK docs might help, since Silicon Labs has standard packet formats that the FG22 firmware likely uses.

## Where I Got Stuck

<figure>
<img src="/assets/posts/rf-reverse-engineering-quietcool/mystery_signal.png" alt="Mystery signals" style="border-radius: 6px;">
<figcaption>Last beacon pair plus the two mystery bursts. The context helps you see how different they are.</figcaption>
</figure>

> **These two blips at the end**
>
> Around t=4.8s and t=5.2s, two faint bursts show up. They're right at the noise floor and look different from everything else:
>
> - Way shorter (20-40ms vs 80-120ms for real signals)
> - Barely above the detection threshold
> - Different frequency offset
> - No handset ping before them
>
> One thought: the EFR32FG22 has an **RFSense OOK wake-up** mode. The tag might send low-power heartbeat beacons so the handset knows it's nearby before starting the full ping-response sequence. Short and quiet would fit.
>
> Or it's just 2.4 GHz interference. WiFi, Bluetooth, somebody's microwave. I tried correlating with button presses and distance changes and couldn't find a pattern.

## Dead Ends

Nobody else seems to have looked at the TabCat protocol. No open-source firmware, no write-ups, nothing. Loc8tor runs a custom stack on RAIL, which makes sense for direction-finding — you'd need custom signal processing (RSSI gradients, maybe phase-difference) that doesn't fit in a BLE or Zigbee framework.

The chip marking `C224HG` is also a dead end. I'm fairly sure about the chip family but can't pin down the exact variant.

## Takeaways

1. **FCC filings tell you a lot.** Even with confidential docs, you get frequency and modulation family. "Spread spectrum" pointed me at DSSS before I captured anything.
2. **Chip + filing + capture all agree.** The FG22 does GFSK and OQPSK DSSS at 2.4 GHz. That matches the FCC classification and the spectral shapes. When all three line up, you can be confident.
3. **2.4 GHz proprietary is hard.** 433 MHz OOK — `rtl_433` handles that on the first try. Custom GFSK at 2.4 GHz with unknown framing is a different problem.
4. **2.4 GHz is loud.** Separating a weak proprietary signal from WiFi/BLE/everything else is hard without a directional antenna or shielded setup.

## What's Next

- **Directional antenna** aimed at the tag
- **GNU Radio** GFSK demodulator at 2435 MHz
- Look for **DSSS spreading codes** in raw IQ
- Captures at different **distances**
- Dig into **RAIL SDK docs**

---

> **If you know something I don't**
>
> I'd like to hear from anyone who's worked with EFR32 chip IDs, proprietary 2.4 GHz stuff, or TabCat/Loc8tor products:
>
> - Does `C224HG` map to a known FG22 variant?
> - Could the mystery bursts be RFSense wake-up packets?
> - Best tool for demodulating unknown GFSK at 2.4 GHz?
>
> [GitHub](https://github.com/bc) / [LinkedIn](https://www.linkedin.com/in/cohn/)

---

## Links

| Resource | Link |
|----------|------|
| TabCat V2 | [us.tabcat.com](https://us.tabcat.com/products/cat-tracker-tabcat-v2) |
| FCC (tag) | [TUW-BT](https://fcc.report/FCC-ID/TUW-BT) |
| FCC (handset) | [TUW-PH](https://fcc.report/FCC-ID/TUW-PH) |
| EFR32FG22 | [silabs.com](https://www.silabs.com/wireless/proprietary/efr32fg22-series-2-2-4-ghz-socs) |
| Datasheet | [PDF](https://www.silabs.com/documents/public/data-sheets/efr32fg22-datasheet.pdf) |
| Code | [GitHub](https://github.com/bc/embedded_hardware_agent_development/tree/main/quietcool) |
