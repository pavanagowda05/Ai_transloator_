# Ai_transloator_
# English to Kannada Translation System

## Overview
This system automatically translates a given English word into Kannada, provides an image representing the word, and allows the user to input audio of the word. All this data is saved in an Excel sheet for record-keeping.

## Features
- **Automatic Translation:** Translates an English word to Kannada.
- **Image Representation:** Fetches an image relevant to the translated word.
- **Audio Input:** Users can provide audio pronunciation of the word.
- **Data Storage:** Saves all information (word, translation, image, and audio) in an Excel sheet.

## How It Works
1. The user inputs an English word.
2. The system translates it to Kannada.
3. An image related to the word is fetched.
4. The user provides an audio pronunciation.
5. The word, translation, image, and audio are stored in an Excel file.

## Technologies Used
- **Python** for backend processing
- **Google Translate API** for English-to-Kannada translation
- **Pandas** for storing data in Excel
- **Pillow/OpenCV** for image processing
- **Speech Recognition** for handling audio input

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/yourrepository.git
   ```
2. Navigate to the project folder:
   ```sh
   cd yourrepository
   ```
3. Install required dependencies:
   ```sh
   pip install googletrans pandas pillow speechrecognition openpyxl
   ```

## Usage
1. Run the script:
   ```sh
   python main.py
   ```
2. Input the English word.
3. Provide an audio pronunciation when prompted.
4. The translated word, image, and audio file will be saved in an Excel sheet.

## Output Example
The Excel sheet will contain columns like:
| English Word | Kannada Translation | Image Path | Audio Path |
|-------------|--------------------|------------|------------|
| Apple      | ಅಪ್ಪಳೆ  | images/apple.jpg | audio/apple.wav |

## Contributions
Feel free to contribute to this project by submitting issues or pull requests.

## License
This project is licensed under the MIT License.


