import json
import re

# Load 80s chart dataset
json_path = r'g:\My Drive\Develop\Binary\MauiTestFlightApp\wwwroot\data\charts_80s_top20_compressed.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data['songs'])} songs.")

# Comprehensive 80s Artist Database: Lead Singers, Band Members (with active dates & roles), and Consensus Genres
ARTIST_DB = {
    # Synth-pop / New Wave Giants
    "DURAN DURAN": {
        "genre": ["Synth-pop", "New Wave"],
        "leadSinger": "Simon Le Bon",
        "members": [
            {"name": "Simon Le Bon", "role": "Lead Singer", "start": 1980, "end": None},
            {"name": "Nick Rhodes", "role": "Keyboards", "start": 1978, "end": None},
            {"name": "John Taylor", "role": "Bass", "start": 1978, "end": None},
            {"name": "Andy Taylor", "role": "Guitar", "start": 1980, "end": 1986},
            {"name": "Roger Taylor", "role": "Drums", "start": 1979, "end": 1985}
        ]
    },
    "DEPECHE MODE": {
        "genre": ["Synth-pop", "New Wave"],
        "leadSinger": "Dave Gahan",
        "members": [
            {"name": "Dave Gahan", "role": "Lead Singer", "start": 1980, "end": None},
            {"name": "Martin Gore", "role": "Keyboards & Guitar", "start": 1980, "end": None},
            {"name": "Andrew Fletcher", "role": "Keyboards", "start": 1980, "end": 2022},
            {"name": "Vince Clarke", "role": "Keyboards & Chief Songwriter", "start": 1980, "end": 1981},
            {"name": "Alan Wilder", "role": "Keyboards & Drums", "start": 1982, "end": 1995}
        ]
    },
    "WHAM!": {
        "genre": ["Pop", "Dance-pop"],
        "leadSinger": "George Michael",
        "members": [
            {"name": "George Michael", "role": "Lead Singer & Songwriter", "start": 1981, "end": 1986},
            {"name": "Andrew Ridgeley", "role": "Guitar & Backing Vocals", "start": 1981, "end": 1986},
            {"name": "Shirlie Holliman", "role": "Backing Singer", "start": 1982, "end": 1986},
            {"name": "Dee C. Lee", "role": "Backing Singer", "start": 1982, "end": 1983},
            {"name": "Pepsi DeMacque", "role": "Backing Singer", "start": 1983, "end": 1986}
        ]
    },
    "QUEEN": {
        "genre": ["Rock", "Arena Rock"],
        "leadSinger": "Freddie Mercury",
        "members": [
            {"name": "Freddie Mercury", "role": "Lead Singer & Piano", "start": 1970, "end": 1991},
            {"name": "Brian May", "role": "Lead Guitar & Vocals", "start": 1970, "end": None},
            {"name": "Roger Taylor", "role": "Drums & Vocals", "start": 1970, "end": None},
            {"name": "John Deacon", "role": "Bass Guitar", "start": 1971, "end": 1997}
        ]
    },
    "THE POLICE": {
        "genre": ["New Wave", "Reggae-Rock"],
        "leadSinger": "Sting",
        "members": [
            {"name": "Sting", "role": "Lead Singer & Bass", "start": 1977, "end": 1986},
            {"name": "Andy Summers", "role": "Guitar", "start": 1977, "end": 1986},
            {"name": "Stewart Copeland", "role": "Drums", "start": 1977, "end": 1986}
        ]
    },
    "CULTURE CLUB": {
        "genre": ["New Wave", "Pop", "Blue-Eyed Soul"],
        "leadSinger": "Boy George",
        "members": [
            {"name": "Boy George", "role": "Lead Singer", "start": 1981, "end": 1986},
            {"name": "Roy Hay", "role": "Guitar & Keyboards", "start": 1981, "end": 1986},
            {"name": "Mikey Craig", "role": "Bass", "start": 1981, "end": 1986},
            {"name": "Jon Moss", "role": "Drums", "start": 1981, "end": 1986}
        ]
    },
    "SPANDAU BALLET": {
        "genre": ["New Romantic", "Synth-pop"],
        "leadSinger": "Tony Hadley",
        "members": [
            {"name": "Tony Hadley", "role": "Lead Singer", "start": 1979, "end": 1990},
            {"name": "Gary Kemp", "role": "Guitar & Songwriter", "start": 1979, "end": 1990},
            {"name": "Martin Kemp", "role": "Bass", "start": 1979, "end": 1990},
            {"name": "Steve Norman", "role": "Saxophone & Percussion", "start": 1979, "end": 1990},
            {"name": "John Keeble", "role": "Drums", "start": 1979, "end": 1990}
        ]
    },
    "TEARS FOR FEARS": {
        "genre": ["Synth-pop", "New Wave"],
        "leadSinger": "Roland Orzabal",
        "members": [
            {"name": "Roland Orzabal", "role": "Lead Singer & Guitar", "start": 1981, "end": None},
            {"name": "Curt Smith", "role": "Co-Lead Singer & Bass", "start": 1981, "end": 1991},
            {"name": "Manny Elias", "role": "Drums", "start": 1981, "end": 1986},
            {"name": "Ian Stanley", "role": "Keyboards", "start": 1981, "end": 1987}
        ]
    },
    "EURYTHMICS": {
        "genre": ["Synth-pop", "New Wave"],
        "leadSinger": "Annie Lennox",
        "members": [
            {"name": "Annie Lennox", "role": "Lead Singer", "start": 1980, "end": 1990},
            {"name": "Dave Stewart", "role": "Guitar, Keyboards & Producer", "start": 1980, "end": 1990}
        ]
    },
    "THE HUMAN LEAGUE": {
        "genre": ["Synth-pop", "New Wave"],
        "leadSinger": "Philip Oakey",
        "members": [
            {"name": "Philip Oakey", "role": "Lead Singer", "start": 1977, "end": None},
            {"name": "Joanne Catherall", "role": "Vocals", "start": 1980, "end": None},
            {"name": "Susan Ann Sulley", "role": "Vocals", "start": 1980, "end": None},
            {"name": "Ian Burden", "role": "Keyboards & Bass", "start": 1981, "end": 1987},
            {"name": "Jo Callis", "role": "Keyboards & Guitar", "start": 1981, "end": 1985},
            {"name": "Martyn Ware", "role": "Keyboards", "start": 1977, "end": 1980},
            {"name": "Ian Craig Marsh", "role": "Keyboards", "start": 1977, "end": 1980}
        ]
    },
    "SOFT CELL": {
        "genre": ["Synth-pop", "New Wave"],
        "leadSinger": "Marc Almond",
        "members": [
            {"name": "Marc Almond", "role": "Lead Singer", "start": 1978, "end": 1984},
            {"name": "Dave Ball", "role": "Synthesizers", "start": 1978, "end": 1984}
        ]
    },
    "ULTRAVOX": {
        "genre": ["Synth-pop", "New Wave"],
        "leadSinger": "Midge Ure",
        "members": [
            {"name": "Midge Ure", "role": "Lead Singer & Guitar", "start": 1979, "end": 1987},
            {"name": "Billy Currie", "role": "Keyboards & Violin", "start": 1974, "end": 1987},
            {"name": "Chris Cross", "role": "Bass & Synthesizers", "start": 1974, "end": 1987},
            {"name": "Warren Cann", "role": "Drums", "start": 1974, "end": 1986},
            {"name": "John Foxx", "role": "Lead Singer", "start": 1974, "end": 1979}
        ]
    },
    "A-HA": {
        "genre": ["Synth-pop", "Pop Rock"],
        "leadSinger": "Morten Harket",
        "members": [
            {"name": "Morten Harket", "role": "Lead Singer", "start": 1982, "end": None},
            {"name": "Magne Furuholmen", "role": "Keyboards & Guitar", "start": 1982, "end": None},
            {"name": "Paul Waaktaar-Savoy", "role": "Guitar & Songwriter", "start": 1982, "end": None}
        ]
    },
    "PET SHOP BOYS": {
        "genre": ["Synth-pop", "Hi-NRG"],
        "leadSinger": "Neil Tennant",
        "members": [
            {"name": "Neil Tennant", "role": "Lead Singer", "start": 1981, "end": None},
            {"name": "Chris Lowe", "role": "Keyboards & Synthesizers", "start": 1981, "end": None}
        ]
    },
    "ERASURE": {
        "genre": ["Synth-pop", "Hi-NRG"],
        "leadSinger": "Andy Bell",
        "members": [
            {"name": "Andy Bell", "role": "Lead Singer", "start": 1985, "end": None},
            {"name": "Vince Clarke", "role": "Synthesizers & Chief Songwriter", "start": 1985, "end": None}
        ]
    },
    "YAZOO": {
        "genre": ["Synth-pop", "New Wave"],
        "leadSinger": "Alison Moyet",
        "members": [
            {"name": "Alison Moyet", "role": "Lead Singer", "start": 1981, "end": 1983},
            {"name": "Vince Clarke", "role": "Synthesizers", "start": 1981, "end": 1983}
        ]
    },
    "FRANKIE GOES TO HOLLYWOOD": {
        "genre": ["Synth-pop", "Dance-pop", "Hi-NRG"],
        "leadSinger": "Holly Johnson",
        "members": [
            {"name": "Holly Johnson", "role": "Lead Singer", "start": 1980, "end": 1987},
            {"name": "Paul Rutherford", "role": "Backing Vocals & Dancing", "start": 1980, "end": 1987},
            {"name": "Brian Nash", "role": "Guitar", "start": 1980, "end": 1987},
            {"name": "Mark O'Toole", "role": "Bass", "start": 1980, "end": 1987},
            {"name": "Peter Gill", "role": "Drums", "start": 1980, "end": 1987}
        ]
    },
    "SIMPLE MINDS": {
        "genre": ["Post-Punk", "Synth-pop", "Arena Rock"],
        "leadSinger": "Jim Kerr",
        "members": [
            {"name": "Jim Kerr", "role": "Lead Singer", "start": 1977, "end": None},
            {"name": "Charlie Burchill", "role": "Guitar & Keyboards", "start": 1977, "end": None},
            {"name": "Mick MacNeil", "role": "Keyboards", "start": 1978, "end": 1990},
            {"name": "Derek Forbes", "role": "Bass", "start": 1978, "end": 1985},
            {"name": "Brian McGee", "role": "Drums", "start": 1977, "end": 1981},
            {"name": "Mel Gaynor", "role": "Drums", "start": 1982, "end": 1991}
        ]
    },
    "MADNESS": {
        "genre": ["Ska", "2 Tone", "Pop"],
        "leadSinger": "Suggs",
        "members": [
            {"name": "Suggs", "role": "Lead Singer", "start": 1977, "end": 1986},
            {"name": "Mike Barson", "role": "Keyboards", "start": 1976, "end": 1984},
            {"name": "Chris Foreman", "role": "Guitar", "start": 1976, "end": 1986},
            {"name": "Mark Bedford", "role": "Bass", "start": 1978, "end": 1986},
            {"name": "Lee Thompson", "role": "Saxophone", "start": 1976, "end": 1986},
            {"name": "Daniel Woodgate", "role": "Drums", "start": 1978, "end": 1986},
            {"name": "Chas Smash", "role": "Backing Vocals & Trumpet", "start": 1979, "end": 1986}
        ]
    },
    "UB40": {
        "genre": ["Reggae", "Dub", "Pop"],
        "leadSinger": "Ali Campbell",
        "members": [
            {"name": "Ali Campbell", "role": "Lead Singer & Rhythm Guitar", "start": 1978, "end": 2008},
            {"name": "Robin Campbell", "role": "Guitar & Vocals", "start": 1978, "end": None},
            {"name": "Astro", "role": "Toasting & Percussion", "start": 1979, "end": 2013},
            {"name": "Mickey Virtue", "role": "Keyboards", "start": 1979, "end": 2008},
            {"name": "Brian Travers", "role": "Saxophone", "start": 1978, "end": 2021},
            {"name": "Earl Falconer", "role": "Bass", "start": 1978, "end": None},
            {"name": "James Brown", "role": "Drums", "start": 1978, "end": None},
            {"name": "Norman Hassan", "role": "Percussion & Trombone", "start": 1978, "end": None}
        ]
    },
    "IRON MAIDEN": {
        "genre": ["Heavy Metal", "NWOBHM"],
        "leadSinger": "Bruce Dickinson",
        "members": [
            {"name": "Bruce Dickinson", "role": "Lead Singer", "start": 1981, "end": 1993},
            {"name": "Paul Di'Anno", "role": "Lead Singer", "start": 1978, "end": 1981},
            {"name": "Steve Harris", "role": "Bass & Chief Songwriter", "start": 1975, "end": None},
            {"name": "Dave Murray", "role": "Guitar", "start": 1976, "end": None},
            {"name": "Adrian Smith", "role": "Guitar", "start": 1980, "end": 1990},
            {"name": "Clive Burr", "role": "Drums", "start": 1979, "end": 1982},
            {"name": "Nicko McBrain", "role": "Drums", "start": 1982, "end": None}
        ]
    },
    "FLEETWOOD MAC": {
        "genre": ["Pop Rock", "Soft Rock"],
        "leadSinger": "Stevie Nicks",
        "members": [
            {"name": "Stevie Nicks", "role": "Lead Singer", "start": 1975, "end": 1991},
            {"name": "Lindsey Buckingham", "role": "Lead Guitar & Vocals", "start": 1975, "end": 1987},
            {"name": "Christine McVie", "role": "Lead Singer & Keyboards", "start": 1970, "end": 1998},
            {"name": "John McVie", "role": "Bass", "start": 1967, "end": None},
            {"name": "Mick Fleetwood", "role": "Drums", "start": 1967, "end": None}
        ]
    },
    "KAJAGOOGOO": {
        "genre": ["Synth-pop", "New Wave"],
        "leadSinger": "Limahl",
        "members": [
            {"name": "Limahl", "role": "Lead Singer", "start": 1981, "end": 1983},
            {"name": "Nick Beggs", "role": "Bass & Chapman Stick / Lead Singer", "start": 1981, "end": 1985},
            {"name": "Steve Askew", "role": "Guitar", "start": 1981, "end": 1985},
            {"name": "Stuart Neale", "role": "Keyboards", "start": 1981, "end": 1985},
            {"name": "Jez Strode", "role": "Drums", "start": 1981, "end": 1984}
        ]
    },
    "HAIRCUT 100": {
        "genre": ["New Wave", "Funk-pop"],
        "leadSinger": "Nick Heyward",
        "members": [
            {"name": "Nick Heyward", "role": "Lead Singer & Guitar", "start": 1980, "end": 1983},
            {"name": "Les Nemes", "role": "Bass", "start": 1980, "end": 1984},
            {"name": "Graham Jones", "role": "Guitar", "start": 1980, "end": 1984},
            {"name": "Blair Cunningham", "role": "Drums", "start": 1981, "end": 1984},
            {"name": "Phil Smith", "role": "Saxophone", "start": 1981, "end": 1984}
        ]
    },
    "ABC": {
        "genre": ["Synth-pop", "New Wave", "Sophisti-pop"],
        "leadSinger": "Martin Fry",
        "members": [
            {"name": "Martin Fry", "role": "Lead Singer", "start": 1980, "end": None},
            {"name": "Mark White", "role": "Guitar & Keyboards", "start": 1980, "end": 1992},
            {"name": "Stephen Singleton", "role": "Saxophone", "start": 1980, "end": 1984},
            {"name": "David Palmer", "role": "Drums", "start": 1982, "end": 1983}
        ]
    },
    "ECHO & THE BUNNYMEN": {
        "genre": ["Post-Punk", "Neo-Psychedelia"],
        "leadSinger": "Ian McCulloch",
        "members": [
            {"name": "Ian McCulloch", "role": "Lead Singer", "start": 1978, "end": 1988},
            {"name": "Will Sergeant", "role": "Lead Guitar", "start": 1978, "end": None},
            {"name": "Les Pattinson", "role": "Bass", "start": 1978, "end": 1998},
            {"name": "Pete de Freitas", "role": "Drums", "start": 1979, "end": 1989}
        ]
    },
    "BANANARAMA": {
        "genre": ["Pop", "Dance-pop", "Hi-NRG"],
        "leadSinger": "Bananarama",
        "members": [
            {"name": "Sara Dallin", "role": "Vocals", "start": 1981, "end": None},
            {"name": "Keren Woodward", "role": "Vocals", "start": 1981, "end": None},
            {"name": "Siobhan Fahey", "role": "Vocals", "start": 1981, "end": 1988},
            {"name": "Jacquie O'Sullivan", "role": "Vocals", "start": 1988, "end": 1991}
        ]
    },
    "THE JAM": {
        "genre": ["Mod Revival", "Punk Rock"],
        "leadSinger": "Paul Weller",
        "members": [
            {"name": "Paul Weller", "role": "Lead Singer & Guitar", "start": 1972, "end": 1982},
            {"name": "Bruce Foxton", "role": "Bass & Vocals", "start": 1974, "end": 1982},
            {"name": "Rick Buckler", "role": "Drums", "start": 1972, "end": 1982}
        ]
    },
    "THE SPECIALS": {
        "genre": ["2 Tone", "Ska"],
        "leadSinger": "Terry Hall",
        "members": [
            {"name": "Terry Hall", "role": "Lead Singer", "start": 1977, "end": 1981},
            {"name": "Neville Staple", "role": "Vocals & Toasting", "start": 1978, "end": 1981},
            {"name": "Jerry Dammers", "role": "Keyboards & Songwriter", "start": 1977, "end": 1984},
            {"name": "Lynval Golding", "role": "Rhythm Guitar & Vocals", "start": 1977, "end": 1984},
            {"name": "Roddy Radiation", "role": "Lead Guitar", "start": 1978, "end": 1981},
            {"name": "Horace Panter", "role": "Bass", "start": 1977, "end": 1984},
            {"name": "John Bradbury", "role": "Drums", "start": 1979, "end": 1984}
        ]
    },
    "THE CLASH": {
        "genre": ["Punk Rock", "Post-Punk", "Ska-Punk"],
        "leadSinger": "Joe Strummer",
        "members": [
            {"name": "Joe Strummer", "role": "Lead Singer & Rhythm Guitar", "start": 1976, "end": 1986},
            {"name": "Mick Jones", "role": "Lead Guitar & Vocals", "start": 1976, "end": 1983},
            {"name": "Paul Simonon", "role": "Bass", "start": 1976, "end": 1986},
            {"name": "Topper Headon", "role": "Drums", "start": 1977, "end": 1982}
        ]
    },
    "DIRE STRAITS": {
        "genre": ["Roots Rock", "Pub Rock"],
        "leadSinger": "Mark Knopfler",
        "members": [
            {"name": "Mark Knopfler", "role": "Lead Singer & Lead Guitar", "start": 1977, "end": 1995},
            {"name": "John Illsley", "role": "Bass & Vocals", "start": 1977, "end": 1995},
            {"name": "David Knopfler", "role": "Rhythm Guitar", "start": 1977, "end": 1980},
            {"name": "Pick Withers", "role": "Drums", "start": 1977, "end": 1982},
            {"name": "Alan Clark", "role": "Keyboards", "start": 1980, "end": 1995},
            {"name": "Hal Lindes", "role": "Rhythm Guitar", "start": 1980, "end": 1985},
            {"name": "Terry Williams", "role": "Drums", "start": 1982, "end": 1988}
        ]
    },
    "BLONDIE": {
        "genre": ["New Wave", "Pop Rock", "Disco"],
        "leadSinger": "Debbie Harry",
        "members": [
            {"name": "Debbie Harry", "role": "Lead Singer", "start": 1974, "end": 1982},
            {"name": "Chris Stein", "role": "Guitar", "start": 1974, "end": 1982},
            {"name": "Clem Burke", "role": "Drums", "start": 1975, "end": 1982},
            {"name": "Jimmy Destri", "role": "Keyboards", "start": 1975, "end": 1982},
            {"name": "Nigel Harrison", "role": "Bass", "start": 1977, "end": 1982},
            {"name": "Frank Infante", "role": "Guitar", "start": 1977, "end": 1982}
        ]
    },
    "ABBA": {
        "genre": ["Pop", "Euro-pop", "Disco"],
        "leadSinger": "Agnetha Fältskog & Anni-Frid Lyngstad",
        "members": [
            {"name": "Agnetha Fältskog", "role": "Lead Singer", "start": 1972, "end": 1982},
            {"name": "Anni-Frid Lyngstad", "role": "Lead Singer", "start": 1972, "end": 1982},
            {"name": "Björn Ulvaeus", "role": "Guitar & Songwriter", "start": 1972, "end": 1982},
            {"name": "Benny Andersson", "role": "Keyboards & Songwriter", "start": 1972, "end": 1982}
        ]
    },
    "GENESIS": {
        "genre": ["Pop Rock", "Progressive Rock"],
        "leadSinger": "Phil Collins",
        "members": [
            {"name": "Phil Collins", "role": "Lead Singer & Drums", "start": 1970, "end": 1996},
            {"name": "Tony Banks", "role": "Keyboards", "start": 1967, "end": 1998},
            {"name": "Mike Rutherford", "role": "Bass & Guitar", "start": 1967, "end": 1998},
            {"name": "Daryl Stuermer", "role": "Touring Guitar & Bass", "start": 1978, "end": None},
            {"name": "Chester Thompson", "role": "Touring Drums", "start": 1977, "end": 1992}
        ]
    },
    "DEXYS MIDNIGHT RUNNERS": {
        "genre": ["Celtic Soul", "New Wave"],
        "leadSinger": "Kevin Rowland",
        "members": [
            {"name": "Kevin Rowland", "role": "Lead Singer", "start": 1978, "end": 1987},
            {"name": "Big Jim Paterson", "role": "Trombone", "start": 1978, "end": 1982},
            {"name": "Pete Williams", "role": "Bass", "start": 1978, "end": 1980},
            {"name": "Steve Spooner", "role": "Alto Sax", "start": 1978, "end": 1980}
        ]
    },
    "THE STYLE COUNCIL": {
        "genre": ["Sophisti-pop", "Blue-Eyed Soul"],
        "leadSinger": "Paul Weller",
        "members": [
            {"name": "Paul Weller", "role": "Lead Singer & Guitar", "start": 1983, "end": 1989},
            {"name": "Mick Talbot", "role": "Keyboards", "start": 1983, "end": 1989},
            {"name": "Dee C. Lee", "role": "Vocals", "start": 1984, "end": 1989},
            {"name": "Steve White", "role": "Drums", "start": 1983, "end": 1989}
        ]
    },
    "THE CURE": {
        "genre": ["Goth Rock", "Post-Punk", "Synth-pop"],
        "leadSinger": "Robert Smith",
        "members": [
            {"name": "Robert Smith", "role": "Lead Singer & Guitar", "start": 1978, "end": None},
            {"name": "Simon Gallup", "role": "Bass", "start": 1979, "end": 1982},
            {"name": "Lol Tolhurst", "role": "Drums & Keyboards", "start": 1978, "end": 1989},
            {"name": "Porl Thompson", "role": "Guitar & Keyboards", "start": 1983, "end": 1993},
            {"name": "Boris Williams", "role": "Drums", "start": 1984, "end": 1994}
        ]
    },
    "U2": {
        "genre": ["Post-Punk", "Arena Rock"],
        "leadSinger": "Bono",
        "members": [
            {"name": "Bono", "role": "Lead Singer", "start": 1976, "end": None},
            {"name": "The Edge", "role": "Lead Guitar & Keyboards", "start": 1976, "end": None},
            {"name": "Adam Clayton", "role": "Bass", "start": 1976, "end": None},
            {"name": "Larry Mullen Jr.", "role": "Drums", "start": 1976, "end": None}
        ]
    },
    "AC/DC": {
        "genre": ["Hard Rock", "Heavy Metal"],
        "leadSinger": "Brian Johnson",
        "members": [
            {"name": "Brian Johnson", "role": "Lead Singer", "start": 1980, "end": 2016},
            {"name": "Bon Scott", "role": "Lead Singer", "start": 1974, "end": 1980},
            {"name": "Angus Young", "role": "Lead Guitar", "start": 1973, "end": None},
            {"name": "Malcolm Young", "role": "Rhythm Guitar", "start": 1973, "end": 2014},
            {"name": "Cliff Williams", "role": "Bass", "start": 1977, "end": 2016},
            {"name": "Phil Rudd", "role": "Drums", "start": 1975, "end": 1983}
        ]
    },
    "STATUS QUO": {
        "genre": ["Boogie Rock", "Hard Rock"],
        "leadSinger": "Francis Rossi & Rick Parfitt",
        "members": [
            {"name": "Francis Rossi", "role": "Lead Singer & Guitar", "start": 1967, "end": None},
            {"name": "Rick Parfitt", "role": "Lead Singer & Rhythm Guitar", "start": 1967, "end": 2016},
            {"name": "Alan Lancaster", "role": "Bass & Vocals", "start": 1967, "end": 1985},
            {"name": "John Coghlan", "role": "Drums", "start": 1967, "end": 1981},
            {"name": "Andy Bown", "role": "Keyboards", "start": 1976, "end": None}
        ]
    },
    "ROXY MUSIC": {
        "genre": ["Art Rock", "Glam Rock", "New Wave"],
        "leadSinger": "Bryan Ferry",
        "members": [
            {"name": "Bryan Ferry", "role": "Lead Singer & Keyboards", "start": 1970, "end": 1983},
            {"name": "Phil Manzanera", "role": "Lead Guitar", "start": 1972, "end": 1983},
            {"name": "Andy Mackay", "role": "Oboe & Saxophone", "start": 1970, "end": 1983},
            {"name": "Paul Thompson", "role": "Drums", "start": 1971, "end": 1980}
        ]
    },
    "GARY NUMAN": {
        "genre": ["Synth-pop", "Industrial"],
        "leadSinger": "Gary Numan",
        "members": [
            {"name": "Gary Numan", "role": "Lead Singer & Synthesizers", "start": 1977, "end": None}
        ]
    },
    "PAUL YOUNG": {
        "genre": ["Blue-Eyed Soul", "Pop"],
        "leadSinger": "Paul Young",
        "members": [
            {"name": "Paul Young", "role": "Lead Singer", "start": 1982, "end": None}
        ]
    },
    "SONIA": {
        "genre": ["Pop", "Stock Aitken Waterman"],
        "leadSinger": "Sonia",
        "members": [
            {"name": "Sonia Evans", "role": "Lead Singer", "start": 1989, "end": None}
        ]
    },
    "KYLIE MINOGUE": {
        "genre": ["Pop", "Dance-pop", "Stock Aitken Waterman"],
        "leadSinger": "Kylie Minogue",
        "members": [
            {"name": "Kylie Minogue", "role": "Lead Singer", "start": 1987, "end": None}
        ]
    },
    "RICK ASTLEY": {
        "genre": ["Pop", "Blue-Eyed Soul", "Stock Aitken Waterman"],
        "leadSinger": "Rick Astley",
        "members": [
            {"name": "Rick Astley", "role": "Lead Singer", "start": 1987, "end": None}
        ]
    },
    "MICHAEL JACKSON": {
        "genre": ["Pop", "R&B", "Dance"],
        "leadSinger": "Michael Jackson",
        "members": [
            {"name": "Michael Jackson", "role": "Lead Singer & Performer", "start": 1964, "end": 2009}
        ]
    },
    "MADONNA": {
        "genre": ["Pop", "Dance-pop"],
        "leadSinger": "Madonna",
        "members": [
            {"name": "Madonna", "role": "Lead Singer & Performer", "start": 1982, "end": None}
        ]
    },
    "CLIFF RICHARD": {
        "genre": ["Pop", "Pop Rock"],
        "leadSinger": "Cliff Richard",
        "members": [
            {"name": "Cliff Richard", "role": "Lead Singer", "start": 1958, "end": None}
        ]
    },
    "SHAKIN' STEVENS": {
        "genre": ["Rockabilly", "Pop Rock"],
        "leadSinger": "Shakin' Stevens",
        "members": [
            {"name": "Shakin' Stevens", "role": "Lead Singer", "start": 1968, "end": None}
        ]
    }
}

# Generic Genre Fallbacks by Artist Keywords
GENRE_PATTERNS = [
    (r"SYNTH|OMD|VISAGE|CLASSIX|ORCHESTRAL MANOEUVRES|NEW MUSIK|BUGGLES|HEAVEN 17|BLANCMANGE|LOTUS EATERS|YELLO|KRAFTWERK|PROPELLERHEADS", ["Synth-pop", "New Wave"]),
    (r"HEAVY|METAL|SAXON|DEF LEPPARD|WHITESNAKE|MOTORHEAD|JUDAS PRIEST|MOTLEY CRUE|BON JOVI|GILLAN|RAINBOW|OZZY|BLACK SABBATH|MEAT LOAF", ["Hard Rock", "Heavy Metal"]),
    (r"SKA|BEAT|BAD MANNERS|SPECIAL AKA|SELECTER|PIRANHAS|SPLODGENESSABOUNDS", ["Ska", "2 Tone"]),
    (r"FUNK|DISCO|IMAGINATION|SHALAMAR|KOOL|GAP BAND|EARTH WIND|CHIC|ODYSSEY|FAT LARRY|DELEGATION|DETROIT SPINNERS|JUNIOR|REAL THING", ["Disco", "Funk", "Soul"]),
    (r"REGGEA|MARLEY|THIRD WORLD|MUSICAL YOUTH|MISTY|EDDY GRANT|PIGBAG", ["Reggae", "Ska"]),
]

# Enrich Songs
enriched_count = 0
for song in data['songs']:
    artist = song['a'].strip()
    artist_upper = artist.upper()

    if artist_upper in ARTIST_DB:
        db_entry = ARTIST_DB[artist_upper]
        song['g'] = db_entry['genre']
        song['ls'] = db_entry['leadSinger']
        if 'members' in db_entry:
            song['mb'] = db_entry['members']
        enriched_count += 1
    else:
        matched_genre = None
        for pattern, g_list in GENRE_PATTERNS:
            if re.search(pattern, artist_upper):
                matched_genre = g_list
                break
        
        if not matched_genre:
            matched_genre = ["Pop Rock", "80s Hits"]

        song['g'] = matched_genre
        song['ls'] = artist

# Save Enriched JSON
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'))

file_size_kb = round(len(json.dumps(data)) / 1024, 2)
print(f"Successfully enriched {len(data['songs'])} songs ({enriched_count} deep relational artist matches).")
print(f"Total Enriched JSON File Size: {file_size_kb} KB")
