---
layout: default
title: "Reverse Engineering the TabCat V2 RF Protocol"
description: "Investigating the 2.4 GHz RF protocol of the TabCat V2 pet tracker."
date: 2026-03-20
---

# Reverse Engineering the TabCat V2 RF Protocol

<p class="post-meta"><time>March 20, 2026</time></p>

<figure>
<img src="/assets/posts/rf-reverse-engineering-quietcool/cat_kit_beacon.jpeg" alt="Kit the cat wearing her TabCat tracking beacon" style="border-radius: 8px; max-height: 420px; width: 100%; object-fit: cover;">
<figcaption>Kit with her TabCat beacon. Unbothered.</figcaption>
</figure>

My cat Kit roams outside. After losing her one too many times, I bought a [TabCat V2](https://us.tabcat.com/products/cat-tracker-tabcat-v2). It’s a small RF tag on her collar and a handheld unit that beeps louder as you get closer. Naturally, I had to open it to see how it works.

## FCC Filings

The FCC documents (Handset: [TUW-PH](https://fcc.report/FCC-ID/TUW-PH), Tag: [TUW-BT](https://fcc.report/FCC-ID/TUW-BT)) show both devices operate at 2435 MHz. Since it's not Wi-Fi or Bluetooth, the FCC classifies it as "low power transmitters using spread spectrum techniques." This points toward OQPSK DSSS or frequency-hopping rather than simple narrowband FSK.

## PCB & The Chip

The board is tiny. The main IC is marked `G22 C224HG`. Based on the specs and FCC data, this is almost certainly a Silicon Labs EFR32FG22 Series 2 chip. 

This hardware makes sense for the application. The EFR32FG22 handles proprietary wireless protocols, supporting GFSK up to 2 Mbps and OQPSK DSSS at 250 kbps. It has no standard BLE or Zigbee stack, meaning Loc8tor runs a custom protocol on Silicon Labs' RAIL API. 

*(Note: I can't find the exact "C224HG" string in any SiLabs ordering guides. Let me know if you know how to read their package markings.)*

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin: 1.5rem 0;">
<img src="/assets/posts/rf-reverse-engineering-quietcool/pcb_overview.jpeg" style="border-radius: 6px; width: 100%; aspect-ratio: 1; object-fit: cover;">
<img src="/assets/posts/rf-reverse-engineering-quietcool/chip_detail.jpeg" style="border-radius: 6px; width: 100%; aspect-ratio: 1; object-fit: cover;">
<img src="/assets/posts/rf-reverse-engineering-quietcool/chip_closeup.jpg" style="border-radius: 6px; width: 100%; aspect-ratio: 1; object-fit: cover;">
</div>

## RF Capture

I used a wideband SDR to capture 2 MHz of bandwidth centered on 2435 MHz. Looking at the spectrogram, the protocol is highly regular. The handset sends a 120ms ping, the tag replies with a quieter 80ms burst, and they wait 500-700ms before repeating.

<figure>
<img src="/assets/posts/rf-reverse-engineering-quietcool/spectrogram_annotated.png" alt="Annotated spectrogram" style="border-radius: 6px;">
<figcaption>Blue = handset pings. Green = tag responses. Yellow = mystery signals.</figcaption>
</figure>

I wrote a Python script to isolate these bursts, shift them to baseband, and apply FM demodulation to extract the bits. I'm stuck here for now. Without knowing the exact bit rate or packet framing (preamble, sync word, CRC), I can't read the payload yet.

## The Mystery Signals

At the end of my capture, two faint 20-40ms blips showed up right at the noise floor. They look entirely different from the main pings. The EFR32FG22 has an RFSense wake-up mode, so the tag might send low-power heartbeats before the main sequence starts. Or it’s just random 2.4 GHz interference.

## Next Steps

Custom 2.4 GHz protocols are tough. Unlike 433 MHz where tools like `rtl_433` usually work out of the box, unknown GFSK needs a lot of manual decoding.

Next up: getting a directional antenna, setting up a GNU Radio flowgraph, and digging into the RAIL SDK docs. If you have experience with EFR32 chips or Loc8tor hardware, get in touch on [GitHub](https://github.com/bc) or [LinkedIn](https://www.linkedin.com/in/cohn/).