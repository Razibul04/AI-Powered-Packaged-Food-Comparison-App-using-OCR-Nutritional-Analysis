# AI-Powered Packaged Food Comparison App using OCR & Nutritional Analysis (Python, JavaScript, React Native)

Description of the project- 

Developed a mobile application that helps users make healthier food choices by comparing packaged food items based on their nutritional values and ingredients. The app leverages OCR to extract nutritional information directly from product labels, processes the data with Python-based AI models, and evaluates health impact using a pre-labeled ingredient database. Built with React Native and JavaScript for cross-platform support, the app delivers real-time, user-friendly comparisons to guide consumers toward smarter dietary decisions.



File Structure - 

AI-Powered-Packaged-Food-Comparison-App/
│
├── backend/                                # Backend modules
│   ├── __pycache__/                        # Python cache files
│   │
│   ├── ocr/                                # OCR (Optical Character Recognition) module
│   │   ├── __init__.py
│   │   ├── ocr_reader.py                   # OCR logic to read food labels
│   │
│   ├── utils/                              # Utility scripts
│   │   ├── __init__.py
│   │   ├── Final_Indian_Ingredient_HealthDataset_Scored.csv
│   │   ├── generate_embeddings.py
│   │   ├── ingredient_cleaner.py
│   │   ├── merge_additives.py
│   │   ├── parse_codex.py
│   │   ├── profile_weights.py
│   │   ├── scoring.py
│   │   ├── scrape_cspi.py
│   │   ├── test_compare.py
│   │
│   ├── ingredient_db.csv                   # Ingredient database
│   └── requirements.txt                    # Dependencies
│
├── frontend/                               # Frontend files
│   ├── index.html                          # Main web interface
│   ├── script.js                           # JavaScript logic
│   └── style.css                           # Styling for frontend
│
├── templates/                              # Flask HTML templates
│
├── test_images/                            # Test images for checking OCR & model
│
├── uploads/                                # Uploaded product images (for testing/comparison)
│
├── app.py                                  # Main Flask backend application
├── README.md                               # Project description/documentation
└── New Text Document.txt                   # Notes / extra reference file
