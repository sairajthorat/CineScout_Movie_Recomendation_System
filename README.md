# 🎬 CineScout - Movie Recommendation System

A modern, AI-powered movie recommendation web application built with Streamlit that helps users discover their next favorite movies.

## ✨ Features

- **Personalized Recommendations**: Get movie suggestions based on your favorite films
- **Beautiful Dark Theme**: Modern, cinema-inspired dark interface
- **Interactive Loading**: Animated progress bar with real-time updates
- **Movie Details**: Rich movie cards with posters, titles, and plot summaries
- **Responsive Design**: Works perfectly on desktop and mobile devices

## 🚀 Live Demo

[Visit CineScout](your-streamlit-app-url-here)

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Python**: Backend logic and ML algorithms
- **Scikit-learn**: Machine learning for recommendations
- **OMDB API**: Movie data and posters
- **CSS**: Custom styling and animations

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cinescout.git
cd cinescout
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OMDB API key:
   - Get a free API key from [OMDB API](http://www.omdbapi.com/apikey.aspx)
   - Create a `config.json` file:
   ```json
   {
     "OMDB_API_KEY": "your_api_key_here"
   }
   ```

4. Run the application:
```bash
streamlit run main.py
```

## 🌐 Deployment

This app is deployed on Streamlit Community Cloud. To deploy your own version:

1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your OMDB API key as a secret in the Streamlit dashboard
5. Deploy!

## 📁 Project Structure

```
cinescout/
├── main.py              # Main Streamlit application
├── recommend.py         # Recommendation algorithm
├── omdb_utils.py        # OMDB API utilities
├── style_loader.py      # CSS loading utilities
├── styles.css           # Custom CSS styling
├── requirements.txt     # Python dependencies
├── movies.csv          # Movie dataset
└── .streamlit/
    └── config.toml     # Streamlit configuration
```

## 🎯 How It Works

1. **Select a Movie**: Choose a movie you enjoyed from the dropdown
2. **Get Recommendations**: Click the button to start the recommendation process
3. **Watch the Magic**: Enjoy the animated loading experience
4. **Discover Movies**: Browse through personalized movie recommendations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Movie data provided by [OMDB API](http://www.omdbapi.com/)
- Built with [Streamlit](https://streamlit.io/)
- Inspired by modern streaming platforms