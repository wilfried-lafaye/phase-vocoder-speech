"""
Visualization utilities for audio data.

Functions to plot audio waveforms, spectrograms, and comparisons using matplotlib and Streamlit.
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display


def plot_audio_waveform(audio_data, sample_rate, title='Audio Waveform'):
    """
    Plot the waveform of an audio signal.

    Args:
        audio_data (np.ndarray): Audio signal data.
        sample_rate (int): Sampling rate of the audio.
        title (str): Title of the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 3))

    times = np.arange(len(audio_data)) / sample_rate

    ax.plot(times, audio_data, linewidth=0.5)

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)
    plt.close()


def plot_spectrogram(audio_data, sample_rate, title='Spectrogram'):
    """
    Plot the spectrogram of an audio signal.

    Args:
        audio_data (np.ndarray): Audio signal data.
        sample_rate (int): Sampling rate of the audio.
        title (str): Title of the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 4))

    spectrogram_db = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data)), ref=np.max)

    img = librosa.display.specshow(
        spectrogram_db,
        x_axis='time',
        y_axis='hz',
        sr=sample_rate,
        ax=ax,
    )

    ax.set_title(title)

    fig.colorbar(img, ax=ax, format='%+2.0f dB')

    st.pyplot(fig)
    plt.close()


def plot_comparison(original_data, processed_data, sample_rate):
    """
    Plot original and processed audio waveforms side by side.

    Args:
        original_data (np.ndarray): Original audio data.
        processed_data (np.ndarray): Processed audio data.
        sample_rate (int): Sampling rate of the audio.
    """
    col1, col2 = st.columns(2)

    with col1:
        plot_audio_waveform(original_data, sample_rate, 'Original')

    with col2:
        plot_audio_waveform(processed_data, sample_rate, 'Processed')
