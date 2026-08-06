// ============================================================================
// SO YOU THINK YOU KNOW 80s MUSIC! - GAME ENGINE
// ============================================================================

let songsMap = {};        // id -> { id, t: title, a: artist }
let chartWeeks = [];      // array of { dateKey, year, monthName, positions: [songId...] }
let currentQuestion = null;
let selectedAnswerIndex = null;

// Player Profile & State
let state = {
    userName: 'SynthRider84',
    avatar: '🕹️',
    score: 0,
    currentLevel: 1,
    unlockedLevel: 1,
    strikes: 0,
    cooldownEndTime: 0, // timestamp
};

const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", 
                     "July", "August", "September", "October", "November", "December"];

// Initial Setup
document.addEventListener('DOMContentLoaded', () => {
    loadLocalState();
    loadChartData();
});

// ----------------------------------------------------------------------------
// 1. DATA PARSING & INITIALIZATION
// ----------------------------------------------------------------------------
async function loadChartData() {
    const progressEl = document.getElementById('splash-progress');
    const statusEl = document.getElementById('splash-status');

    try {
        if (statusEl) statusEl.textContent = 'Loading 80s Top 20 Charts JSON...';
        if (progressEl) progressEl.style.width = '30%';

        const response = await fetch('data/charts_80s_top20_compressed.json');
        const data = await response.json();

        if (progressEl) progressEl.style.width = '65%';
        if (statusEl) statusEl.textContent = 'Parsing 1980 - 1989 UK Charts...';

        // Parse Songs
        data.songs.forEach(song => {
            songsMap[song.id] = song;
        });

        // Parse & Filter 80s Chart Weeks (1980 - 1989)
        const dateKeys = Object.keys(data.charts).sort();
        dateKeys.forEach(dateKey => {
            const year = parseInt(dateKey.substring(0, 4));
            if (year >= 1980 && year <= 1989) {
                const month = parseInt(dateKey.substring(4, 6)) - 1;
                const monthName = MONTH_NAMES[month] || '';
                chartWeeks.push({
                    dateKey: dateKey,
                    year: year,
                    monthName: `${monthName} ${year}`,
                    positions: data.charts[dateKey]
                });
            }
        });

        if (progressEl) progressEl.style.width = '100%';
        if (statusEl) statusEl.textContent = `Loaded ${chartWeeks.length} weeks of 80s Top 20 hits!`;

        setTimeout(() => {
            document.getElementById('splash-screen').classList.add('hidden');
            updateUserUI();
            checkCooldownState();
            generateNextQuestion();
            renderLeaderboard();
        }, 1200);

    } catch (err) {
        console.error('Error loading chart data:', err);
        if (statusEl) statusEl.textContent = 'Failed to load chart data. Using offline mode.';
        setTimeout(() => {
            document.getElementById('splash-screen').classList.add('hidden');
        }, 1500);
    }
}

// ----------------------------------------------------------------------------
// 2. QUESTION GENERATORS (LEVELS 1 - 4)
// ----------------------------------------------------------------------------
function generateNextQuestion() {
    if (chartWeeks.length === 0) return;
    if (checkCooldownState()) return;

    // Reset UI
    selectedAnswerIndex = null;
    document.getElementById('btn-next').disabled = true;
    document.getElementById('feedback-banner').className = 'feedback-banner hidden';

    // Pick random week
    const weekIndex = Math.floor(Math.random() * chartWeeks.length);
    const week = chartWeeks[weekIndex];

    const level = state.currentLevel;

    if (level === 1) {
        generateLevel1Question(week, weekIndex);
    } else if (level === 2) {
        generateLevel2Question(week, weekIndex);
    } else if (level === 3) {
        generateLevel3Question(week, weekIndex);
    } else {
        generateLevel4Question(week, weekIndex);
    }

    renderQuestionUI();
}

// Level 1: "Who sang..." (Top 2 Hits)
function generateLevel1Question(week, weekIndex) {
    const pos = Math.floor(Math.random() * 2); // #0 (1st) or #1 (2nd)
    const songId = week.positions[pos];
    const targetSong = songsMap[songId];

    const questionText = `Who sang "${targetSong.t}" when it stormed the Top 2 in ${week.monthName}?`;
    const correctAnswer = targetSong.a;

    // Distractors: Artists from position #3, #4, #5 or adjacent week
    const distractors = new Set();
    [2, 3, 4, 5].forEach(p => {
        if (week.positions[p]) {
            const a = songsMap[week.positions[p]].a;
            if (a !== correctAnswer) distractors.add(a);
        }
    });

    // Add from adjacent week if needed
    if (distractors.size < 3 && weekIndex > 0) {
        const prevWeek = chartWeeks[weekIndex - 1];
        [0, 1, 2].forEach(p => {
            if (prevWeek.positions[p]) {
                const a = songsMap[prevWeek.positions[p]].a;
                if (a !== correctAnswer) distractors.add(a);
            }
        });
    }

    const options = assembleFourOptions(correctAnswer, Array.from(distractors));

    currentQuestion = {
        level: 1,
        points: 1,
        category: 'LEVEL 1: TOP 2 HITS',
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Level 2: "What song did [Artist] get to Number 1 with in [Month Year]?"
function generateLevel2Question(week, weekIndex) {
    const songId = week.positions[0]; // Number 1
    const targetSong = songsMap[songId];

    const questionText = `What song did ${targetSong.a} get to Number 1 with in ${week.monthName}?`;
    const correctAnswer = targetSong.t;

    // Distractors: Song titles from #2, #3, #4 in same week
    const distractors = new Set();
    [1, 2, 3, 4].forEach(p => {
        if (week.positions[p]) {
            const title = songsMap[week.positions[p]].t;
            if (title !== correctAnswer) distractors.add(title);
        }
    });

    const options = assembleFourOptions(correctAnswer, Array.from(distractors));

    currentQuestion = {
        level: 2,
        points: 2,
        category: 'LEVEL 2: NUMBER 1 HITS',
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Level 3: Top 10 Deep-Dive
function generateLevel3Question(week, weekIndex) {
    const pos = Math.floor(Math.random() * 10); // 0 to 9
    const songId = week.positions[pos];
    const targetSong = songsMap[songId];

    const questionText = `Who sang "${targetSong.t}" when it reached Number ${pos + 1} in ${week.monthName}?`;
    const correctAnswer = targetSong.a;

    // Distractors: Artists from nearby positions
    const distractors = new Set();
    for (let i = 0; i < 10; i++) {
        if (i !== pos && week.positions[i]) {
            const a = songsMap[week.positions[i]].a;
            if (a !== correctAnswer) distractors.add(a);
        }
    }

    const options = assembleFourOptions(correctAnswer, Array.from(distractors));

    currentQuestion = {
        level: 3,
        points: 3,
        category: `LEVEL 3: TOP 10 DEEP-DIVE (NUMBER ${pos + 1})`,
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Level 4: 80s Chart Showdowns!
function generateLevel4Question(week, weekIndex) {
    const num1Song = songsMap[week.positions[0]];
    const num2Song = songsMap[week.positions[1]];

    let questionText = '';
    let correctAnswer = '';
    const distractors = new Set();

    if (Math.random() > 0.5 && num1Song && num2Song) {
        // "Artist X got to #2 in Month Year with Song X. What song was holding them off at #1?"
        questionText = `${num2Song.a} got to Number 2 in ${week.monthName} with "${num2Song.t}". What song was holding them off at Number 1?`;
        correctAnswer = num1Song.t;

        [2, 3, 4, 5].forEach(p => {
            if (week.positions[p]) distractors.add(songsMap[week.positions[p]].t);
        });
    } else {
        // "In Month Year, Song A was at #1. Which song was right behind it at #2?"
        questionText = `In ${week.monthName}, "${num1Song.t}" by ${num1Song.a} was at Number 1. Which song was right behind it at Number 2?`;
        correctAnswer = num2Song.t;

        [2, 3, 4, 5].forEach(p => {
            if (week.positions[p]) distractors.add(songsMap[week.positions[p]].t);
        });
    }

    const options = assembleFourOptions(correctAnswer, Array.from(distractors));

    currentQuestion = {
        level: 4,
        points: 4,
        category: 'LEVEL 4: CHART SHOWDOWN',
        text: questionText,
        options: options.shuffled,
        correctIndex: options.correctIndex
    };
}

// Helper to shuffle correct answer with 3 distractors
function assembleFourOptions(correct, distractorsList) {
    // Fill up to 3 distractors if list is short
    while (distractorsList.length < 3) {
        const randomSong = songsMap[Math.floor(Math.random() * Object.keys(songsMap).length) + 1];
        if (randomSong && randomSong.a !== correct && randomSong.t !== correct) {
            distractorsList.push(randomSong.a);
        }
    }

    const set3 = distractorsList.slice(0, 3);
    const pool = [correct, ...set3];
    
    // Shuffle pool
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
// 3. UI RENDERERS & GAMEPLAY CONTROLS
// ----------------------------------------------------------------------------
function renderQuestionUI() {
    if (!currentQuestion) return;

    document.getElementById('question-category').textContent = currentQuestion.category;
    document.getElementById('question-points').textContent = `+${currentQuestion.points} PT${currentQuestion.points > 1 ? 'S' : ''}`;
    document.getElementById('question-text').textContent = currentQuestion.text;

    currentQuestion.options.forEach((opt, idx) => {
        const btn = document.getElementById(`ans-${idx}`);
        const parentBtn = btn.closest('.answer-btn');
        btn.textContent = opt;
        parentBtn.className = 'answer-btn';
        parentBtn.disabled = false;
    });
}

function submitAnswer(selectedIndex) {
    if (selectedAnswerIndex !== null || !currentQuestion) return;

    selectedAnswerIndex = selectedIndex;
    const isCorrect = (selectedIndex === currentQuestion.correctIndex);
    const feedbackBanner = document.getElementById('feedback-banner');
    const feedbackIcon = document.getElementById('feedback-icon');
    const feedbackText = document.getElementById('feedback-text');

    // Disable all buttons & show correct/wrong styles
    currentQuestion.options.forEach((opt, idx) => {
        const btn = document.getElementById(`ans-${idx}`).closest('.answer-btn');
        btn.disabled = true;
        if (idx === currentQuestion.correctIndex) {
            btn.classList.add('correct');
        } else if (idx === selectedIndex) {
            btn.classList.add('wrong');
        }
    });

    if (isCorrect) {
        state.score += currentQuestion.points;
        feedbackBanner.className = 'feedback-banner correct-banner';
        feedbackIcon.textContent = '🎉';
        feedbackText.textContent = `CORRECT! +${currentQuestion.points} POINT${currentQuestion.points > 1 ? 'S' : ''}!`;
        
        // Check Level Unlocks
        checkLevelUnlocks();
    } else {
        state.strikes++;
        feedbackBanner.className = 'feedback-banner wrong-banner';
        feedbackIcon.textContent = '❌';
        feedbackText.textContent = `WRONG! The correct answer was "${currentQuestion.options[currentQuestion.correctIndex]}".`;

        if (state.strikes >= 5) {
            startCooldownPenalty();
        }
    }

    saveLocalState();
    updateUserUI();
    document.getElementById('btn-next').disabled = false;
}

// Level Unlocks Logic
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

// ----------------------------------------------------------------------------
// 4. PENALTY & COOL-DOWN SYSTEM (5 WRONG ANSWERS)
// ----------------------------------------------------------------------------
let timerInterval = null;

function startCooldownPenalty() {
    state.cooldownEndTime = Date.now() + (5 * 60 * 1000); // 5 minutes from now
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

// ----------------------------------------------------------------------------
// 5. NAVIGATION & USER PROFILE
// ----------------------------------------------------------------------------
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

    // Update Strikes Dots
    const dots = document.querySelectorAll('.strike-dot');
    dots.forEach((dot, idx) => {
        if (idx < state.strikes) dot.classList.add('filled');
        else dot.classList.remove('filled');
    });

    // Update Level Cards Status
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

// ----------------------------------------------------------------------------
// 6. LOCAL STORAGE PERSISTENCE & LEADERBOARD
// ----------------------------------------------------------------------------
function saveLocalState() {
    localStorage.setItem('80s_quiz_state', JSON.stringify(state));
}

function loadLocalState() {
    const saved = localStorage.getItem('80s_quiz_state');
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

    // Insert user into mock leaderboard
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
