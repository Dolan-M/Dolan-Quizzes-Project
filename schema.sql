DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS leaderboard;

CREATE TABLE leaderboard
(
    user_id TEXT PRIMARY KEY NOT NULL,
    wombatpoints INTEGER NOT NULL,
    historypoints INTEGER NOT NULL,
    geographypoints INTEGER NOT NULL,
    totalpoints INTEGER NOT NULL
);

DROP TABLE IF EXISTS suggestions;

CREATE TABLE suggestions
(
    user_id TEXT PRIMARY KEY NOT NULL,
    suggestion TEXT NOT NULL,
    date TEXT NOT NULL
);

DROP TABLE IF EXISTS pastwombat;

CREATE TABLE pastwombat
(
    user_id TEXT,
    points INTEGER NOT NULL,
    date TEXT NOT NULL
);

DROP TABLE IF EXISTS pasthistory;

CREATE TABLE pasthistory
(
    user_id TEXT,
    points INTEGER NOT NULL,
    date TEXT NOT NULL
);

DROP TABLE IF EXISTS pastgeography;

CREATE TABLE pastgeography
(
    user_id TEXT,
    points INTEGER NOT NULL,
    date TEXT NOT NULL
);

