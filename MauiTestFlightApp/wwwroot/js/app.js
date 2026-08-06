// ============================================================================
// SO YOU THINK YOU KNOW 80s MUSIC! - ENHANCED GAME ENGINE V3
// ============================================================================

let songsMap = {};          // id -> { id, t: title, a: artist, highestPos, weeksInTop10, weeksInTop20, reachedNum1 }
let artistSongsMap = {};    // artistName -> array of song objects
let chartWeeks = [];        // array of { dateKey, year, exactDateFormatted, positions: [songId...] }
let currentQuestion = null;
let currentWeek = null;
let currentChartModalWeekIndex = 0;
let selectedAnswerIndex = null;
let answerRevealed = false;

// Timer Mode & Bonus Points State
let bonusTimerInterval = null;
let bonusSecondsLeft = 10;
let currentBonusPoints = 5;

// Player Profile & State
let state = {
    userName: 'SynthRider84',
    avatar: '🕹️',
    score: 0,
    currentLevel: 1,
    unlockedLevel: 1,
    strikes: 0,
    lifelines5050: 3,
    cooldownEndTime: 0,
    timerModeEnabled: false,
    tonedDownTheme: false
};

const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", 
                     "July", "August", "September", "October", "November", "December"];

// Initial Setup
document.addEventListener('DOMContentLoaded', () => {
    loadLocalState();
    loadChartData();
});

// ----------------------------------------------------------------------------
// 1. DATA PARSING & EXACT DATE FORMATTING
// ----------------------------------------------------------------------------
async function loadChartData() {
    const progressEl = document.getElementById('splash-progress');
    const statusEl = document.getElementById('splash-status');

    try {
        if (statusEl) statusEl.textContent = 'Loading 80s Top 20 Charts JSON...';
        if (progressEl) progressEl.style.width = '30%';

        const response = await fetch('data/charts_80s_top20_compressed.json');
        const data = await response.json();

        if (progressEl) progressEl.style.width = '55%';
        if (statusEl) statusEl.textContent = 'Pre-computing 80s Song Statistics & Exact Dates...';

        // Initialize Songs
        data.songs.forEach(song => {
            songsMap[song.id] = {
                id: song.id,
                t: song.t,
                a: song.a,
                highestPos: 99,
                weeksInTop10: 0,
                weeksInTop20: 0,
                reachedNum1: false
            };

            const artistKey = song.a.trim().toUpperCase();
            if (!artistSongsMap[artistKey]) artistSongsMap[artistKey] = [];
            artistSongsMap[artistKey].push(songsMap[song.id]);
        });

        // Parse & Compute Exact Dates (1980 - 1989)
        const dateKeys = Object.keys(data.charts).sort();
        dateKeys.forEach(dateKey => {
            const year = parseInt(dateKey.substring(0, 4));
            if (year >= 1980 && year <= 1989) {
                const exactDateFormatted = formatExactChartDate(dateKey);
                const positions = data.charts[dateKey];

                chartWeeks.push({
                    dateKey: dateKey,
                    year: year,
                    exactDateFormatted: exactDateFormatted,
                    positions: positions
                });

                // Compute stats for each song
                positions.forEach((songId, idx) => {
                    const posNum = idx + 1;
                    const s = songsMap[songId];
                    if (s) {
                        if (posNum < s.highestPos) s.highestPos = posNum;
                        if (posNum === 1) s.reachedNum1 = true;
                        if (posNum <= 10) s.weeksInTop10++;
                        s.weeksInTop20++;
                    }
                });
            }
        });

        if (progressEl) progressEl.style.width = '100%';
        if (statusEl) statusEl.textContent = `Loaded ${chartWeeks.length} chart weeks & ${Object.keys(songsMap).length} songs!`;

        setTimeout(() => {
            document.getElementById('splash-screen').classList.add('hidden');
            applyTheme();
            updateUserUI();
            checkCooldownState();
            generateNextQuestion();
            renderLeaderboard();
        }, 1000);

    } catch (err) {
        console.error('Error loading chart data:', err);
        if (statusEl) statusEl.textContent = 'Failed to load chart data.';
        setTimeout(() => {
            document.getElementById('splash-screen').classList.add('hidden');
        }, 1500);
    }
}

// Helper: Format exact YYYYMMDD date to "July 18th, 1984"
function formatExactChartDate(dateKey) {
    const year = dateKey.substring(0, 4);
    const month = parseInt(dateKey.substring(4, 6)) - 1;
    const day = parseInt(dateKey.substring(6, 8));

    const monthName = MONTH_NAMES[month] || '';
    const ordinal = getOrdinalSuffix(day);

    return `${monthName} ${day}${ordinal}, ${year}`;
}

function getOrdinalSuffix(d) {
    if (d > 3 && d < 21) return 'th';
    switch (d % 10) {
        case 1:  return "st";
        case 2:  return "nd";
        case 3:  return "rd";
        default: return "th";
    }
}

// ----------------------------------------------------------------------------
// 2. QUESTION GENERATION ENGINE (LEVELS 1 - 4)
// ----------------------------------------------------------------------------
function generateNextQuestion() {
    if (chartWeeks.length === 0) return;
    if (checkCooldownState()) return;

    // Reset UI & State
    selectedAnswerIndex = null;
    answerRevealed = false;
    stopBonusTimer();

    document.getElementById('btn-next').disabled = true;
    document.getElementById('feedback-banner').className = 'feedback-banner hidden';
    document.getElementById('btn-reveal-answer').classList.add('hidden');
    document.getElementById('btn-view-chart').classList.add('hidden');
    document.getElementById('btn-5050').disabled = (state.lifelines5050 <= 0);

    // Re-enable all 4 answer buttons
    for (let i = 0; i < 4; i++) {
        const btn = document.getElementById(`btn-ans-${i}`);
        btn.className = 'answer-btn';
        btn.disabled = false;
    }

    // Pick random week
    const weekIndex = Math.floor(Math.random() * chartWeeks.length);
    currentWeek = chartWeeks[weekIndex];
    currentChartModalWeekIndex = weekIndex;

    const level = state.currentLevel;
    const typeRoll = Math.random();

    if (level === 1) {
        generateLevel1Question(currentWeek, weekIndex);
    } else if (level === 2) {
        generateLevel2Question(currentWeek, weekIndex);
    } else if (level === 3) {
        if (typeRoll > 0.5) generateLevel3Question(currentWeek, weekIndex);
        else generateHighestPeakQuestion();
    } else {
        if (typeRoll > 0.6) generateLevel4Question(currentWeek, weekIndex);
        else if (typeRoll > 0.3) generateNeverNumberOneQuestion();
        else generateWeeksInTop10Question();
    }

    renderQuestionUI();

    if (state.timerModeEnabled) {
        startBonusTimer();
    } else {
        document.getElementById('bonus-timer-box').classList.add('hidden');
    }
}

// Level 1: "Who sang..." (Artist-Specific Questions)
function generateLevel1Question(week, weekIndex) {
    const pos = Math.floor(Math.random() * 2);
    const songId = week.positions[pos];
    const targetSong = songsMap[songId];

    const questionText = `Who sang "${targetSong.t}" when it hit the Top 2 on ${week.exactDateFormatted}?`;
    const correctAnswer = targetSong.a;

    const distractors = getSmartArtistDistractors(targetSong.a, week, pos);
    const options = assembleFourOptions(correctAnswer, distractors);

    currentQuestion = {
        level: 1,
        basePoints: 1,
        artistNamed: false,
        category: 'LEVEL 1: TOP 2 HITS',
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Level 2: "Which song did [Artist] get to Number 1 with on [Exact Date]?" (Song Titles ONLY when artist is named!)
function generateLevel2Question(week, weekIndex) {
    const num1Song = songsMap[week.positions[0]];
    const num2Song = songsMap[week.positions[1]];

    let questionText = '';
    let correctAnswer = '';
    let artistNamed = true;
    const distractors = new Set();

    if (Math.random() > 0.5 && num1Song && num2Song) {
        // Artist IS named in prompt -> Answer options are SONG TITLES ONLY!
        questionText = `Which song did ${num1Song.a} get to Number 1 with on ${week.exactDateFormatted}?`;
        correctAnswer = num1Song.t;
        artistNamed = true;

        // Try to get other songs by the exact same artist (e.g. Sonia, Madonna)!
        const artistKey = num1Song.a.trim().toUpperCase();
        const sameArtistSongs = artistSongsMap[artistKey] || [];
        sameArtistSongs.forEach(s => {
            if (s.t !== correctAnswer) distractors.add(s.t);
        });

        // Fill remaining distractors with songs from same week
        [1, 2, 3, 4].forEach(p => {
            if (week.positions[p]) distractors.add(songsMap[week.positions[p]].t);
        });
    } else {
        // Artist NOT named in prompt -> Format as "Song Title" - Artist Name
        questionText = `Which song was held off top spot at Number 2 on ${week.exactDateFormatted}?`;
        correctAnswer = `"${num2Song.t}" - ${num2Song.a}`;
        artistNamed = false;

        [0, 2, 3, 4].forEach(p => {
            if (week.positions[p]) {
                const s = songsMap[week.positions[p]];
                distractors.add(`"${s.t}" - ${s.a}`);
            }
        });
    }

    const options = assembleFourOptions(correctAnswer, Array.from(distractors));

    currentQuestion = {
        level: 2,
        basePoints: 2,
        artistNamed: artistNamed,
        category: 'LEVEL 2: NUMBER 1 HITS',
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Level 3: Top 10 Deep-Dive
function generateLevel3Question(week, weekIndex) {
    const pos = Math.floor(Math.random() * 10);
    const songId = week.positions[pos];
    const targetSong = songsMap[songId];

    const questionText = `Who sang "${targetSong.t}" when it reached Number ${pos + 1} on ${week.exactDateFormatted}?`;
    const correctAnswer = targetSong.a;

    const distractors = getSmartArtistDistractors(targetSong.a, week, pos);
    const options = assembleFourOptions(correctAnswer, distractors);

    currentQuestion = {
        level: 3,
        basePoints: 3,
        artistNamed: false,
        category: `LEVEL 3: TOP 10 DEEP-DIVE (NUMBER ${pos + 1})`,
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Level 3 Peak Question
function generateHighestPeakQuestion() {
    const randomSongId = Math.floor(Math.random() * Object.keys(songsMap).length) + 1;
    const targetSong = songsMap[randomSongId];

    if (!targetSong) return generateLevel3Question(currentWeek, 0);

    const peakPos = targetSong.highestPos;
    const questionText = `What was the highest UK chart position reached by "${targetSong.t}" by ${targetSong.a}?`;
    const correctAnswer = `Number ${peakPos}`;

    const distractors = new Set();
    [peakPos + 1, peakPos + 2, Math.max(1, peakPos - 1), peakPos + 4].forEach(p => {
        if (p !== peakPos && p <= 20) distractors.add(`Number ${p}`);
    });

    const options = assembleFourOptions(correctAnswer, Array.from(distractors));

    currentQuestion = {
        level: 3,
        basePoints: 3,
        artistNamed: true,
        category: 'LEVEL 3: HIGHEST PEAK POSITION',
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Level 4: Never Number 1 Question
function generateNeverNumberOneQuestion() {
    const num1Songs = Object.values(songsMap).filter(s => s.reachedNum1);
    const neverNum1Songs = Object.values(songsMap).filter(s => !s.reachedNum1 && s.highestPos <= 3);

    if (num1Songs.length < 3 || neverNum1Songs.length === 0) return generateLevel4Question(currentWeek, 0);

    const targetNever = neverNum1Songs[Math.floor(Math.random() * neverNum1Songs.length)];
    const questionText = `Which of these famous 80s songs NEVER got to Number 1 in the UK?`;
    const correctAnswer = `"${targetNever.t}" - ${targetNever.a} (Peaked at #${targetNever.highestPos})`;

    const distractors = new Set();
    while (distractors.size < 3) {
        const s = num1Songs[Math.floor(Math.random() * num1Songs.length)];
        distractors.add(`"${s.t}" - ${s.a}`);
    }

    const options = assembleFourOptions(correctAnswer, Array.from(distractors));

    currentQuestion = {
        level: 4,
        basePoints: 4,
        artistNamed: false,
        category: 'LEVEL 4: NEVER NUMBER 1?',
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Level 4: Weeks in Top 10 Question
function generateWeeksInTop10Question() {
    const songsWithWeeks = Object.values(songsMap).filter(s => s.weeksInTop10 >= 3);
    const targetSong = songsWithWeeks[Math.floor(Math.random() * songsWithWeeks.length)];

    if (!targetSong) return generateLevel4Question(currentWeek, 0);

    const weeksCount = targetSong.weeksInTop10;
    const questionText = `How many weeks did "${targetSong.t}" by ${targetSong.a} remain in the UK Top 10?`;
    const correctAnswer = `${weeksCount} Weeks`;

    const distractors = new Set();
    [weeksCount + 2, Math.max(1, weeksCount - 2), weeksCount + 4, weeksCount + 1].forEach(w => {
        if (w !== weeksCount) distractors.add(`${w} Weeks`);
    });

    const options = assembleFourOptions(correctAnswer, Array.from(distractors));

    currentQuestion = {
        level: 4,
        basePoints: 4,
        artistNamed: true,
        category: 'LEVEL 4: WEEKS IN TOP 10',
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Level 4: Advanced Chart Showdown
function generateLevel4Question(week, weekIndex) {
    const num1Song = songsMap[week.positions[0]];
    const num2Song = songsMap[week.positions[1]];

    const questionText = `Who did ${num1Song.a} knock off top spot on ${week.exactDateFormatted} with "${num1Song.t}"?`;
    const correctAnswer = `"${num2Song.t}" - ${num2Song.a}`;

    const distractors = new Set();
    [2, 3, 4, 5].forEach(p => {
        if (week.positions[p]) {
            const s = songsMap[week.positions[p]];
            distractors.add(`"${s.t}" - ${s.a}`);
        }
    });

    const options = assembleFourOptions(correctAnswer, Array.from(distractors));

    currentQuestion = {
        level: 4,
        basePoints: 4,
        artistNamed: false,
        category: 'LEVEL 4: CHART SHOWDOWN',
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Smart Distractors Generator
function getSmartArtistDistractors(artistName, week, targetPos) {
    const distractors = new Set();
    const artistKey = artistName.trim().toUpperCase();
    const sameArtistSongs = artistSongsMap[artistKey] || [];

    if (sameArtistSongs.length >= 2) {
        sameArtistSongs.forEach(s => {
            if (s.a !== artistName) distractors.add(s.a);
        });
    }

    [1, 2, 3, 4, 5, 6].forEach(p => {
        if (p !== targetPos && week.positions[p]) {
            const a = songsMap[week.positions[p]].a;
            if (a !== artistName) distractors.add(a);
        }
    });

    return Array.from(distractors);
}

// Assemble 4 Options
function assembleFourOptions(correct, distractorsList) {
    while (distractorsList.length < 3) {
        const randomSong = songsMap[Math.floor(Math.random() * Object.keys(songsMap).length) + 1];
        if (randomSong && randomSong.a !== correct && randomSong.t !== correct) {
            distractorsList.push(randomSong.a);
        }
    }

    const set3 = distractorsList.slice(0, 3);
    const pool = [correct, ...set3];
    
    for (let i = pool.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [pool[i], pool[j]] = [pool[j], pool[i]];
    }

    return {
        shuffled: pool,
        correctIndex: pool.indexOf(correct)
    };
}

// ----------------------------------------------------------------------------
// 3. TIMER MODE TOGGLE & BONUS TIMER
// ----------------------------------------------------------------------------
function toggleTimerMode() {
    state.timerModeEnabled = !state.timerModeEnabled;
    saveLocalState();

    const statusEl = document.getElementById('timer-toggle-status');
    const btnToggle = document.getElementById('btn-timer-toggle');
    const bonusBox = document.getElementById('bonus-timer-box');

    if (state.timerModeEnabled) {
        statusEl.textContent = 'ON (2x Pts)';
        btnToggle.classList.add('active');
        bonusBox.classList.remove('hidden');
        startBonusTimer();
    } else {
        statusEl.textContent = 'OFF';
        btnToggle.classList.remove('active');
        bonusBox.classList.add('hidden');
        stopBonusTimer();
    }

    updateQuestionPointsDisplay();
}

function updateQuestionPointsDisplay() {
    if (!currentQuestion) return;
    const multiplier = state.timerModeEnabled ? 2 : 1;
    const finalPts = currentQuestion.basePoints * multiplier;
    document.getElementById('question-points').textContent = `+${finalPts} PT${finalPts > 1 ? 'S' : ''}${state.timerModeEnabled ? ' (2x TIMER)' : ''}`;
}

function startBonusTimer() {
    stopBonusTimer();
    bonusSecondsLeft = 10;
    currentBonusPoints = 5;
    updateTimerUI();

    bonusTimerInterval = setInterval(() => {
        bonusSecondsLeft--;
        if (bonusSecondsLeft % 2 === 0 && currentBonusPoints > 0) {
            currentBonusPoints--;
        }
        updateTimerUI();

        if (bonusSecondsLeft <= 0) {
            stopBonusTimer();
        }
    }, 1000);
}

function stopBonusTimer() {
    if (bonusTimerInterval) {
        clearInterval(bonusTimerInterval);
        bonusTimerInterval = null;
    }
}

function updateTimerUI() {
    const timerText = document.getElementById('timer-text');
    const bonusBadge = document.getElementById('bonus-points-badge');

    if (timerText) timerText.textContent = `${bonusSecondsLeft}s`;
    if (bonusBadge) bonusBadge.textContent = `+${currentBonusPoints} BONUS`;
}

// ----------------------------------------------------------------------------
// 4. 50/50 LIFELINE
// ----------------------------------------------------------------------------
function useLifeline5050() {
    if (state.lifelines5050 <= 0 || !currentQuestion || selectedAnswerIndex !== null) return;

    state.lifelines5050--;
    document.getElementById('count-5050').textContent = state.lifelines5050;
    document.getElementById('btn-5050').disabled = true;

    const wrongIndices = [0, 1, 2, 3].filter(idx => idx !== currentQuestion.correctIndex);
    wrongIndices.sort(() => Math.random() - 0.5);

    wrongIndices.slice(0, 2).forEach(idx => {
        const btn = document.getElementById(`btn-ans-${idx}`);
        btn.disabled = true;
        btn.classList.add('eliminated');
    });

    saveLocalState();
}

// ----------------------------------------------------------------------------
// 5. UI RENDERERS & GAMEPLAY CONTROLS
// ----------------------------------------------------------------------------
function renderQuestionUI() {
    if (!currentQuestion) return;

    document.getElementById('question-category').textContent = currentQuestion.category;
    updateQuestionPointsDisplay();
    document.getElementById('question-text').textContent = currentQuestion.text;

    currentQuestion.options.forEach((opt, idx) => {
        const btn = document.getElementById(`ans-${idx}`);
        btn.textContent = opt;
    });
}

function submitAnswer(selectedIndex) {
    if (selectedAnswerIndex !== null || !currentQuestion) return;

    stopBonusTimer();
    selectedAnswerIndex = selectedIndex;
    const isCorrect = (selectedIndex === currentQuestion.correctIndex);
    const feedbackBanner = document.getElementById('feedback-banner');
    const feedbackIcon = document.getElementById('feedback-icon');
    const feedbackText = document.getElementById('feedback-text');
    const btnReveal = document.getElementById('btn-reveal-answer');
    const btnChart = document.getElementById('btn-view-chart');

    for (let i = 0; i < 4; i++) {
        const btn = document.getElementById(`btn-ans-${i}`);
        btn.disabled = true;
    }

    const multiplier = state.timerModeEnabled ? 2 : 1;
    const basePtsEarned = currentQuestion.basePoints * multiplier;

    if (isCorrect) {
        const bonusPtsEarned = state.timerModeEnabled ? currentBonusPoints : 0;
        const totalPointsEarned = basePtsEarned + bonusPtsEarned;
        state.score += totalPointsEarned;

        document.getElementById(`btn-ans-${selectedIndex}`).classList.add('correct');

        feedbackBanner.className = 'feedback-banner correct-banner';
        feedbackIcon.textContent = '🎉';
        feedbackText.textContent = `CORRECT! +${basePtsEarned} PT${bonusPtsEarned > 0 ? ` (+${bonusPtsEarned} TIMER BONUS)` : ''}!`;

        // Hide "Reveal Answer" on correct guess! Show "View Chart"
        btnReveal.classList.add('hidden');
        btnChart.classList.remove('hidden');

        checkLevelUnlocks();
    } else {
        state.strikes++;

        document.getElementById(`btn-ans-${selectedIndex}`).classList.add('wrong');

        feedbackBanner.className = 'feedback-banner wrong-banner';
        feedbackIcon.textContent = '❌';
        feedbackText.textContent = `NOT QUITE RIGHT! Strike ${state.strikes} of 5.`;

        // SHOW "Reveal Answer" ONLY on incorrect guess! Hide "View Chart" until revealed
        btnReveal.classList.remove('hidden');
        btnChart.classList.add('hidden');

        if (state.strikes >= 5) {
            startCooldownPenalty();
        }
    }

    saveLocalState();
    updateUserUI();
    document.getElementById('btn-next').disabled = false;
}

function revealCorrectAnswer() {
    if (!currentQuestion || answerRevealed) return;
    answerRevealed = true;

    document.getElementById(`btn-ans-${currentQuestion.correctIndex}`).classList.add('correct');
    
    document.getElementById('feedback-text').textContent = `Correct Answer: "${currentQuestion.options[currentQuestion.correctIndex]}"`;
    document.getElementById('btn-reveal-answer').classList.add('hidden');
    document.getElementById('btn-view-chart').classList.remove('hidden');
}

// ----------------------------------------------------------------------------
// 6. TOP 5 CHART VIEW MODAL & WEEK NAVIGATION (PREV/NEXT)
// ----------------------------------------------------------------------------
function openWeekChartModal() {
    if (chartWeeks.length === 0) return;
    renderChartModalWeek(currentChartModalWeekIndex);
    document.getElementById('modal-chart').classList.remove('hidden');
}

function navigateChartWeek(dir) {
    let nextIndex = currentChartModalWeekIndex + dir;
    if (nextIndex < 0) nextIndex = 0;
    if (nextIndex >= chartWeeks.length) nextIndex = chartWeeks.length - 1;

    currentChartModalWeekIndex = nextIndex;
    renderChartModalWeek(nextIndex);
}

function renderChartModalWeek(idx) {
    const week = chartWeeks[idx];
    if (!week) return;

    document.getElementById('chart-modal-title').textContent = `UK Official Chart - ${week.exactDateFormatted}`;
    document.getElementById('chart-week-index-text').textContent = `Week ${idx + 1} of ${chartWeeks.length}`;

    const listEl = document.getElementById('chart-modal-list');

    // Free Tier: Render positions #1 through #5 ONLY!
    const top5Positions = week.positions.slice(0, 5);

    listEl.innerHTML = top5Positions.map((songId, posIdx) => {
        const song = songsMap[songId];
        const isHighlighted = (currentQuestion && (currentQuestion.options[currentQuestion.correctIndex].includes(song.t) || currentQuestion.options[currentQuestion.correctIndex].includes(song.a)));

        return `
            <div class="chart-row ${isHighlighted ? 'highlight' : ''}">
                <div class="chart-pos">#${posIdx + 1}</div>
                <div class="chart-song-info">
                    <div class="chart-title">${song.t}</div>
                    <div class="chart-artist">${song.a}</div>
                </div>
            </div>
        `;
    }).join('');
}

function closeWeekChartModal() {
    document.getElementById('modal-chart').classList.add('hidden');
}

// ----------------------------------------------------------------------------
// 7. VISUAL THEME & LEVEL UNLOCKS
// ----------------------------------------------------------------------------
function toggleVisualTheme() {
    state.tonedDownTheme = !state.tonedDownTheme;
    saveLocalState();
    applyTheme();
}

function applyTheme() {
    const body = document.getElementById('app-body');
    const btnText = document.getElementById('theme-btn-text');

    if (state.tonedDownTheme) {
        body.classList.add('theme-toned-down');
        btnText.textContent = '⚡ Neon Theme';
    } else {
        body.classList.remove('theme-toned-down');
        btnText.textContent = '🎨 Toned-Down';
    }
}

function checkLevelUnlocks() {
    let newlyUnlocked = state.unlockedLevel;

    if (state.score >= 30) newlyUnlocked = 4;
    else if (state.score >= 15) newlyUnlocked = 3;
    else if (state.score >= 5) newlyUnlocked = 2;

    if (newlyUnlocked > state.unlockedLevel) {
        state.unlockedLevel = newlyUnlocked;
        state.currentLevel = newlyUnlocked;
    }
}

function selectLevel(lvl) {
    if (lvl > state.unlockedLevel) return;
    state.currentLevel = lvl;
    saveLocalState();
    updateUserUI();
    showScreen('game');
    generateNextQuestion();
}

// Penalty & Cool-down System
let timerInterval = null;

function startCooldownPenalty() {
    state.cooldownEndTime = Date.now() + (5 * 60 * 1000);
    saveLocalState();
    checkCooldownState();
}

function checkCooldownState() {
    const modal = document.getElementById('modal-cooldown');
    const now = Date.now();

    if (state.cooldownEndTime && state.cooldownEndTime > now) {
        modal.classList.remove('hidden');
        updateCooldownTimerDisplay();
        
        if (!timerInterval) {
            timerInterval = setInterval(() => {
                const remaining = state.cooldownEndTime - Date.now();
                if (remaining <= 0) {
                    clearInterval(timerInterval);
                    timerInterval = null;
                    state.cooldownEndTime = 0;
                    state.strikes = 0;
                    saveLocalState();
                    updateUserUI();
                    modal.classList.add('hidden');
                    generateNextQuestion();
                } else {
                    updateCooldownTimerDisplay();
                }
            }, 1000);
        }
        return true;
    } else {
        modal.classList.add('hidden');
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        return false;
    }
}

function updateCooldownTimerDisplay() {
    const remainingMs = Math.max(0, state.cooldownEndTime - Date.now());
    const totalSecs = Math.floor(remainingMs / 1000);
    const mins = Math.floor(totalSecs / 60);
    const secs = totalSecs % 60;

    const timerText = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    document.getElementById('cooldown-timer-text').textContent = timerText;
}

function skipCooldown() {
    state.cooldownEndTime = 0;
    state.strikes = 0;
    saveLocalState();
    updateUserUI();
    document.getElementById('modal-cooldown').classList.add('hidden');
    generateNextQuestion();
}

// Navigation & Profile
function showScreen(screenId) {
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.screen-view').forEach(sc => sc.classList.remove('active'));

    const navBtn = document.getElementById(`nav-${screenId}`);
    if (navBtn) navBtn.classList.add('active');

    const targetScreen = document.getElementById(`screen-${screenId}`);
    if (targetScreen) targetScreen.classList.add('active');
}

function updateUserUI() {
    document.getElementById('user-avatar-display').textContent = state.avatar;
    document.getElementById('user-name-display').textContent = state.userName;
    document.getElementById('user-rank-display').textContent = `Level ${state.currentLevel} (${getLevelName(state.currentLevel)})`;
    document.getElementById('score-display').textContent = state.score;
    document.getElementById('level-display').textContent = `Lvl ${state.currentLevel}`;
    document.getElementById('count-5050').textContent = state.lifelines5050;

    const timerStatus = document.getElementById('timer-toggle-status');
    const btnTimerToggle = document.getElementById('btn-timer-toggle');
    const bonusBox = document.getElementById('bonus-timer-box');

    if (state.timerModeEnabled) {
        if (timerStatus) timerStatus.textContent = 'ON (2x Pts)';
        if (btnTimerToggle) btnTimerToggle.classList.add('active');
        if (bonusBox) bonusBox.classList.remove('hidden');
    } else {
        if (timerStatus) timerStatus.textContent = 'OFF';
        if (btnTimerToggle) btnTimerToggle.classList.remove('active');
        if (bonusBox) bonusBox.classList.add('hidden');
    }

    const dots = document.querySelectorAll('.strike-dot');
    dots.forEach((dot, idx) => {
        if (idx < state.strikes) dot.classList.add('filled');
        else dot.classList.remove('filled');
    });

    updateLevelCardsUI();
}

function updateLevelCardsUI() {
    for (let l = 2; l <= 4; l++) {
        const card = document.getElementById(`level-card-${l}`);
        const status = document.getElementById(`level-status-${l}`);
        if (!card || !status) continue;

        if (l <= state.unlockedLevel) {
            card.classList.add('unlocked');
            status.textContent = (l === state.currentLevel) ? 'ACTIVE' : 'UNLOCKED';
            status.style.color = '#00F0FF';
        } else {
            card.classList.remove('unlocked');
            const req = (l === 2) ? 5 : (l === 3) ? 15 : 30;
            status.textContent = `REQ: ${req} PTS`;
            status.style.color = '#A0A0C0';
        }
    }
}

function getLevelName(lvl) {
    switch(lvl) {
        case 1: return 'Novice';
        case 2: return 'Hit Master';
        case 3: return 'Chart Expert';
        case 4: return '80s Music Legend';
        default: return 'Gamer';
    }
}

function saveLocalState() {
    localStorage.setItem('80s_quiz_state_v3', JSON.stringify(state));
}

function loadLocalState() {
    const saved = localStorage.getItem('80s_quiz_state_v3');
    if (saved) {
        try {
            state = { ...state, ...JSON.parse(saved) };
        } catch (e) { console.error('Failed to parse local storage', e); }
    }
}

function renderLeaderboard() {
    const lbRowsEl = document.getElementById('lb-rows');
    document.getElementById('lb-user-name').textContent = state.userName;
    document.getElementById('lb-user-stats').textContent = `Score: ${state.score} Pts • Level ${state.currentLevel}`;

    const mockPlayers = [
        { name: 'NeonQueen88', score: 142, level: 4 },
        { name: 'RetroRick', score: 118, level: 4 },
        { name: 'SynthMaster', score: 94, level: 4 },
        { name: 'CassetteKid', score: 76, level: 3 },
        { name: 'VaporDave', score: 58, level: 3 },
        { name: 'ArcadeHero', score: 45, level: 2 },
    ];

    const all = [...mockPlayers, { name: `${state.userName} (You)`, score: state.score, level: state.currentLevel, isUser: true }];
    all.sort((a, b) => b.score - a.score);

    lbRowsEl.innerHTML = all.map((p, idx) => `
        <div class="lb-row ${p.isUser ? 'lb-user-row' : ''}">
            <span>#${idx + 1}</span>
            <span>${p.name}</span>
            <span>Lvl ${p.level}</span>
            <span>${p.score} pts</span>
        </div>
    `).join('');
}

// Modals
function showPlayerModal() {
    document.getElementById('player-name-input').value = state.userName;
    document.getElementById('modal-player').classList.remove('hidden');
}

function closePlayerModal() {
    document.getElementById('modal-player').classList.add('hidden');
}

function selectAvatar(emoji) {
    state.avatar = emoji;
}

function savePlayerProfile() {
    const val = document.getElementById('player-name-input').value.trim();
    if (val) state.userName = val;
    saveLocalState();
    updateUserUI();
    renderLeaderboard();
    closePlayerModal();
}

function showPaywallModal(type) {
    const title = document.getElementById('paywall-title');
    const desc = document.getElementById('paywall-desc');

    if (type === 'level5') {
        title.textContent = 'Unlock Level 5: Lyrics & Trivia Pack!';
        desc.textContent = 'Get access to lyric challenges, band histories, and album trivia!';
    } else if (type === 'chart') {
        title.textContent = 'Unlock Full Top 20 Weekly Chart Archives!';
        desc.textContent = 'Access positions #6 through #20 for all 522 chart weeks of the 1980s!';
    } else {
        title.textContent = 'Unlock 90s & 00s Music Charts!';
        desc.textContent = 'Expand your quiz beyond the 80s with thousands of Top 20 hits from 1990 to 2009!';
    }

    document.getElementById('modal-paywall').classList.remove('hidden');
}

function closePaywallModal() {
    document.getElementById('modal-paywall').classList.add('hidden');
}

function simulatePurchase() {
    alert('Simulated In-App Purchase Successful! All packs & Level 5 unlocked!');
    closePaywallModal();
}
