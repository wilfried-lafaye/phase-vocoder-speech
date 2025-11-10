"""
audio_processor module containing the AudioProcessor class.

This module handles loading, saving, and processing audio files
with various effects.
"""

import librosa
import soundfile as sf

from effects.robot_effect import RobotEffect
from effects.pitch_effect import PitchEffect
from effects.speed_effect import SpeedEffect
from effects.echo_effect import EchoEffect


class AudioProcessor:
    """
    Class for audio processing with various effects.

    It manages loading, saving, and applying audio effects.
    """

    def __init__(self):
        """
        Initialize available effects.
        """
        self.effects = {
            'robot': RobotEffect(),
            'pitch': PitchEffect(),
            'speed': SpeedEffect(),
            'echo': EchoEffect()
        }

    def get_available_effects(self):
        """
        Returns a dictionary of available effects.
        
        Returns:
            dict: Available effects as {name: effect}.
        """
        return dict(self.effects)

    def add_effect(self, name, effect):
        """
        Adds an effect to the processor.

        Args:
            name (str): Name of the effect.
            effect: Instance of the effect.
        """
        self.effects[name] = effect

    def load_audio(self, file_path):
        """
        Loads an audio file.

        Args:
            file_path (str): Path to the audio file to load.

        Returns:
            tuple: (audio_data (np.ndarray), sample_rate (int))

        Raises:
            IOError: If loading fails.
        """
        try:
            audio_data, sample_rate = librosa.load(file_path, sr=None)
            return audio_data, sample_rate
        except Exception as e:
            raise IOError(f'Error loading audio: {str(e)}') from e

    def save_audio(self, audio_data, sample_rate, output_path):
        """
        Saves an audio file.

        Args:
            audio_data (np.ndarray): Audio data to save.
            sample_rate (int): Sampling rate.
            output_path (str): Path to the output file.

        Returns:
            bool: True if save is successful.

        Raises:
            IOError: If saving fails.
        """
        try:
            sf.write(output_path, audio_data, sample_rate)
            return True
        except Exception as e:
            raise IOError(f'Error saving audio: {str(e)}') from e

    def process_audio(self, input_path, effect_name, parameters):
        """
        Applies an audio effect on a file.

        Args:
            input_path (str): Path to the audio file to process.
            effect_name (str): Name of the effect to apply.
            parameters (dict): Parameters of the effect.

        Returns:
            tuple: (processed_audio (np.ndarray), sample_rate (int))

        Raises:
            ValueError: If the requested effect does not exist.
        """
        if effect_name not in self.effects:
            raise ValueError(f'Effect {effect_name} not available')

        audio_data, sample_rate = self.load_audio(input_path)
        effect = self.effects[effect_name]
        processed_audio = effect.apply(audio_data, sample_rate, **parameters)
        return processed_audio, sample_rate
