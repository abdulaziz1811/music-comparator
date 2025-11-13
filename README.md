# Music Comparator

This project allows users to compare two audio tracks by analyzing key musical features such as waveforms, spectrograms, tempo, and frequency energy.
It is built using Python, Librosa, and Streamlit, and includes support for Arabic text rendering.

## Features

- Upload two audio files (MP3/WAV).
- Visual comparison of:
  - Waveforms
  - Spectrograms
  - Tempo (BPM)
  - Frequency distribution
- Automatic extraction of audio features.
- Arabic text support using arabic-reshaper and python-bidi.
- Simple and clean Streamlit interface.

## File Structure

Music_Comparator/
    music_comparator.py
    fairuz.jpg
    Amiri-Regular1.ttf
    requirements.txt
    README.md

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   streamlit run music_comparator.py

3. Upload two audio files and view the analysis.

## Notes

- The application supports both English and Arabic text.
- For accurate analysis, use high-quality audio files.
- This project performs feature-based analysis without ML models.

## License

This project is for educational and personal use.
