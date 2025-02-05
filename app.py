from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import pandas as pd
from googletrans import Translator

app = Flask(__name__)
CORS(app)

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
translator = Translator()

# Updated Database model
class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(100), nullable=False)
    kannada = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(255))
    audio_file = db.Column(db.String(255))

def initialize_database():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

initialize_database()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/save_data', methods=['POST'])
def save_data():
    try:
        english_text = request.form['english']
        
        translation = translator.translate(english_text, src='en', dest='kn')
        kannada_text = translation.text

        image_filename = save_uploaded_file(request.files.get('image'))
        audio_filename = save_uploaded_file(request.files.get('audio'))

        new_entry = Translation(
            english=english_text,
            kannada=kannada_text,
            image_file=image_filename,
            audio_file=audio_filename
        )

        db.session.add(new_entry)
        db.session.commit()

        save_to_excel(new_entry)

        return jsonify({
            "message": "Data saved successfully!",
            "kannada": kannada_text,
            "id": new_entry.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def save_uploaded_file(file):
    if file and file.filename:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return file.filename  # Store only the filename (not the full path)
    return None

def save_to_excel(entry):
    excel_file = 'translations_data.xlsx'
    columns = ["ID", "English", "Kannada", "Image File", "Audio File"]
    
    try:
        if not os.path.exists(excel_file):
            pd.DataFrame(columns=columns).to_excel(excel_file, index=False)
            
        with pd.ExcelFile(excel_file) as xls:
            df = pd.read_excel(xls)
        
        new_row = {
            "ID": entry.id,
            "English": entry.english,
            "Kannada": entry.kannada,
            "Image File": entry.image_file,
            "Audio File": entry.audio_file
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False)
            
    except Exception as e:
        print(f"Error saving to Excel: {e}")

# Get Translation data based on English word
@app.route('/get_translation', methods=['GET'])
def get_translation():
    try:
        english_word = request.args.get('english')
        
        # Query the database for the translation
        translation = Translation.query.filter_by(english=english_word).first()
        
        if translation:
            return jsonify({
                "kannada": translation.kannada,
                "image_file": translation.image_file,
                "audio_file": translation.audio_file
            })
        else:
            return jsonify({"error": "Translation not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
