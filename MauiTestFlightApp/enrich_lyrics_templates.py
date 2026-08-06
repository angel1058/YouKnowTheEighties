import json

# Path to template catalogue file
templates_path = r'g:\My Drive\Develop\Binary\MauiTestFlightApp\wwwroot\data\question_templates_catalogue.json'

CATALOGUE = {
    # -------------------------------------------------------------------------
    # CAT 1: ARTIST & SONG MATCHING (NO POSITION FOCUS)
    # -------------------------------------------------------------------------
    "WHO_SANG_SONG": {
        "cat_id": 1,
        "name": "Who Sang This Song?",
        "templates": [
            "Who sang '{SongTitle}' when it stormed the UK charts on {ExactDate}?",
            "Which 80s artist released the hit single '{SongTitle}'?",
            "Who was the performing vocalist behind '{SongTitle}' on {ExactDate}?",
            "'{SongTitle}' was a huge hit on {ExactDate} - but who sang it?",
            "Which music act recorded the famous 80s track '{SongTitle}'?",
            "Who took '{SongTitle}' into the UK charts on {ExactDate}?",
            "Name the performing artist for '{SongTitle}' on {ExactDate}.",
            "Which iconic 80s singer or group gave us '{SongTitle}'?",
            "Who scored a massive chart hit with '{SongTitle}' on {ExactDate}?",
            "Whose distinctive vocals can be heard on '{SongTitle}' from {ExactDate}?"
        ]
    },
    "WHAT_SONG_DID_ARTIST_SING": {
        "cat_id": 1,
        "name": "What Song Did Artist Sing?",
        "templates": [
            "Which hit single did {Artist} perform on {ExactDate}?",
            "What song was {Artist} making waves with on {ExactDate}?",
            "Which classic track was released by {Artist} around {ExactDate}?",
            "What track did {Artist} take high into the UK charts on {ExactDate}?",
            "Which of these songs was recorded and released by {Artist}?",
            "Which famous 80s single belongs to {Artist} on {ExactDate}?",
            "What was the title of {Artist}'s chart entry on {ExactDate}?",
            "Which track on {ExactDate} brought fame to {Artist}?",
            "What song did {Artist} perform on Top of the Pops on {ExactDate}?",
            "Which hit single featured the musical talents of {Artist} on {ExactDate}?"
        ]
    },

    # -------------------------------------------------------------------------
    # CAT 2: SINGLE-POSITION CHART TOPPER & BAND
    # -------------------------------------------------------------------------
    "WHAT_SONG_WAS_NUMBER_ONE": {
        "cat_id": 2,
        "name": "What Song Was Number 1?",
        "templates": [
            "What song was the UK Number 1 single on {ExactDate}?",
            "Which track sat proudly atop the UK Official Chart on {ExactDate}?",
            "On {ExactDate}, which song ruled supreme at the top of the UK chart?",
            "What hit single occupied the coveted Number 1 spot on {ExactDate}?",
            "Which track was crowned official UK Number 1 on {ExactDate}?",
            "What song was being played as the UK Number 1 on {ExactDate}?",
            "Which single held the top spot in the UK Top 20 on {ExactDate}?",
            "What was the UK's best-selling single on {ExactDate}?",
            "On {ExactDate}, which track sat at Number 1 on Top of the Pops?",
            "Which chart-topping single was at Number 1 on {ExactDate}?"
        ]
    },
    "WHICH_BAND_HELD_TOP_SPOT": {
        "cat_id": 2,
        "name": "Which Band Held Top Spot?",
        "templates": [
            "Which group or artist held top spot on the UK charts on {ExactDate}?",
            "Who was ruling the UK chart at Number 1 on {ExactDate}?",
            "Which music act claimed the UK Number 1 position on {ExactDate}?",
            "On {ExactDate}, who sat at the very top of the UK Official Chart?",
            "Which artist or band had the Number 1 single on {ExactDate}?",
            "Who was king of the UK charts on {ExactDate} with a Number 1 hit?",
            "Which act held the Number 1 crown on {ExactDate}?",
            "Whose record was sitting at Number 1 in the UK on {ExactDate}?",
            "On {ExactDate}, who was celebrated as the UK chart topper?",
            "Which famous act held top spot on Top of the Pops on {ExactDate}?"
        ]
    },

    # -------------------------------------------------------------------------
    # CAT 3: RUNNER-UP & SHOWDOWN COMBINATIONS (#1 & #2)
    # -------------------------------------------------------------------------
    "WHO_STOPPED_ARTIST_GETTING_TO_NUMBER_ONE": {
        "cat_id": 3,
        "name": "Who Stopped Artist Getting to Number 1?",
        "templates": [
            "Who stopped {Num2Artist} getting to Number 1 on {ExactDate}?",
            "Which artist denied {Num2Artist} the top spot on {ExactDate}?",
            "On {ExactDate}, who kept {Num2Artist}'s '{Num2Song}' at Number 2?",
            "Which chart topper blocked {Num2Artist} from reaching Number 1 on {ExactDate}?",
            "Who stood in the way of {Num2Artist} hitting Number 1 on {ExactDate}?",
            "Which artist kept {Num2Artist} frustrated at Number 2 on {ExactDate}?",
            "Whose Number 1 single prevented {Num2Artist} from reaching the top on {ExactDate}?",
            "On {ExactDate}, who stopped {Num2Artist} claiming the Number 1 spot?",
            "Which act held off {Num2Artist} at Number 2 on {ExactDate}?",
            "Who thwarted {Num2Artist}'s chart-topping ambitions on {ExactDate}?"
        ]
    },
    "STUCK_AT_NUMBER_TWO": {
        "cat_id": 3,
        "name": "Stuck at Number 2",
        "templates": [
            "{Num1Artist} looked down from top spot onto which artist on {ExactDate}?",
            "When {Num1Artist} topped the charts on {ExactDate} with '{Num1Song}', who held second spot?",
            "Top of the Pops on {ExactDate} was {Num1Artist} with '{Num1Song}'. Who were they holding off in second spot?",
            "Who could not get to the top on {ExactDate} as {Num1Artist} held tight to Number 1 with '{Num1Song}'?",
            "Which artist was denied a Number 1 spot on {ExactDate} by {Num1Artist}?",
            "Which artist was stuck in the runner-up position on {ExactDate} while {Num1Artist} ruled the charts?",
            "Who sat in second spot looking up at {Num1Artist} on {ExactDate}?",
            "Which artist's chart assault was kept at Number 2 by {Num1Artist} on {ExactDate}?",
            "On {ExactDate}, who was forced to settle for Number 2 behind {Num1Artist}'s '{Num1Song}'?",
            "Whose chart-topping ambitions were thwarted at Number 2 by {Num1Artist} on {ExactDate}?"
        ]
    },
    "LOOKED_DOWN_ON_RUNNER_UP": {
        "cat_id": 3,
        "name": "Looked Down on Runner Up",
        "templates": [
            "Who looked down from Number 1 on {Num2Artist} stranded at Number 2 on {ExactDate}?",
            "Which artist held the top spot above {Num2Artist}'s '{Num2Song}' on {ExactDate}?",
            "Who was ruling at Number 1 while {Num2Artist} sat in second place on {ExactDate}?",
            "On {ExactDate}, which act occupied Number 1 above {Num2Artist} at Number 2?",
            "Who claimed the chart crown on {ExactDate}, keeping {Num2Artist} at Number 2?",
            "Which act was at Number 1 looking down at {Num2Artist} on {ExactDate}?",
            "Who was holding the Number 1 single above {Num2Artist} on {ExactDate}?",
            "On {ExactDate}, who kept {Num2Artist} in second spot while holding top spot?",
            "Which chart leader stood above {Num2Artist} on {ExactDate}?",
            "Who was sitting pretty at Number 1 on {ExactDate} while {Num2Artist} held Number 2?"
        ]
    },

    # -------------------------------------------------------------------------
    # CAT 4: PEAK POSITIONS & MID-CHART DEEP DIVES (POSITIONS 3 - 10)
    # -------------------------------------------------------------------------
    "WHO_PEAKED_AT_POS_ON_DATE": {
        "cat_id": 4,
        "name": "Who Peaked at Pos on Date?",
        "templates": [
            "Who reached Number {Pos} on {ExactDate} while {Num1Artist} held top spot?",
            "On {ExactDate}, which artist was charting at Number {Pos}?",
            "Which act occupied Number {Pos} on the UK chart on {ExactDate}?",
            "Who sat at Number {Pos} on {ExactDate} behind the chart leaders?",
            "Which artist claimed the Number {Pos} spot on {ExactDate}?",
            "On {ExactDate}, who reached Number {Pos} in the UK Top 10?",
            "Which song was sitting at Number {Pos} on {ExactDate}?",
            "Who reached a peak position of Number {Pos} on {ExactDate}?",
            "On {ExactDate}, which performer was at Number {Pos} on Top of the Pops?",
            "Which hit reached Number {Pos} on the UK Official Chart on {ExactDate}?"
        ]
    },

    # -------------------------------------------------------------------------
    # CAT 5: DETHRONED / REPLACEMENT & NEVER REACHED POSITION
    # -------------------------------------------------------------------------
    "WHO_KNOCKED_OFF_TOP_SPOT": {
        "cat_id": 5,
        "name": "Who Knocked Off Top Spot?",
        "templates": [
            "Who did {Num1Artist} knock off top spot on {ExactDate} with '{Num1Song}'?",
            "Which track was dethroned from Number 1 by {Num1Artist} on {ExactDate}?",
            "When {Num1Artist} reached Number 1 on {ExactDate}, which single did they replace at top spot?",
            "Who was ousted from the Number 1 crown by {Num1Artist} on {ExactDate}?",
            "Which artist lost their Number 1 spot to {Num1Artist} on {ExactDate}?",
            "Whose chart reign was ended by {Num1Artist} taking top spot on {ExactDate}?",
            "On {ExactDate}, who did {Num1Artist} replace at the top of the UK chart?",
            "Which song was knocked out of Number 1 by {Num1Artist} on {ExactDate}?",
            "Whose Number 1 run was cut short by {Num1Artist} on {ExactDate}?",
            "Who surrendered the top spot to {Num1Artist}'s '{Num1Song}' on {ExactDate}?"
        ]
    },
    "NEVER_GOT_ABOVE_POSITION": {
        "cat_id": 5,
        "name": "Never Got Above Position",
        "templates": [
            "Which of these famous 80s songs NEVER got to Number 1 in the UK?",
            "Which iconic 80s hit peaked in the Top 3 but NEVER reached top spot?",
            "Which of these tracks failed to ever hit the UK Number 1 spot?",
            "Which famous 80s single was denied a Number 1 peak during its run?",
            "Which of these songs peaked at Number 2 or #3 but NEVER hit Number 1?",
            "Which 80s classic never made it all the way to Number 1?",
            "Which of these hit singles never reached the peak Number 1 position?",
            "Which song among these choices never topped the UK Official Chart?",
            "Which famous 80s anthem missed out on reaching Number 1?",
            "Which of these tracks never achieved a UK Number 1 chart peak?"
        ]
    },

    # -------------------------------------------------------------------------
    # CAT 6: ENDURANCE & WEEKS IN CHART / RELATIVE ENDURANCE
    # -------------------------------------------------------------------------
    "WEEKS_IN_TOP_TEN": {
        "cat_id": 6,
        "name": "Weeks in Top 10",
        "templates": [
            "How many weeks did '{SongTitle}' by {Artist} remain in the UK Top 10?",
            "For how many total chart weeks did {Artist} stay in the Top 10 with '{SongTitle}'?",
            "What was the total Top 10 endurance (in weeks) for '{SongTitle}' by {Artist}?",
            "How many consecutive or total weeks was '{SongTitle}' in the Top 10?",
            "How many weeks did {Artist}'s '{SongTitle}' spend inside the UK Top 10?",
            "For how many weeks did '{SongTitle}' remain a Top 10 hit for {Artist}?",
            "How many chart weeks did '{SongTitle}' spend in the top ten?",
            "What was the duration (in weeks) of '{SongTitle}' inside the Top 10?",
            "How many weeks did {Artist} hold a Top 10 position with '{SongTitle}'?",
            "How many total weeks did '{SongTitle}' feature in the UK Top 10?"
        ]
    },

    # -------------------------------------------------------------------------
    # CAT 7: BAND MEMBER LINEUPS & FRUSTRATED LEAD VOCALISTS
    # -------------------------------------------------------------------------
    "IDENTIFY_BAND_BY_MEMBER": {
        "cat_id": 7,
        "name": "Identify Band By Member",
        "templates": [
            "Which band was {MemberName} a member of on {ExactDate}?",
            "On {ExactDate}, which group featured {MemberName} in their official lineup?",
            "Which 80s group included {MemberName} in their lineup on {ExactDate}?",
            "Which famous band had {MemberName} performing on {ExactDate}?",
            "On {ExactDate}, {MemberName} was part of which iconic 80s band?",
            "Which group's lineup featured {MemberName} on {ExactDate}?",
            "Which band did {MemberName} perform with on {ExactDate}?",
            "On {ExactDate}, {MemberName} played in which chart-topping band?",
            "Which 80s music group counted {MemberName} as a member on {ExactDate}?",
            "Who did {MemberName} perform alongside in a band on {ExactDate}?"
        ]
    },
    "LEAD_SINGER_BEHIND_NUMBER_ONE": {
        "cat_id": 7,
        "name": "Lead Singer Behind Number 1",
        "templates": [
            "While {Num1Artist} sat at Number 1 on {ExactDate}, who was the lead singer of the group waiting at Number 2?",
            "Who fronted the group occupying Number 2 right behind {Num1Artist} on {ExactDate}?",
            "Which lead vocalist was stuck at Number 2 on {ExactDate} while {Num1Artist} held top spot?",
            "Who was the lead singer of the band sitting in second place behind {Num1Artist} on {ExactDate}?",
            "On {ExactDate}, who led the vocals for the group at Number 2 behind {Num1Artist}?",
            "Which famous frontman was stranded at Number 2 behind {Num1Artist} on {ExactDate}?",
            "Who was lead singer for the runner-up band on {ExactDate} behind {Num1Artist}?",
            "Which lead singer was frustrated at Number 2 on {ExactDate} as {Num1Artist} ruled #1?",
            "Who fronted the band occupying 2nd place on {ExactDate} below {Num1Artist}?",
            "Which lead vocalist held the Number 2 spot behind {Num1Artist} on {ExactDate}?"
        ]
    },

    # -------------------------------------------------------------------------
    # CAT 8: BAND DEPARTURES & LINEUP CHANGES
    # -------------------------------------------------------------------------
    "BAND_DEPARTURES": {
        "cat_id": 8,
        "name": "Band Member Departures",
        "templates": [
            "Which prominent member left {BandName} in {Year}?",
            "In {Year}, which major member departed from {BandName}?",
            "Who left the lineup of {BandName} in {Year}?",
            "Which musician announced their exit from {BandName} in {Year}?",
            "Who quit {BandName} in {Year} to pursue a solo career or new projects?",
            "In {Year}, who departed from {BandName}'s famous lineup?",
            "Which key band member parted ways with {BandName} in {Year}?",
            "Who left {BandName} in {Year} after a string of hit singles?",
            "In {Year}, which member split from {BandName}?",
            "Who walked away from {BandName} in {Year}?"
        ]
    },

    # -------------------------------------------------------------------------
    # CAT 13: INSTRUMENTS & BAND ROLES
    # -------------------------------------------------------------------------
    "INSTRUMENT_PLAYED": {
        "cat_id": 13,
        "name": "Instrument Played by Member",
        "templates": [
            "What main instrument did {MemberName} play in {BandName}?",
            "Which instrument was {MemberName} famous for playing in {BandName}?",
            "In {BandName}, what role or instrument did {MemberName} handle?",
            "What did {MemberName} play in the lineup of {BandName}?",
            "Which instrument was handled by {MemberName} during his time in {BandName}?",
            "What was {MemberName}'s primary instrument in {BandName}?",
            "Which musical instrument did {MemberName} play for {BandName}?",
            "In {BandName}, what instrument did {MemberName} perform on stage?",
            "What instrument was {MemberName} credited with in {BandName}?",
            "Which role did {MemberName} fill in {BandName}?"
        ]
    },

    # -------------------------------------------------------------------------
    # CAT 7/LYRICS: FAIR-USE FIRST-LINE LYRIC CHALLENGES (PREMIUM PAYWALL TEMPTER)
    # -------------------------------------------------------------------------
    "FIRST_LINE_LYRIC_CHALLENGE": {
        "cat_id": 7,
        "name": "First Line Lyric Challenge",
        "templates": [
            "Which 80s hit single begins with the famous line: '{LyricSnippet}'?",
            "'{LyricSnippet}' is the opening line to which iconic 80s track?",
            "Which 80s chart topper starts with the lyrics: '{LyricSnippet}'?",
            "Can you identify the song that opens with: '{LyricSnippet}'?",
            "Which classic 80s song features the opening line: '{LyricSnippet}'?",
            "Which hit single opens with these words: '{LyricSnippet}'?",
            "Name the 80s track that begins with: '{LyricSnippet}'.",
            "Which song starts with the famous lyrics: '{LyricSnippet}'?",
            "'{LyricSnippet}' - which 80s anthem starts with this line?",
            "Which famous 80s hit begins with: '{LyricSnippet}'?"
        ]
    }
}

# Write JSON Catalogue File
with open(templates_path, 'w', encoding='utf-8') as f:
    json.dump(CATALOGUE, f, indent=2)

print(f"Successfully created question_templates_catalogue.json with {len(CATALOGUE)} logic categories!")
