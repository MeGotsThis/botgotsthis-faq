CREATE TABLE faq (
    broadcaster VARCHAR NOT NULL PRIMARY KEY,
    faq VARCHAR NOT NULL 
);

CREATE TABLE faq_game (
    broadcaster VARCHAR NOT NULL,
    twitchGame VARCHAR NOT NULL,
    faq VARCHAR NOT NULL,
    PRIMARY KEY (broadcaster, twitchGame)
);
