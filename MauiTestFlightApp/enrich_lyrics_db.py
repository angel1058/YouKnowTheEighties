import json

json_path = r'g:\My Drive\Develop\Binary\MauiTestFlightApp\wwwroot\data\charts_80s_top20_compressed.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fair-use first line lyric snippets database for famous 80s hits
LYRICS_DB = {
    "RELAX": "Relax, don't do it, when you want to go to it...",
    "CARELESS WHISPER": "I feel so unsure as I take your hand and lead you to the dance floor...",
    "KARMA CHAMELEON": "Desert loving in your eyes all the way...",
    "TAKE ON ME": "We're talking away, I don't know what I'm to say...",
    "SWEET DREAMS (ARE MADE OF THIS)": "Sweet dreams are made of this, who am I to disagree...",
    "BLUE MONDAY": "How does it feel to treat me like you do...",
    "TAINTED LOVE": "Sometimes I feel I've got to run away, I've got to get away...",
    "VIENNA": "We walked in the cold air, freezing breath on a window pane...",
    "ASHES TO ASHES": "Do you remember a guy that's been in such an early song...",
    "DON'T YOU WANT ME": "You were working as a waitress in a cocktail bar...",
    "GOLD": "Thank you for coming home, I'm sorry that the chairs are all worn...",
    "TRUE": "So true, funny how it seems, always in time, but never in line for dreams...",
    "GHOSTBUSTERS": "If there's something strange in your neighborhood, who ya gonna call...",
    "INTO THE GROOVE": "And you can dance for inspiration, come on I'm waiting...",
    "LIKE A VIRGIN": "I made it through the wilderness, somehow I made it through...",
    "WAKE ME UP BEFORE YOU GO-GO": "Jitterbug, jitterbug, you put the boom-boom into my heart...",
    "NEVER GONNA GIVE YOU UP": "We're no strangers to love, you know the rules and so do I...",
    "YOU SPIN ME ROUND (LIKE A RECORD)": "If I, I get to know your name, well if I, could trace your private number...",
    "UNDER PRESSURE": "Pressure pushing down on me, pressing down on you...",
    "COME ON EILEEN": "Poor old Johnny Ray sounded sad upon the radio...",
    "WEST END GIRLS": "Sometimes you're better off dead, there's a gun in your hand...",
    "SHOUT": "Shout, shout, let it all out, these are the things I can do without...",
    "EVERYBODY WANTS TO RULE THE WORLD": "Welcome to your life, there's no turning back...",
    "TWO TRIBES": "When two tribes go to war, one is all that you can score...",
    "CALL ME": "Color me your color, baby, color me your car...",
    "WITH OR WITHOUT YOU": "See the stone set in your eyes, see the thorn twist in your side...",
    "LIVING ON A PRAYER": "Tommy used to work on the docks, union's been on strike...",
    "THE FINAL COUNTDOWN": "We're leaving together, but still it's farewell..."
}

lyric_matches = 0
for song in data['songs']:
    title_clean = song['t'].strip().upper()
    if title_clean in LYRICS_DB:
        song['ly'] = LYRICS_DB[title_clean]
        lyric_matches += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'))

file_size_kb = round(len(json.dumps(data)) / 1024, 2)
print(f"Injected {lyric_matches} iconic fair-use first line lyric snippets into dataset.")
print(f"Total Enriched JSON Size: {file_size_kb} KB")
