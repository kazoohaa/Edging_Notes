# Mel-Spectrogram

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 1) Load audio (replace "test.wav" with your file)
y, sr = librosa.load("test.wav", sr=None)

# 2) Compute Mel-spectrogram
#    - n_mels sets the number of Mel bands (vertical resolution)
#    - fmax sets the upper frequency limit of the Mel scale
S_mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=4096)

# 3) Convert power (amplitude^2) to decibels
S_mel_dB = librosa.power_to_db(S_mel, ref=np.max)

# 4) Plot
fig, ax = plt.subplots(figsize=(8, 6))
img = librosa.display.specshow(
    S_mel_dB, 
    sr=sr,
    x_axis='time', 
    y_axis='mel',
    fmax=4096, 
    ax=ax,
    cmap='plasma',   # Choose a colormap you like: 'plasma', 'magma', etc.
    vmin=-80,        # Set the range to match your screenshot
    vmax=0
)

# 5) Add a colorbar and label
cbar = fig.colorbar(img, ax=ax, format='%+2.0f dB')
cbar.set_label('Amplitude (dB)')

# 6) Title and show
ax.set_title('Mel-frequency spectrogram')
plt.tight_layout()
plt.show()
