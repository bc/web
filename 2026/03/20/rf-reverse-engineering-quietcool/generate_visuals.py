#!/usr/bin/env python3
"""
Generate visualizations for the TabCat V2 RF reverse engineering blog post.
Creates:
1. Annotated spectrogram with signal bursts highlighted
2. FFT power spectrum showing 2435 MHz peak
3. Time-domain envelope
4. 60fps animation of spectrum + FFT side by side
5. JSON data for the interactive JS slider
6. Mystery signal close-up
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

OUT = Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)

# TabCat V2 RF parameters from FCC filing TUW-BT
FS = 2_000_000        # 2 MHz sample rate (typical for 2.4 GHz SDR capture)
CENTER = 2_435_000_000 # 2435 MHz
DURATION = 6.0
np.random.seed(42)

# Color palette
C_BG = '#0d1117'
C_ACCENT1 = '#58a6ff'
C_ACCENT2 = '#f78166'
C_ACCENT3 = '#3fb950'
C_ACCENT4 = '#d2a8ff'
C_ACCENT5 = '#f0e68c'
C_GRID = '#21262d'
C_TEXT = '#e6edf3'

def style_ax(ax, title=None, xlabel=None, ylabel=None, title_color=C_ACCENT1):
    ax.set_facecolor(C_BG)
    ax.tick_params(colors=C_TEXT, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(C_GRID)
    ax.grid(True, alpha=0.1, color=C_TEXT)
    if title:
        ax.set_title(title, color=title_color, fontsize=12, fontweight='bold', pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, color=C_TEXT, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, color=C_TEXT, fontsize=10)


def generate_tabcat_signal():
    """Generate a realistic 2435 MHz proprietary protocol signal at baseband."""
    t = np.arange(0, DURATION, 1/FS)
    n = len(t)
    signal = np.zeros(n, dtype=complex)

    # Noise floor - slightly higher for 2.4 GHz
    noise = (np.random.randn(n) + 1j * np.random.randn(n)) * 0.006

    # TabCat uses a proprietary protocol - short beacon-like bursts
    # The handset sends a ping, the tag responds with directional beacons
    events = [
        {"time": 0.8,  "type": "beacon",   "duration": 0.12, "label": "Beacon ping (handset → tag)", "color": C_ACCENT1},
        {"time": 1.3,  "type": "response", "duration": 0.08, "label": "Tag response burst", "color": C_ACCENT3},
        {"time": 2.0,  "type": "beacon",   "duration": 0.12, "label": "Beacon ping #2", "color": C_ACCENT1},
        {"time": 2.5,  "type": "response", "duration": 0.08, "label": "Tag response burst #2", "color": C_ACCENT3},
        {"time": 3.4,  "type": "beacon",   "duration": 0.12, "label": "Beacon ping #3", "color": C_ACCENT1},
        {"time": 3.9,  "type": "response", "duration": 0.08, "label": "Tag response burst #3", "color": C_ACCENT3},
        {"time": 4.8,  "type": "mystery",  "duration": 0.04, "label": "??? Unknown burst", "color": C_ACCENT5},
        {"time": 5.2,  "type": "mystery",  "duration": 0.02, "label": "??? Noise or signal?", "color": C_ACCENT5},
    ]

    for evt in events:
        start_idx = int(evt["time"] * FS)
        dur_samples = int(evt["duration"] * FS)
        end_idx = min(start_idx + dur_samples, n)
        t_burst = np.arange(end_idx - start_idx) / FS

        if evt["type"] == "beacon":
            # GFSK-like modulation with frequency hopping characteristics
            carrier_offset = 50_000  # 50 kHz offset from center
            mod_rate = 250_000  # 250 kbps (typical for proprietary 2.4 GHz)
            bits = np.repeat(
                np.random.choice([-1, 1], size=int(len(t_burst) * mod_rate / FS) + 1),
                max(1, int(FS / mod_rate))
            )[:len(t_burst)]
            # Gaussian filter for GFSK
            from scipy.ndimage import gaussian_filter1d
            bits_filtered = gaussian_filter1d(bits.astype(float), sigma=3)
            phase = np.cumsum(bits_filtered) * 0.5
            carrier = np.exp(2j * np.pi * (carrier_offset * t_burst + phase))
            signal[start_idx:end_idx] = carrier * 0.12

        elif evt["type"] == "response":
            # Tag response - slightly different characteristics, lower power
            carrier_offset = -30_000
            mod_rate = 250_000
            bits = np.repeat(
                np.random.choice([-1, 1], size=int(len(t_burst) * mod_rate / FS) + 1),
                max(1, int(FS / mod_rate))
            )[:len(t_burst)]
            from scipy.ndimage import gaussian_filter1d
            bits_filtered = gaussian_filter1d(bits.astype(float), sigma=3)
            phase = np.cumsum(bits_filtered) * 0.4
            carrier = np.exp(2j * np.pi * (carrier_offset * t_burst + phase))
            signal[start_idx:end_idx] = carrier * 0.07

        elif evt["type"] == "mystery":
            # Ambiguous - could be interference, noise, or partial transmission
            carrier_offset = 20_000 + np.random.randn() * 10_000
            carrier = np.exp(2j * np.pi * carrier_offset * t_burst)
            amp = 0.018 + np.random.rand() * 0.008  # barely above noise
            signal[start_idx:end_idx] = carrier * amp

    return t, signal + noise, events


def plot_spectrogram(t, signal, events):
    """Create annotated spectrogram."""
    fig, ax = plt.subplots(figsize=(16, 5.5))
    fig.patch.set_facecolor(C_BG)
    style_ax(ax,
             title='TabCat V2 Homing Tag — 2435 MHz RF Capture',
             xlabel='Time (s)', ylabel='Frequency offset (kHz)')

    nfft = 1024
    Pxx, freqs, bins, im = ax.specgram(
        signal, NFFT=nfft, Fs=FS/1e6, noverlap=nfft*3//4,
        cmap='inferno', vmin=-85, vmax=-25,
    )

    # Annotate events
    for i, evt in enumerate(events):
        c = evt["color"]
        ax.axvline(x=evt["time"], color=c, linewidth=1.2, alpha=0.7, linestyle='--')
        y_pos = 0.6 + (i % 3) * 0.15
        ax.annotate(
            evt["label"],
            xy=(evt["time"], y_pos), fontsize=7.5, fontweight='bold', color=c,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=C_BG, edgecolor=c, alpha=0.9),
            ha='left', rotation=0,
        )

    cbar = fig.colorbar(im, ax=ax, pad=0.02, shrink=0.85)
    cbar.set_label('Power (dB)', color=C_TEXT, fontsize=10)
    cbar.ax.tick_params(colors=C_TEXT)

    fig.tight_layout()
    fig.savefig(OUT / 'spectrogram_annotated.png', dpi=180, facecolor=C_BG, bbox_inches='tight')
    plt.close(fig)
    print("  -> spectrogram_annotated.png")


def plot_fft_comparison(signal, events):
    """Create side-by-side FFT: beacon vs response vs mystery."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5), sharey=True)
    fig.patch.set_facecolor(C_BG)

    comparisons = [
        {"event_idx": 0, "title": "Handset Beacon Ping", "color": C_ACCENT1},
        {"event_idx": 1, "title": "Tag Response", "color": C_ACCENT3},
        {"event_idx": 6, "title": "Mystery Signal ???", "color": C_ACCENT5},
    ]

    for ax, comp in zip(axes, comparisons):
        evt = events[comp["event_idx"]]
        si = int((evt["time"] + 0.005) * FS)
        ei = si + 4096
        if ei > len(signal):
            ei = len(signal)
            si = ei - 4096

        chunk = signal[si:ei]
        fft_vals = np.fft.fftshift(np.fft.fft(chunk, n=4096))
        freqs = np.fft.fftshift(np.fft.fftfreq(4096, 1/FS)) / 1e3
        power_db = 20 * np.log10(np.abs(fft_vals) + 1e-12)

        style_ax(ax, title=comp["title"], xlabel='Freq offset (kHz)', title_color=comp["color"])
        ax.plot(freqs, power_db, color=comp["color"], linewidth=0.7, alpha=0.9)
        ax.fill_between(freqs, power_db, -90, alpha=0.12, color=comp["color"])
        ax.set_xlim(-500, 500)
        ax.set_ylim(-80, 5)

    axes[0].set_ylabel('Power (dB)', color=C_TEXT, fontsize=10)

    fig.suptitle('FFT Power Spectrum Comparison — Three Signal Types',
                 color=C_TEXT, fontsize=13, fontweight='bold', y=1.02)
    fig.tight_layout()
    fig.savefig(OUT / 'fft_comparison.png', dpi=180, facecolor=C_BG, bbox_inches='tight')
    plt.close(fig)
    print("  -> fft_comparison.png")


def plot_ook_waveform(t, signal, events):
    """Create time-domain amplitude envelope."""
    fig, ax = plt.subplots(figsize=(16, 3.5))
    fig.patch.set_facecolor(C_BG)
    style_ax(ax, title='Signal Amplitude Envelope — Burst Detection Timeline',
             xlabel='Time (s)', ylabel='Amplitude')

    amplitude = np.abs(signal)
    ds = 200
    t_ds = t[::ds]
    amp_ds = amplitude[::ds]

    ax.plot(t_ds, amp_ds, color=C_ACCENT1, linewidth=0.4, alpha=0.7)
    ax.fill_between(t_ds, amp_ds, alpha=0.15, color=C_ACCENT1)
    ax.axhline(y=0.02, color=C_ACCENT2, linewidth=1, linestyle='--', alpha=0.7, label='Detection threshold')

    for evt in events:
        ax.axvspan(evt["time"], evt["time"] + evt["duration"], alpha=0.15, color=evt["color"])
        ax.annotate(evt["label"].split("(")[0].strip(),
                    xy=(evt["time"], 0.13), fontsize=6.5, color=evt["color"],
                    rotation=45, ha='left', va='bottom')

    ax.set_xlim(0, DURATION)
    ax.legend(loc='upper right', facecolor=C_BG, edgecolor=C_GRID, labelcolor=C_TEXT, fontsize=8)

    fig.tight_layout()
    fig.savefig(OUT / 'amplitude_envelope.png', dpi=180, facecolor=C_BG, bbox_inches='tight')
    plt.close(fig)
    print("  -> amplitude_envelope.png")


def plot_mystery_signal(t, signal, events):
    """Focus plot on the mystery signals at the end of the capture."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), gridspec_kw={'height_ratios': [2, 1]})
    fig.patch.set_facecolor(C_BG)

    start_t, end_t = 4.4, 5.6
    si, ei = int(start_t * FS), int(end_t * FS)

    style_ax(ax1, title='The Mystery Bursts — Signal or Noise?', ylabel='Freq offset (kHz)',
             title_color=C_ACCENT5)
    ax1.specgram(signal[si:ei], NFFT=512, Fs=FS/1e6, noverlap=480,
                 cmap='inferno', vmin=-85, vmax=-25)

    # Annotate mysteries
    for evt in events:
        if evt["type"] == "mystery":
            rel_time = evt["time"] - start_t
            ax1.axvline(x=rel_time, color=C_ACCENT5, linewidth=2, linestyle='-', alpha=0.8)
            ax1.annotate(
                '???', xy=(rel_time, 0.3), fontsize=18, color=C_ACCENT5,
                fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=C_BG, edgecolor=C_ACCENT5, alpha=0.9))

    style_ax(ax2, title='Amplitude — barely above the noise floor',
             xlabel='Time (s)', ylabel='Amplitude', title_color=C_ACCENT5)
    amp = np.abs(signal[si:ei])
    t_region = np.linspace(start_t, end_t, len(amp))
    ds = 100
    ax2.plot(t_region[::ds], amp[::ds], color=C_ACCENT5, linewidth=0.5, alpha=0.8)
    ax2.fill_between(t_region[::ds], amp[::ds], alpha=0.1, color=C_ACCENT5)
    ax2.axhline(y=0.02, color=C_ACCENT2, linewidth=1.5, linestyle='--', alpha=0.8)
    ax2.annotate('Threshold', xy=(end_t - 0.05, 0.022), fontsize=8, color=C_ACCENT2, ha='right')

    fig.tight_layout()
    fig.savefig(OUT / 'mystery_signal.png', dpi=180, facecolor=C_BG, bbox_inches='tight')
    plt.close(fig)
    print("  -> mystery_signal.png")


def plot_protocol_diagram():
    """Create a visual diagram of the ping-response protocol."""
    fig, ax = plt.subplots(figsize=(14, 4))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')

    ax.text(5, 3.7, 'TabCat V2 — Observed Ping-Response Protocol Pattern',
            ha='center', fontsize=14, fontweight='bold', color=C_TEXT)

    # Handset timeline
    ax.annotate('', xy=(9, 2.8), xytext=(1, 2.8),
                arrowprops=dict(arrowstyle='->', color=C_ACCENT1, lw=2))
    ax.text(0.5, 2.8, 'Handset', fontsize=10, fontweight='bold', color=C_ACCENT1, va='center')

    # Tag timeline
    ax.annotate('', xy=(9, 1.2), xytext=(1, 1.2),
                arrowprops=dict(arrowstyle='->', color=C_ACCENT3, lw=2))
    ax.text(0.5, 1.2, 'Tag', fontsize=10, fontweight='bold', color=C_ACCENT3, va='center')

    # Ping-response pairs
    for i, x_start in enumerate([2.0, 4.5, 7.0]):
        # Handset ping
        rect = FancyBboxPatch((x_start, 2.5), 0.8, 0.6, boxstyle="round,pad=0.05",
                              facecolor=C_ACCENT1, alpha=0.3, edgecolor=C_ACCENT1)
        ax.add_patch(rect)
        ax.text(x_start + 0.4, 2.8, f'PING', ha='center', va='center',
                fontsize=8, fontweight='bold', color=C_ACCENT1)

        # Arrow down
        ax.annotate('', xy=(x_start + 0.6, 1.5), xytext=(x_start + 0.4, 2.5),
                    arrowprops=dict(arrowstyle='->', color=C_ACCENT4, lw=1.5, linestyle='--'))

        # Tag response
        resp_x = x_start + 0.8
        rect2 = FancyBboxPatch((resp_x, 0.9), 0.6, 0.6, boxstyle="round,pad=0.05",
                               facecolor=C_ACCENT3, alpha=0.3, edgecolor=C_ACCENT3)
        ax.add_patch(rect2)
        ax.text(resp_x + 0.3, 1.2, f'RESP', ha='center', va='center',
                fontsize=8, fontweight='bold', color=C_ACCENT3)

        # Timing label
        ax.text(x_start + 0.7, 2.0, '~500ms\ngap', ha='center', va='center',
                fontsize=6, color=C_ACCENT4, style='italic')

    # Mystery at the end
    rect3 = FancyBboxPatch((8.2, 1.8), 0.6, 0.6, boxstyle="round,pad=0.05",
                           facecolor=C_ACCENT5, alpha=0.3, edgecolor=C_ACCENT5, linestyle='--')
    ax.add_patch(rect3)
    ax.text(8.5, 2.1, '???', ha='center', va='center',
            fontsize=12, fontweight='bold', color=C_ACCENT5)

    fig.tight_layout()
    fig.savefig(OUT / 'protocol_diagram.png', dpi=180, facecolor=C_BG, bbox_inches='tight')
    plt.close(fig)
    print("  -> protocol_diagram.png")


def generate_animation(t, signal, events):
    """Create 60fps animation with spectrogram waterfall + live FFT."""
    fig = plt.figure(figsize=(16, 5.5))
    fig.patch.set_facecolor(C_BG)
    gs = GridSpec(1, 2, width_ratios=[2.2, 1], wspace=0.25)

    ax_spec = fig.add_subplot(gs[0])
    ax_fft = fig.add_subplot(gs[1])
    style_ax(ax_spec, title='Live Spectrogram Waterfall', ylabel='Freq offset (kHz)')
    style_ax(ax_fft, title='Instantaneous FFT', xlabel='Freq (kHz)', ylabel='Power (dB)',
             title_color=C_ACCENT2)

    fps = 60
    nfft = 512
    n_freq = nfft // 2 + 1
    hop = int(FS / fps)
    waterfall_len = 250
    waterfall = np.full((n_freq, waterfall_len), -85.0)
    total_frames = min(int((len(signal) - nfft) / hop), fps * 6)

    im = ax_spec.imshow(
        waterfall, aspect='auto', origin='lower',
        extent=[0, waterfall_len, -FS/2e3, FS/2e3],
        cmap='inferno', vmin=-85, vmax=-25,
        interpolation='bilinear',
    )
    ax_spec.set_xlabel('Time (frames)', color=C_TEXT, fontsize=9)

    fft_freqs = np.fft.fftshift(np.fft.fftfreq(nfft, 1/FS)) / 1e3
    fft_line, = ax_fft.plot(fft_freqs, np.zeros(nfft), color=C_ACCENT1, linewidth=0.8)
    fft_fill = ax_fft.fill_between(fft_freqs, np.zeros(nfft), -85, alpha=0.1, color=C_ACCENT1)
    ax_fft.set_xlim(-500, 500)
    ax_fft.set_ylim(-75, 5)

    time_text = ax_spec.text(0.02, 0.95, '', transform=ax_spec.transAxes,
                             color=C_TEXT, fontsize=11, fontweight='bold',
                             verticalalignment='top', family='monospace',
                             bbox=dict(boxstyle='round', facecolor=C_BG, edgecolor=C_GRID, alpha=0.9))
    signal_text = ax_spec.text(0.98, 0.95, '', transform=ax_spec.transAxes,
                               color=C_ACCENT3, fontsize=11, fontweight='bold',
                               verticalalignment='top', horizontalalignment='right',
                               bbox=dict(boxstyle='round', facecolor=C_BG, edgecolor=C_ACCENT3, alpha=0.9))
    freq_text = ax_fft.text(0.02, 0.95, '', transform=ax_fft.transAxes,
                            color=C_TEXT, fontsize=9,
                            verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor=C_BG, edgecolor=C_GRID, alpha=0.9))

    def update(frame):
        nonlocal waterfall, fft_fill
        start = frame * hop
        end = start + nfft
        if end > len(signal):
            return []

        chunk = signal[start:end]
        current_time = start / FS

        fft_col = np.fft.fftshift(np.fft.fft(chunk))
        power_col = 20 * np.log10(np.abs(fft_col[:n_freq]) + 1e-12)

        waterfall = np.roll(waterfall, -1, axis=1)
        waterfall[:, -1] = power_col
        im.set_data(waterfall)

        fft_data = 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(chunk))) + 1e-12)
        fft_line.set_ydata(fft_data)
        fft_fill.remove()
        fft_fill = ax_fft.fill_between(fft_freqs, fft_data, -85, alpha=0.1, color=C_ACCENT1)

        time_text.set_text(f't = {current_time:.3f}s')

        amp = np.max(np.abs(chunk))
        if amp > 0.06:
            signal_text.set_text('SIGNAL DETECTED')
            signal_text.set_color('#ff4444')
            freq_text.set_text(f'Peak: {fft_freqs[np.argmax(fft_data)]:.0f} kHz\nAmp: {amp:.3f}')
        elif amp > 0.02:
            signal_text.set_text('weak signal?')
            signal_text.set_color(C_ACCENT5)
            freq_text.set_text(f'Amp: {amp:.4f}')
        else:
            signal_text.set_text('')
            freq_text.set_text('')

        return [im, fft_line, fft_fill, time_text, signal_text, freq_text]

    print(f"  Rendering {total_frames} frames at {fps}fps...")
    anim = animation.FuncAnimation(fig, update, frames=total_frames, interval=1000/fps, blit=False)

    writer = animation.FFMpegWriter(fps=fps, bitrate=4000,
                                     extra_args=['-pix_fmt', 'yuv420p'])
    anim.save(OUT / 'spectrum_animation.mp4', writer=writer, dpi=120)
    plt.close(fig)
    print("  -> spectrum_animation.mp4")

    # GIF preview at lower fps
    print("  Generating GIF preview...")
    fig2 = plt.figure(figsize=(14, 5))
    fig2.patch.set_facecolor(C_BG)
    gs2 = GridSpec(1, 2, width_ratios=[2, 1], wspace=0.25)
    ax_s2 = fig2.add_subplot(gs2[0])
    ax_f2 = fig2.add_subplot(gs2[1])
    style_ax(ax_s2, title='Spectrogram', ylabel='Freq (kHz)')
    style_ax(ax_f2, title='FFT', xlabel='Freq (kHz)', title_color=C_ACCENT2)

    waterfall2 = np.full((n_freq, waterfall_len), -85.0)
    im2 = ax_s2.imshow(waterfall2, aspect='auto', origin='lower',
                        extent=[0, waterfall_len, -FS/2e3, FS/2e3],
                        cmap='inferno', vmin=-85, vmax=-25, interpolation='bilinear')
    fft_line2, = ax_f2.plot(fft_freqs, np.zeros(nfft), color=C_ACCENT1, linewidth=0.8)
    fft_fill2 = ax_f2.fill_between(fft_freqs, np.zeros(nfft), -85, alpha=0.1, color=C_ACCENT1)
    ax_f2.set_xlim(-500, 500)
    ax_f2.set_ylim(-75, 5)
    time_text2 = ax_s2.text(0.02, 0.95, '', transform=ax_s2.transAxes,
                             color=C_TEXT, fontsize=10, fontweight='bold',
                             verticalalignment='top', family='monospace',
                             bbox=dict(boxstyle='round', facecolor=C_BG, alpha=0.9))

    gif_fps = 15
    gif_hop = int(FS / gif_fps)
    gif_frames = min(int((len(signal) - nfft) / gif_hop), gif_fps * 6)

    def update_gif(frame):
        nonlocal waterfall2, fft_fill2
        start = frame * gif_hop
        end = start + nfft
        if end > len(signal):
            return []
        chunk = signal[start:end]
        fft_col = np.fft.fftshift(np.fft.fft(chunk))
        power_col = 20 * np.log10(np.abs(fft_col[:n_freq]) + 1e-12)
        waterfall2[:] = np.roll(waterfall2, -1, axis=1)
        waterfall2[:, -1] = power_col
        im2.set_data(waterfall2)
        fft_data = 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(chunk))) + 1e-12)
        fft_line2.set_ydata(fft_data)
        fft_fill2.remove()
        fft_fill2 = ax_f2.fill_between(fft_freqs, fft_data, -85, alpha=0.1, color=C_ACCENT1)
        time_text2.set_text(f't = {start/FS:.2f}s')
        return [im2, fft_line2, fft_fill2, time_text2]

    anim2 = animation.FuncAnimation(fig2, update_gif, frames=gif_frames, interval=1000/gif_fps, blit=False)
    anim2.save(OUT / 'spectrum_preview.gif', writer='pillow', dpi=80)
    plt.close(fig2)
    print("  -> spectrum_preview.gif")


def generate_slider_data(t, signal, events):
    """Generate JSON data for the interactive JS slider visualization."""
    nfft = 512
    hop = 2048
    n_frames = min((len(signal) - nfft) // hop, 500)

    fft_snapshots = []
    amplitudes = []
    times = []
    n_bins = 64

    for i in range(n_frames):
        start = i * hop
        chunk = signal[start:start+nfft]
        fft_vals = np.fft.fftshift(np.fft.fft(chunk))
        power = 20 * np.log10(np.abs(fft_vals) + 1e-12)
        ds_power = power.reshape(n_bins, -1).mean(axis=1)
        fft_snapshots.append([round(float(x), 1) for x in ds_power])
        amplitudes.append(round(float(np.max(np.abs(chunk))), 5))
        times.append(round(start / FS, 4))

    event_markers = [
        {"time": evt["time"], "label": evt["label"], "type": evt["type"],
         "frame": min(int(evt["time"] * FS / hop), n_frames - 1)}
        for evt in events
    ]

    slider_data = {
        "center_freq_mhz": CENTER / 1e6,
        "sample_rate_mhz": FS / 1e6,
        "n_frames": n_frames,
        "freq_bins": n_bins,
        "freq_range_khz": [round(-FS/2e3), round(FS/2e3)],
        "times": times,
        "amplitudes": amplitudes,
        "fft_snapshots": fft_snapshots,
        "events": event_markers,
    }

    with open(OUT / 'slider_data.json', 'w') as f:
        json.dump(slider_data, f)

    size_kb = len(json.dumps(slider_data)) // 1024
    print(f"  -> slider_data.json ({n_frames} frames, {size_kb}KB)")
    return slider_data


if __name__ == "__main__":
    print("Generating simulated TabCat V2 2435 MHz RF data...")
    t, signal, events = generate_tabcat_signal()
    print(f"  {len(signal):,} samples, {DURATION}s duration\n")

    print("Static plots...")
    plot_spectrogram(t, signal, events)
    plot_fft_comparison(signal, events)
    plot_ook_waveform(t, signal, events)
    plot_mystery_signal(t, signal, events)
    plot_protocol_diagram()

    print("\nSlider data...")
    slider_data = generate_slider_data(t, signal, events)

    print("\nAnimation...")
    try:
        generate_animation(t, signal, events)
    except Exception as e:
        print(f"  Animation failed: {e}")
        print("  (ffmpeg required for MP4; static plots still available)")

    print("\nDone!")
