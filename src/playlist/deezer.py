#!/usr/bin/env python3
"""
generate_deezer_playlist.py

Takes JSON parameters from CV model pipeline and generates a filtered playlist from Deezer.

Usage:
    python generate_deezer_playlist.py '{"playlist_search_query": "lofi chill", ...}'
    
Or with file:
    python generate_deezer_playlist.py --input params.json
"""

import requests
import json
import sys
import argparse
import os
from datetime import datetime
from typing import List, Dict, Optional


class DeezerPlaylistGenerator:
    def __init__(self):
        self.base_url = "https://api.deezer.com"
        self.log_file = None
    
    def search_playlists(self, query: str, limit: int = 3) -> List[Dict]:
        """
        Search for playlists on Deezer
        
        Args:
            query: Search query string
            limit: Number of playlists to return (default: 3)
        
        Returns:
            List of playlist objects
        """
        url = f"{self.base_url}/search/playlist"
        params = {"q": query, "limit": limit}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            playlists = data.get("data", [])
            print(f"[OK] Found {len(playlists)} playlists for query: '{query}'")
            return playlists
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error searching playlists: {e}", file=sys.stderr)
            return []
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """
        Get all tracks from a specific playlist
        
        Args:
            playlist_id: Deezer playlist ID
        
        Returns:
            List of track objects
        """
        url = f"{self.base_url}/playlist/{playlist_id}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            tracks = data.get("tracks", {}).get("data", [])
            return tracks
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error fetching playlist {playlist_id}: {e}", file=sys.stderr)
            return []
    
    def calculate_match_score(self, track: Dict, params: Dict) -> float:
        """
        Calculate how well a track matches the target parameters
        
        Args:
            track: Deezer track object
            params: Target parameters from CV model
        
        Returns:
            Match score (0.0 to 1.0)
        """
        score = 0.0
        total_weight = 0.0
        
        # BPM/Tempo matching (weight: 3.0)
        track_bpm = track.get("bpm")
        target_tempo = params.get("target_tempo", 120)
        
        if track_bpm and track_bpm > 0:
            tempo_diff = abs(track_bpm - target_tempo)
            # Allow 20 BPM tolerance
            if tempo_diff <= 20:
                tempo_score = 1.0
            elif tempo_diff <= 40:
                tempo_score = 0.5
            else:
                tempo_score = max(0, 1 - (tempo_diff / 100))
            
            score += tempo_score * 3.0
            total_weight += 3.0
        
        # Duration matching (weight: 1.0)
        # Prefer songs between 2-6 minutes
        duration = track.get("duration", 0)
        if 120 <= duration <= 360:
            score += 1.0
            total_weight += 1.0
        elif duration > 0:
            score += 0.3
            total_weight += 1.0
        
        # Popularity/Rank (weight: 2.0)
        # Higher rank = more popular and generally better quality
        rank = track.get("rank", 0)
        if rank > 700000:
            score += 1.0 * 2.0
        elif rank > 500000:
            score += 0.8 * 2.0
        elif rank > 300000:
            score += 0.6 * 2.0
        elif rank > 100000:
            score += 0.4 * 2.0
        else:
            score += 0.2 * 2.0
        total_weight += 2.0
        
        return score / total_weight if total_weight > 0 else 0.0
    
    def filter_by_mood(self, track: Dict, params: Dict) -> bool:
        """
        Filter tracks by mood/valence using title/artist keywords
        
        Args:
            track: Deezer track object
            params: Target parameters
        
        Returns:
            True if track matches mood, False otherwise
        """
        title = track.get("title", "").lower()
        artist_name = track.get("artist", {}).get("name", "").lower()
        combined_text = f"{title} {artist_name}"
        
        target_valence = params.get("target_valence", 0.5)
        target_energy = params.get("target_energy", 0.5)
        
        # High valence (happy) - exclude sad songs
        if target_valence > 0.75:
            sad_keywords = ["sad", "cry", "tears", "hurt", "pain", "alone", "broken", "goodbye", "miss you"]
            if any(keyword in combined_text for keyword in sad_keywords):
                return False
        
        # Low valence (sad) - exclude very happy/party songs
        elif target_valence < 0.3:
            happy_keywords = ["party", "celebrate", "dance", "happy", "joy", "fun"]
            if any(keyword in combined_text for keyword in happy_keywords):
                return False
        
        # High energy - avoid explicit "sleep" or "lullaby" songs
        if target_energy > 0.7:
            low_energy_keywords = ["sleep", "lullaby", "meditation", "sleeping"]
            if any(keyword in combined_text for keyword in low_energy_keywords):
                return False
        
        # Low energy - avoid explicit "party" or "workout" songs
        elif target_energy < 0.3:
            high_energy_keywords = ["party", "workout", "pump", "rage", "hardcore"]
            if any(keyword in combined_text for keyword in high_energy_keywords):
                return False
        
        return True
    
    def _init_filter_log(self, params: Dict) -> str:
        """
        Initialize a log file for tracking the filtering process
        
        Args:
            params: Parameters dict for context
            
        Returns:
            Path to the log file
        """
        # Create history directory if it doesn't exist (relative to project root)
        history_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "history")
        os.makedirs(history_dir, exist_ok=True)
        
        # Generate timestamped log file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"filtering_log_{timestamp}.txt"
        log_path = os.path.join(history_dir, log_filename)
        
        # Open log file for writing
        self.log_file = open(log_path, 'w', encoding='utf-8')
        
        # Write header
        search_query = params.get("playlist_search_query", "N/A")
        self.log_file.write(f"Filtering Process Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log_file.write(f"Search Query: {search_query}\n")
        self.log_file.write(f"Target Tempo: {params.get('target_tempo', 'N/A')} BPM\n")
        self.log_file.write(f"Target Valence: {params.get('target_valence', 'N/A')}\n")
        self.log_file.write(f"Target Energy: {params.get('target_energy', 'N/A')}\n")
        self.log_file.write("=" * 80 + "\n\n")
        
        return log_path
    
    def _log_filter_result(self, track: Dict, score: float, passed: bool):
        """
        Log a song's filtering result
        
        Args:
            track: Track dictionary
            score: Match score calculated
            passed: Whether the track passed filtering
        """
        if self.log_file:
            title = track.get("title", "Unknown")
            artist = track.get("artist", {}).get("name", "Unknown")
            status = "PASSED" if passed else "FILTERED OUT"
            self.log_file.write(f"{status} | Score: {score:.3f} | {title} - {artist}\n")
    
    def _close_filter_log(self):
        """Close the filter log file"""
        if self.log_file:
            self.log_file.close()
            self.log_file = None
    
    def generate_playlist(self, params: Dict) -> Dict:
        """
        Main function: Generate filtered playlist based on parameters
        
        Args:
            params: JSON parameters from CV model containing:
                - playlist_search_query: Search query for playlists
                - target_tempo, target_valence, target_energy, etc.
                - limit: Number of tracks to return
        
        Returns:
            JSON object with filtered playlist
        """
        # Extract parameters
        search_query = params.get("playlist_search_query", "")
        target_limit = params.get("limit", 20)
        
        if not search_query:
            # Fallback: use seed_genres if no search query
            seed_genres = params.get("seed_genres", [])
            if seed_genres:
                search_query = " ".join(seed_genres[:2])
            else:
                search_query = "pop music"
        
        print(f"\n{'='*80}")
        print(f"[DEEZER] PLAYLIST GENERATOR")
        print(f"{'='*80}")
        print(f"Search Query: {search_query}")
        print(f"Target Tracks: {target_limit}")
        print(f"Target Tempo: {params.get('target_tempo', 'N/A')} BPM")
        print(f"Target Valence: {params.get('target_valence', 'N/A')}")
        print(f"Target Energy: {params.get('target_energy', 'N/A')}")
        print(f"{'='*80}\n")
        
        # Step 1: Search for playlists
        print("Step 1: Searching for playlists...")
        playlists = self.search_playlists(search_query, limit=3)
        
        if not playlists:
            return {
                "success": False,
                "error": "No playlists found",
                "tracks": []
            }
        
        # Step 2: Collect tracks from top 3 playlists
        print("\nStep 2: Collecting tracks from top 3 playlists...")
        all_tracks = []
        seen_track_ids = set()
        
        for i, playlist in enumerate(playlists[:3], 1):
            # Deezer API should always return an ID, but we guard against missing/None
            playlist_id = playlist.get("id")
            if playlist_id is None:
                print(f"  [{i}] Skipping playlist without ID: {playlist!r}", file=sys.stderr)
                continue

            playlist_id_str = str(playlist_id)
            playlist_title = playlist.get("title")
            print(f"  [{i}] Fetching from: {playlist_title} (ID: {playlist_id_str})")
            
            tracks = self.get_playlist_tracks(playlist_id_str)
            print(f"      → Found {len(tracks)} tracks")
            
            # Add unique tracks only
            for track in tracks:
                track_id = track.get("id")
                if track_id and track_id not in seen_track_ids:
                    all_tracks.append(track)
                    seen_track_ids.add(track_id)
        
        print(f"\n[OK] Total unique tracks collected: {len(all_tracks)}")
        
        # Initialize filtering log
        log_path = self._init_filter_log(params)
        print(f"[LOG] Filtering log: {log_path}")
        
        # Step 3: Filter and score tracks
        print("\nStep 3: Filtering tracks by parameters...")
        filtered_tracks = []
        
        for track in all_tracks:
            # Filter by mood
            if not self.filter_by_mood(track, params):
                # Calculate score even if filtered out, for logging
                score = self.calculate_match_score(track, params)
                self._log_filter_result(track, score, passed=False)
                continue
            
            # Calculate match score
            score = self.calculate_match_score(track, params)
            
            # Keep tracks with reasonable match score
            if score >= 0.3:  # Threshold
                track_info = {
                    "id": track.get("id"),
                    "title": track.get("title"),
                    "artist": track.get("artist", {}).get("name"),
                    "artist_id": track.get("artist", {}).get("id"),
                    "album": track.get("album", {}).get("title"),
                    "album_id": track.get("album", {}).get("id"),
                    "duration_seconds": track.get("duration"),
                    "duration_formatted": f"{track.get('duration', 0) // 60}:{track.get('duration', 0) % 60:02d}",
                    "bpm": track.get("bpm"),
                    "rank": track.get("rank"),
                    "preview_url": track.get("preview"),
                    "deezer_link": track.get("link"),
                    "match_score": round(score, 3)
                }
                filtered_tracks.append(track_info)
                self._log_filter_result(track, score, passed=True)
            else:
                # Track didn't meet minimum score threshold
                self._log_filter_result(track, score, passed=False)
        
        # Sort by match score (best matches first)
        filtered_tracks.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Limit to requested number
        final_tracks = filtered_tracks[:target_limit]
        
        # Write summary to log file
        if self.log_file:
            self.log_file.write("\n" + "=" * 80 + "\n")
            self.log_file.write(f"SUMMARY:\n")
            self.log_file.write(f"Total tracks analyzed: {len(all_tracks)}\n")
            self.log_file.write(f"Tracks passed filtering: {len(filtered_tracks)}\n")
            self.log_file.write(f"Tracks returned: {len(final_tracks)}\n")
            self.log_file.write("=" * 80 + "\n")
        
        print(f"[OK] Filtered to {len(filtered_tracks)} matching tracks")
        print(f"[OK] Returning top {len(final_tracks)} tracks")
        
        # Step 4: Build result JSON
        result = {
            "success": True,
            "metadata": {
                "search_query": search_query,
                "source_playlists_count": len(playlists),
                "total_tracks_analyzed": len(all_tracks),
                "tracks_after_filtering": len(filtered_tracks),
                "tracks_returned": len(final_tracks),
                "parameters": params
            },
            "playlist": final_tracks
        }
        
        # Print summary
        print(f"\n{'='*80}")
        print(f"[SUCCESS] PLAYLIST GENERATED SUCCESSFULLY")
        print(f"{'='*80}")
        if final_tracks:
            print(f"\nTop 5 tracks:")
            for i, track in enumerate(final_tracks[:5], 1):
                print(f"  {i}. {track['title']} - {track['artist']}")
                print(f"     BPM: {track['bpm']} | Score: {track['match_score']}")
        print(f"\n{'='*80}\n")
        
        # Close filter log
        self._close_filter_log()
        
        return result


