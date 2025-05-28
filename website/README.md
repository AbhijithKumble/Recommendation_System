# Anime Recommendation System - Project Structure

## 📁 Directory Structure

```
anime_recommender/
│
├── main.py                          # Main Streamlit application
│
├── config/
│   ├── __init__.py
│   └── settings.py                  # Configuration settings
│
├── ui/
│   ├── __init__.py
│   ├── styles.py                    # Custom CSS styles
│   ├── components.py                # Reusable UI components
│   └── tabs.py                      # Main tab components
│
├── utils/
│   ├── __init__.py
│   ├── model_loader.py              # Model loading utilities
│   ├── recommendation_handler.py    # Recommendation processing
│   ├── analytics.py                 # Analytics and statistics
│   └── jikan_api.py                 # Your existing API utilities
│
├── recommender/
│   ├── __init__.py
│   ├── content_based.py             # Your existing content-based system
│   └── collaborative.py             # Your existing collaborative system
│
├── requirements.txt                 # Python dependencies
└── README.md                       # Project documentation
```

## 🚀 Setup Instructions

### 1. Create Directory Structure
```bash
mkdir -p anime_recommender/{config,ui,utils,recommender}
touch anime_recommender/{config,ui,utils,recommender}/__init__.py
```

### 2. Install Dependencies
```bash
pip install streamlit pandas plotly pillow requests
```

### 3. Create requirements.txt
```txt
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
Pillow>=9.0.0
requests>=2.28.0
scikit-learn>=1.3.0
numpy>=1.24.0
```

### 4. File Organization

Copy the provided code into respective files:

1. **main.py** - Main Streamlit application
2. **config/settings.py** - Configuration settings
3. **ui/styles.py** - Custom CSS styles
4. **ui/components.py** - Reusable UI components
5. **ui/tabs.py** - Main tab components  
6. **utils/model_loader.py** - Model loading utilities
7. **utils/recommendation_handler.py** - Recommendation processing
8. **utils/analytics.py** - Analytics and statistics

### 5. Your Existing Files
Keep your existing files in their respective locations:
- **utils/jikan_api.py** - Your API utilities
- **recommender/content_based.py** - Your content-based system
- **recommender/collaborative.py** - Your collaborative system

## 🔧 Key Features Handled

### Different Return Formats
The `utils/recommendation_handler.py` handles the different return formats:
- **Content-based**: Returns list format → processed as-is
- **Collaborative**: Returns DataFrame format → converted to list of dicts using `to_dict('records')`

### Recommendation Processing
```python
def normalize_recommendations(recommendations: Union[List, pd.DataFrame]) -> List[Dict[str, Any]]:
    if isinstance(recommendations, pd.DataFrame):
        return recommendations.to_dict('records')
    elif isinstance(recommendations, list):
        return recommendations
    else:
        return []
```

### Hybrid System
Combines both methods:
```python
def get_hybrid_recommendations(...):
    content_recs = get_content_based_recommendations(...)
    collab_recs = get_collaborative_recommendations(...)
    combined_recs = content_recs + collab_recs
    # Remove duplicates and return
```

## 🎨 UI/UX Features

- **Modern Design**: Gradient headers, hover effects, custom styling
- **Responsive Layout**: Works on different screen sizes
- **Interactive Elements**: Smooth animations and transitions
- **Analytics Dashboard**: Visual charts and statistics
- **History Tracking**: User activity tracking and export
- **Advanced Filtering**: Genre, score, episode filters
- **Error Handling**: User-friendly error messages

## 🚀 Running the Application

```bash
cd anime_recommender
streamlit run main.py
```

## 📊 Features Overview

### Main Tabs
1. **🎯 Get Recommendations** - Main recommendation interface
2. **🔍 Search Anime** - Direct anime search and random discovery
3. **📊 Analytics** - Usage statistics and visualizations  
4. **📝 History** - Recommendation history with export

### Recommendation Methods
- **Hybrid (Best)** - Combines content-based and collaborative
- **Content-Based** - Uses your existing content-based system
- **Collaborative Filtering** - Uses your existing collaborative system

### Advanced Features
- **Real-time filtering** based on user preferences
- **Visual analytics** with Plotly charts
- **Session management** with state persistence
- **Export functionality** for history data
- **Responsive design** with modern UI elements

## 🔒 Data Handling

- **No Browser Storage**: All data stored in session state (Streamlit requirement)
- **Memory-based**: Data persists only during the session
- **Export Options**: Users can download their history as CSV

## 🎯 Usage Tips

1. **Model Loading**: Models are cached for performance
2. **Error Handling**: Comprehensive error handling with user feedback
3. **Performance**: Efficient filtering and processing
4. **Extensibility**: Modular design for easy feature additions

The application provides a professional, user-friendly interface for anime recommendations with comprehensive analytics and modern UI/UX design!
