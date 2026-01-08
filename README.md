# Photo to Playlist

Transform any photo into a personalized music playlist using AI-powered image analysis and music recommendation.

## Overview

**Photo to Playlist** analyzes the mood, setting, and atmosphere of your photos using computer vision AI, then generates a matching playlist of songs. Upload a beach sunset photo and get chill summer vibes. Upload a party scene and get upbeat dance tracks.

### How It Works

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Upload    │ ──▶ │  AI Vision      │ ──▶ │  Music Params    │ ──▶ │  Generate   │
│   Photo     │     │  Analysis       │     │  Extraction      │     │  Playlist   │
└─────────────┘     └─────────────────┘     └──────────────────┘     └─────────────┘
                           │                        │                       │
                    OpenAI GPT-4V           OpenAI GPT-4              Deezer API
                    or Ollama               or Ollama                     +
                                                                    Spotify Export
```

1. **Image Analysis**: AI analyzes your photo to understand the scene, mood, colors, setting, and atmosphere
2. **Parameter Generation**: Converts the visual analysis into music parameters (tempo, energy, valence, genres)
3. **Playlist Creation**: Searches Deezer for matching tracks and creates a curated playlist
4. **Spotify Export**: Optionally save your playlist directly to your Spotify account

## Features

- **AI-Powered Image Analysis**: Uses OpenAI GPT-4 Vision or local Ollama models
- **Smart Music Matching**: Translates visual vibes into musical parameters
- **Web UI**: Modern Streamlit interface with real-time progress
- **Spotify Integration**: OAuth 2.0 flow to save playlists to your account
- **Flexible Model Support**: Choose between OpenAI (cloud) or Ollama (local)
- **Customizable**: Adjust number of tracks and model preferences

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key (for GPT-4 Vision) OR Ollama installed locally
- Spotify Developer credentials (optional, for Spotify export)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/photo-to-playlist.git
   cd photo-to-playlist
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .\.venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=your-openai-api-key
   
   # Spotify Configuration (optional - for Spotify export)
   SPOTIFY_CLIENT_ID=your-spotify-client-id
   SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
   ```

5. **Run the app**
   ```bash
   streamlit run src/app/main.py
   ```

6. Open http://localhost:8501 in your browser

## Configuration

### OpenAI Setup

1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add it to your `.env` file as `OPENAI_API_KEY`

### Spotify Setup (Optional)

To enable "Save to Spotify" functionality:

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Set the Redirect URI to `http://127.0.0.1:8888/callback`
4. Copy your Client ID and Client Secret to `.env`

### Using Ollama (Local AI)

For privacy or offline use, you can use Ollama instead of OpenAI:

1. Install [Ollama](https://ollama.ai/)
2. Pull a vision-capable model: `ollama pull llava`
3. Select "Ollama" in the app's model configuration

## Project Structure

```
photo_to_playlist/
├── src/
│   ├── app/                    # Streamlit web application
│   │   ├── main.py            # App entry point
│   │   ├── components/        # UI components
│   │   └── utils/             # UI utilities
│   ├── vision/                # Image analysis modules
│   │   ├── openai.py          # OpenAI GPT-4V provider
│   │   └── ollama.py          # Ollama local provider
│   ├── params/                # Music parameter generation
│   │   ├── openai.py          # OpenAI parameter converter
│   │   └── ollama.py          # Ollama parameter converter
│   ├── playlist/              # Playlist generation
│   │   ├── deezer.py          # Deezer API integration
│   │   ├── spotify_client.py  # Spotify API client
│   │   └── oauth_server.py    # OAuth callback server
│   ├── storage/               # Data persistence
│   ├── pipeline.py            # Main pipeline orchestration
│   └── env_config.py          # Environment configuration
├── prompts/                   # AI prompt templates
├── requirements.txt
├── .env.example
└── README.md
```

## Usage

1. **Upload a Photo**: Click "Upload Photo" and select an image
2. **Configure Models**: Choose your preferred AI models (OpenAI/Ollama)
3. **Generate Playlist**: Click "Generate Playlist" and watch the magic happen
4. **Preview Tracks**: Listen to 30-second previews of each track
5. **Save to Spotify**: Connect your Spotify account and save the playlist

## Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4 Vision, Ollama (LLaVA)
- **Music APIs**: Deezer, Spotify
- **Authentication**: OAuth 2.0 (Spotify)
- **Environment**: python-dotenv

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

## Acknowledgments

- [OpenAI](https://openai.com/) for GPT-4 Vision API
- [Ollama](https://ollama.ai/) for local AI models
- [Deezer](https://developers.deezer.com/) for music API
- [Spotify](https://developer.spotify.com/) for playlist integration
- [Streamlit](https://streamlit.io/) for the web framework

