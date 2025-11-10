"""
Main application module for Audio Vocoder.

This app allows users to upload audio files, apply audio effects,
and visualize or download the processed audio.
"""

import tempfile

import streamlit as st

from audio_processor import AudioProcessor
from utils.visualization import (
    plot_audio_waveform,
    plot_spectrogram,
    plot_comparison,
)
from utils.file_utils import save_uploaded_file, cleanup_temp_files
import config


st.set_page_config(page_title='Audio Vocoder', layout='wide')


def select_effect_and_params(audio_processor):
    """
    UI for selecting an audio effect and setting its parameters.

    Args:
        audio_processor (AudioProcessor): The audio processor instance.

    Returns:
        tuple: selected_effect name (str), parameters (dict)
    """
    st.subheader('Audio Effects')
    effect_names = {
        'robot': 'Robot Effect',
        'pitch': 'Pitch Shift',
        'speed': 'Speed Change',
        'echo': 'Echo',
    }
    selected_effect = st.selectbox('Choose effect', options=list(effect_names.keys()))
    effect = audio_processor.effects[selected_effect]

    st.subheader('Parameters')
    params = effect.get_parameter_widgets()
    return selected_effect, params


def process_and_display_audio(audio_processor, context, params):
    """
    Process the audio using the selected effect and display results.

    Args:
        audio_processor (AudioProcessor): The audio processor instance.
        context (dict): Dictionary containing:
            - input_path (str): Path to input audio file.
            - uploaded_file: Uploaded file object.
            - selected_effect (str): Name of the effect.
            - original_audio (np.ndarray): Original audio data.
            - sample_rate (int): Original sample rate.
        params (dict): Effect parameters.

    Returns:
        output_path (str): Path to processed audio file.
    """
    st.subheader('Result')

    processed_audio, processed_sr = audio_processor.process_audio(
        context['input_path'], context['selected_effect'], params
    )

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
        output_path = tmp_file.name

    audio_processor.save_audio(processed_audio, processed_sr, output_path)

    plot_comparison(
        context['original_audio'],
        processed_audio,
        context['sample_rate'],
    )
    st.audio(output_path)

    with open(output_path, 'rb') as f:
        st.download_button(
            label='Download Result',
            data=f,
            file_name=f"processed_{context['uploaded_file'].name}",
            mime='audio/wav',
        )

    return output_path


def main():
    """
    Main function to run the Streamlit Audio Vocoder app.
    """
    st.title('Audio Vocoder App')
    st.write('Audio processing application with modular effects')

    config.Config.ensure_directories()

    audio_processor = AudioProcessor()

    uploaded_file = st.file_uploader('Choose an audio file', type=['wav', 'mp3'])

    if uploaded_file is not None:
        if uploaded_file.size > config.Config.MAX_FILE_SIZE:
            st.error('File too large')
            return

        input_path = save_uploaded_file(uploaded_file)

        try:
            original_audio, sample_rate = audio_processor.load_audio(input_path)

            st.subheader('Original Signal')
            col1, col2 = st.columns(2)
            with col1:
                plot_audio_waveform(original_audio, sample_rate, 'Original Waveform')
            with col2:
                plot_spectrogram(original_audio, sample_rate, 'Original Spectrogram')

            st.audio(input_path)

            selected_effect, params = select_effect_and_params(audio_processor)

            if st.button('Apply Effect'):
                with st.spinner('Processing...'):
                    try:
                        context = {
                            'input_path': input_path,
                            'uploaded_file': uploaded_file,
                            'selected_effect': selected_effect,
                            'original_audio': original_audio,
                            'sample_rate': sample_rate,
                        }
                        output_path = process_and_display_audio(
                            audio_processor, context, params
                        )
                        cleanup_temp_files([output_path])
                    except (IOError, ValueError) as ex:
                        st.error(f'Processing error: {str(ex)}')
        except (IOError, ValueError) as ex:
            st.error(f'Error: {str(ex)}')
        finally:
            cleanup_temp_files([input_path])


if __name__ == '__main__':
    main()
