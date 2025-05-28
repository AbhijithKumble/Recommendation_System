import streamlit as st


def load_custom_css():
    """Load custom CSS styles for the application"""
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .main-header h1 {
            font-size: 3rem;
            margin: 0;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-header p {
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
        }
        
        .recommendation-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease;
        }
        
        .recommendation-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .anime-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .anime-card:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }
        
        .metric-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin: 0.5rem 0;
        }
        
        .filter-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 1px solid #e9ecef;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .loading-animation {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
        }
        
        .genre-tag {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            margin: 0.2rem;
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .score-badge {
            background: #28a745;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .warning-badge {
            background: #ffc107;
            color: #212529;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .info-badge {
            background: #17a2b8;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .success-message {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
            font-weight: 500;
        }
        
        .error-message {
            background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
            font-weight: 500;
        }
        
        .footer {
            text-align: center;
            color: #666;
            padding: 2rem 1rem;
            margin-top: 3rem;
            border-top: 1px solid #e9ecef;
            background: #f8f9fa;
        }
    </style>
    """, unsafe_allow_html=True)
