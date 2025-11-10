"""
Pitch effect implementation for audio processing.

Provides pitch shifting audio effect as a subclass of BaseEffect.
"""

import librosa
import numpy as np

from effects.base_effect import BaseEffect


class PitchEffect(BaseEffect):
    """
    Pitch shift effect class to change pitch of audio data.

    Inherits from BaseEffect.
    """

    def __init__(self):
        """
        Initialize the pitch shift effect.
        """
        # No special initialization needed

    def apply(self, audio_data, sample_rate, **kwargs):
        """
        Apply the pitch shift effect to audio data.

        Args:
            audio_data (np.ndarray): Input audio data.
            sample_rate (int): Sample rate of the audio.
            **kwargs: Parameters for the pitch effect.
                Expected keys:
                - n_steps (float): Number of half steps to shift pitch. Positive is higher pitch.

        Returns:
            np.ndarray: Processed audio data with pitch shifted.

        Raises:
            RuntimeError: If processing fails.
        """
        n_steps = kwargs.get('n_steps', 0.0)  # default no pitch shift

        try:
            shifted_audio = librosa.effects.pitch_shift(
                y=audio_data,
                sr=sample_rate,
                n_steps=n_steps,
            )
            return shifted_audio.astype(np.float32)
        except Exception as e:
            raise RuntimeError(f"Pitch shift error: {str(e)}") from e
