import os
from pymediainfo import MediaInfo

#How to Use
#Install dependencies (if not done already):

#1-run :pip install pymediainfo

#2-Save the script as rename_series.py.

#3-Open file path on CMD

#4-Run :python rename_series.py

episode_names = {
    1: [
        "Winter Is Coming", "The Kingsroad", "Lord Snow", 
        "Cripples, Bastards, and Broken Things", "The Wolf and the Lion", 
        "A Golden Crown", "You Win or You Die", "The Pointy End", 
        "Baelor", "Fire and Blood"
    ],
    2: [
        "The North Remembers", "The Night Lands", "What Is Dead May Never Die", 
        "Garden of Bones", "The Ghost of Harrenhal", "The Old Gods and the New", 
        "A Man Without Honor", "The Prince of Winterfell", "Blackwater", 
        "Valar Morghulis"
    ],
    3: [
        "Valar Dohaeris", "Dark Wings, Dark Words", "Walk of Punishment", 
        "And Now His Watch Is Ended", "Kissed by Fire", "The Climb", 
        "The Bear and the Maiden Fair", "Second Sons", "The Rains of Castamere", 
        "Mhysa"
    ],
    4: [
        "Two Swords", "The Lion and the Rose", "Breaker of Chains", 
        "Oathkeeper", "First of His Name", "The Laws of Gods and Men", 
        "Mockingbird", "The Mountain and the Viper", "The Watchers on the Wall", 
        "The Children"
    ],
    5: [
        "The Wars to Come", "The House of Black and White", "High Sparrow", 
        "Sons of the Harpy", "Kill the Boy", "Unbowed, Unbent, Unbroken", 
        "The Gift", "Hardhome", "The Dance of Dragons", "Mother's Mercy"
    ],
    6: [
        "The Red Woman", "Home", "Oathbreaker", "Book of the Stranger", 
        "The Door", "Blood of My Blood", "The Broken Man", "No One", 
        "Battle of the Bastards", "The Winds of Winter"
    ],
    7: [
        "Dragonstone", "Stormborn", "The Queen's Justice", "The Spoils of War", 
        "Eastwatch", "Beyond the Wall", "The Dragon and the Wolf"
    ],
    8: [
        "Winterfell", "A Knight of the Seven Kingdoms", "The Long Night", 
        "The Last of the Starks", "The Bells", "The Iron Throne"
    ]
}

def detect_quality(file_path):
    """Detects if video is 360p, 480p, or 720p"""
    try:
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            if track.track_type == "Video":
                height = int(track.height)
                if height >= 720:
                    return "720p"
                elif height >= 480:
                    return "480p"
                elif height >= 360:
                    return "360p"
                else:
                    return f"{height}p"  # Fallback (e.g., 240p)
        return "Unknown"
    except:
        return "Unknown"

def rename_episodes(base_dir):
    for season in range(1, 9):
        season_dir = os.path.join(base_dir, f"season {season}")
        if not os.path.exists(season_dir):
            continue
            
        print(f"\nProcessing Season {season}...")
        episodes = episode_names[season]
        
        for ep_num, ep_name in enumerate(episodes, 1):
            old_file = os.path.join(season_dir, f"{ep_num}.mp4")
            if not os.path.exists(old_file):
                print(f"⚠️ Missing: S{season}E{ep_num}")
                continue
                
            quality = detect_quality(old_file)
            new_name = f"S{season:02d}E{ep_num:02d} - {ep_name} [{quality}].mp4"
            new_file = os.path.join(season_dir, new_name)
            
            try:
                os.rename(old_file, new_file)
                print(f"✅ Renamed: {new_name}")
            except Exception as e:
                print(f"❌ Failed to rename {old_file}: {e}")

if __name__ == "__main__":
    base_directory = input("Enter the directory path: ")
    rename_episodes(base_directory)
    print("\n🎉 All episodes renamed with detected quality!")