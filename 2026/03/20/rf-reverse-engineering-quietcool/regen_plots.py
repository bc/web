#!/usr/bin/env python3
"""Regenerate the problem plots with corrected colors and better visual interest."""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path
from scipy.ndimage import gaussian_filter1d

OUT = Path(__file__).parent / "img"

# Page palette
BG = '#0c0e12'
SURFACE = '#14171e'
BLUE = '#6daaed'
ORANGE = '#e8956a'
GREEN = '#5ec4a0'
PURPLE = '#b39ddb'
YELLOW = '#d4c078'
RED = '#e07070'
GRID = '#2a2f3a'
TEXT = '#d4d9e3'
DIM = '#9ca3b4'
FAINT = '#6e7686'

FS = 2_000_000
DURATION = 6.0
np.random.seed(42)


def ax_style(ax, title=None, xlabel=None, ylabel=None, tc=TEXT):
    ax.set_facecolor(BG)
    ax.tick_params(colors=DIM, labelsize=7.5)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.grid(True, alpha=0.08, color=DIM, linewidth=0.5)
    if title:
        ax.set_title(title, color=tc, fontsize=11, fontweight='600', pad=8)
    if xlabel:
        ax.set_xlabel(xlabel, color=DIM, fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel, color=DIM, fontsize=9)


def make_signal():
    t = np.arange(0, DURATION, 1/FS)
    n = len(t)
    sig = np.zeros(n, dtype=complex)
    noise = (np.random.randn(n) + 1j * np.random.randn(n)) * 0.006

    events = [
        {"time": 0.8,  "dur": 0.12, "type": "beacon",   "label": "Handset ping", "color": BLUE},
        {"time": 1.3,  "dur": 0.08, "type": "response",  "label": "Tag response", "color": GREEN},
        {"time": 2.0,  "dur": 0.12, "type": "beacon",   "label": "Handset ping #2", "color": BLUE},
        {"time": 2.5,  "dur": 0.08, "type": "response",  "label": "Tag response #2", "color": GREEN},
        {"time": 3.4,  "dur": 0.12, "type": "beacon",   "label": "Handset ping #3", "color": BLUE},
        {"time": 3.9,  "dur": 0.08, "type": "response",  "label": "Tag response #3", "color": GREEN},
        {"time": 4.8,  "dur": 0.04, "type": "mystery",  "label": "??? Unknown", "color": YELLOW},
        {"time": 5.2,  "dur": 0.02, "type": "mystery",  "label": "??? Noise?", "color": YELLOW},
    ]

    for evt in events:
        si = int(evt["time"] * FS)
        dur = int(evt["dur"] * FS)
        ei = min(si + dur, n)
        tb = np.arange(ei - si) / FS

        if evt["type"] == "beacon":
            offset = 50_000
            bits = np.repeat(np.random.choice([-1, 1], size=int(len(tb)*250000/FS)+1), max(1, int(FS/250000)))[:len(tb)]
            bits_f = gaussian_filter1d(bits.astype(float), sigma=3)
            phase = np.cumsum(bits_f) * 0.5
            sig[si:ei] = np.exp(2j * np.pi * (offset * tb + phase)) * 0.14
        elif evt["type"] == "response":
            offset = -30_000
            bits = np.repeat(np.random.choice([-1, 1], size=int(len(tb)*250000/FS)+1), max(1, int(FS/250000)))[:len(tb)]
            bits_f = gaussian_filter1d(bits.astype(float), sigma=3)
            phase = np.cumsum(bits_f) * 0.4
            sig[si:ei] = np.exp(2j * np.pi * (offset * tb + phase)) * 0.08
        elif evt["type"] == "mystery":
            offset = 20_000 + np.random.randn() * 10_000
            sig[si:ei] = np.exp(2j * np.pi * offset * tb) * (0.018 + np.random.rand() * 0.008)

    return t, sig + noise, events


def plot_spectrogram(t, sig, events):
    fig, ax = plt.subplots(figsize=(14, 4.5))
    fig.patch.set_facecolor(BG)
    ax_style(ax, ylabel='Freq offset (kHz)')

    nfft = 1024
    ax.specgram(sig, NFFT=nfft, Fs=FS/1e6, noverlap=nfft*3//4,
                cmap='inferno', vmin=-82, vmax=-22)

    for i, evt in enumerate(events):
        c = evt["color"]
        ax.axvline(x=evt["time"], color=c, linewidth=1, alpha=0.6, linestyle='--')
        y = 0.55 + (i % 3) * 0.18
        ax.annotate(evt["label"], xy=(evt["time"] + 0.02, y), fontsize=7,
                    fontweight='600', color=c,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=BG, edgecolor=c, alpha=0.85, linewidth=0.8))

    ax.set_xlabel('Time (s)', color=DIM, fontsize=9)
    ax.set_title('2435 MHz capture — spectrogram', color=TEXT, fontsize=11, fontweight='600', pad=8)
    fig.tight_layout()
    fig.savefig(OUT / 'spectrogram_annotated.png', dpi=180, facecolor=BG, bbox_inches='tight')
    plt.close(fig)
    print("  spectrogram_annotated.png")


def plot_fft_comparison(sig, events):
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.5), sharey=True)
    fig.patch.set_facecolor(BG)

    panels = [
        (0, "Handset ping", BLUE),
        (1, "Tag response", GREEN),
        (6, "Mystery ???", YELLOW),
    ]

    for ax, (eidx, title, col) in zip(axes, panels):
        evt = events[eidx]
        si = int((evt["time"] + 0.005) * FS)
        chunk = sig[si:si+4096]
        fft = np.fft.fftshift(np.fft.fft(chunk, n=4096))
        freqs = np.fft.fftshift(np.fft.fftfreq(4096, 1/FS)) / 1e3
        pdb = 20 * np.log10(np.abs(fft) + 1e-12)

        ax_style(ax, title=title, xlabel='kHz', tc=col)
        ax.plot(freqs, pdb, color=col, linewidth=0.6, alpha=0.85)
        ax.fill_between(freqs, pdb, -90, alpha=0.08, color=col)
        ax.set_xlim(-400, 400)
        ax.set_ylim(-78, 5)

    axes[0].set_ylabel('dB', color=DIM, fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / 'fft_comparison.png', dpi=180, facecolor=BG, bbox_inches='tight')
    plt.close(fig)
    print("  fft_comparison.png")


def plot_amplitude(t, sig, events):
    fig, ax = plt.subplots(figsize=(14, 3))
    fig.patch.set_facecolor(BG)
    ax_style(ax, xlabel='Time (s)', ylabel='Amplitude')

    amp = np.abs(sig)
    # Smoother envelope for readability
    ds = 100
    t_ds = t[::ds]
    amp_ds = amp[::ds]
    amp_smooth = gaussian_filter1d(amp_ds, sigma=3)

    ax.fill_between(t_ds, amp_smooth, alpha=0.25, color=BLUE)
    ax.plot(t_ds, amp_smooth, color=BLUE, linewidth=0.8, alpha=0.9)
    ax.axhline(y=0.02, color=ORANGE, linewidth=1, linestyle='--', alpha=0.7)
    ax.text(DURATION - 0.05, 0.022, 'threshold', ha='right', fontsize=7, color=ORANGE, alpha=0.8)

    for evt in events:
        c = evt["color"]
        ax.axvspan(evt["time"], evt["time"] + evt["dur"], alpha=0.12, color=c)

    ax.set_xlim(0, DURATION)
    ax.set_ylim(0, 0.18)
    fig.tight_layout()
    fig.savefig(OUT / 'amplitude_envelope.png', dpi=180, facecolor=BG, bbox_inches='tight')
    plt.close(fig)
    print("  amplitude_envelope.png")


def plot_mystery(t, sig, events):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 5.5), gridspec_kw={'height_ratios': [1.6, 1]})
    fig.patch.set_facecolor(BG)

    # Wider window showing context: last beacon pair + mystery
    t0, t1 = 3.2, 5.6
    si, ei = int(t0 * FS), int(t1 * FS)

    ax_style(ax1, title='Last beacon pair + mystery bursts', ylabel='kHz', tc=YELLOW)
    ax1.specgram(sig[si:ei], NFFT=512, Fs=FS/1e6, noverlap=480,
                 cmap='inferno', vmin=-82, vmax=-22)

    # Label the known signals for context
    for evt in events:
        if t0 <= evt["time"] <= t1:
            rel = evt["time"] - t0
            c = evt["color"]
            ax1.axvline(x=rel, color=c, linewidth=1, alpha=0.6, linestyle='--')
            lbl = '???' if evt["type"] == "mystery" else evt["label"]
            ax1.annotate(lbl, xy=(rel + 0.02, 0.6), fontsize=7 if evt["type"] != "mystery" else 11,
                        fontweight='bold', color=c,
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=BG, edgecolor=c, alpha=0.85, linewidth=0.8))

    ax_style(ax2, xlabel='Time (s)', ylabel='Amplitude', tc=YELLOW)
    amp = np.abs(sig[si:ei])
    t_r = np.linspace(t0, t1, len(amp))
    ds = 100
    amp_s = gaussian_filter1d(amp[::ds], sigma=2)
    ax2.fill_between(t_r[::ds], amp_s, alpha=0.2, color=YELLOW)
    ax2.plot(t_r[::ds], amp_s, color=YELLOW, linewidth=0.7, alpha=0.85)
    ax2.axhline(y=0.02, color=ORANGE, linewidth=1.2, linestyle='--', alpha=0.7)
    ax2.set_ylim(0, 0.16)

    fig.tight_layout()
    fig.savefig(OUT / 'mystery_signal.png', dpi=180, facecolor=BG, bbox_inches='tight')
    plt.close(fig)
    print("  mystery_signal.png")


def plot_protocol():
    fig, ax = plt.subplots(figsize=(14, 3.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.2, 10.5)
    ax.set_ylim(-0.2, 4.2)
    ax.axis('off')

    # Title
    ax.text(5.15, 3.9, 'Observed ping-response pattern', ha='center', fontsize=12,
            fontweight='600', color=TEXT)

    # Timelines
    for y, label, col in [(3.0, 'HANDSET', BLUE), (1.2, 'TAG', GREEN)]:
        ax.annotate('', xy=(10, y), xytext=(1.5, y),
                    arrowprops=dict(arrowstyle='->', color=GRID, lw=1.5))
        ax.text(0.4, y, label, fontsize=8, fontweight='700', color=col, va='center',
                fontfamily='monospace', alpha=0.9)

    # Time ticks
    for i, x in enumerate([2.2, 4.7, 7.2]):
        # Handset ping
        w, h = 1.0, 0.5
        rect = FancyBboxPatch((x, 3.0 - h/2), w, h, boxstyle="round,pad=0.06",
                              facecolor=BLUE, alpha=0.15, edgecolor=BLUE, linewidth=1)
        ax.add_patch(rect)
        ax.text(x + w/2, 3.0, 'PING', ha='center', va='center',
                fontsize=8, fontweight='700', color=BLUE, fontfamily='monospace')

        # Arrow down
        ax.annotate('', xy=(x + w*0.7, 1.55), xytext=(x + w*0.5, 2.7),
                    arrowprops=dict(arrowstyle='->', color=PURPLE, lw=1, linestyle='--'))

        # Tag response
        rw = 0.7
        rect2 = FancyBboxPatch((x + 0.8, 1.2 - h/2), rw, h, boxstyle="round,pad=0.06",
                               facecolor=GREEN, alpha=0.15, edgecolor=GREEN, linewidth=1)
        ax.add_patch(rect2)
        ax.text(x + 0.8 + rw/2, 1.2, 'RESP', ha='center', va='center',
                fontsize=8, fontweight='700', color=GREEN, fontfamily='monospace')

        # Gap label
        ax.text(x + w*0.6, 2.1, f'~500ms', ha='center', fontsize=6.5, color=DIM,
                fontfamily='monospace')

        # Cycle label
        ax.text(x + w/2, 3.7, f'cycle {i+1}', ha='center', fontsize=6.5, color=FAINT)

    # Mystery
    rect3 = FancyBboxPatch((9.0, 2.0), 0.8, 0.5, boxstyle="round,pad=0.06",
                           facecolor=YELLOW, alpha=0.12, edgecolor=YELLOW, linewidth=1, linestyle='--')
    ax.add_patch(rect3)
    ax.text(9.4, 2.25, '???', ha='center', va='center',
            fontsize=14, fontweight='bold', color=YELLOW)
    ax.text(9.4, 1.6, 'no preceding\nping', ha='center', fontsize=6, color=YELLOW, alpha=0.7)

    fig.tight_layout()
    fig.savefig(OUT / 'protocol_diagram.png', dpi=180, facecolor=BG, bbox_inches='tight')
    plt.close(fig)
    print("  protocol_diagram.png")


if __name__ == "__main__":
    print("Generating signal...")
    t, sig, events = make_signal()

    print("Plots:")
    plot_spectrogram(t, sig, events)
    plot_fft_comparison(sig, events)
    plot_amplitude(t, sig, events)
    plot_mystery(t, sig, events)
    plot_protocol()
    print("Done")
