"""
Speed effect implementation for audio processing.

Provides functionality to change the speed of audio data.
"""

import librosa
import numpy as np

from effects.base_effect import BaseEffect


class SpeedEffect(BaseEffect):
    """
    Speed change effect class.

    Inherits from BaseEffect.
    """

    def __init__(self):
        """
        Initialize the speed change effect.
        """
        # No special initialization needed

    def apply(self, audio_data, sample_rate, **kwargs):
        """
        Apply speed change to audio data.

        Args:
            audio_data (np.ndarray): Input audio data.
            sample_rate (int): Sample rate of the audio (unused).
            **kwargs: Parameters for the speed effect.
                Expected keys:
                - speed_factor (float): Speed change factor.

        Returns:
            np.ndarray: Processed audio data with altered speed.

        Raises:
            RuntimeError: If processing fails.
        """
        speed_factor = kwargs.get('speed_factor', 1.0)  # default no speed change

        try:
            processed = librosa.effects.time_stretch(audio_data, rate=speed_factor)
            return processed.astype(np.float32)
        except Exception as e:
            raise RuntimeError(f"Speed change error: {str(e)}") from e
