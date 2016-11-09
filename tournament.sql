create table players(
    id serial primary key,
    name text,
    wins integer,
    matches integer);

-- references players to keep winner and loser for every match
create table matches(
    winner integer,
    loser integer,
    primary key (winner, loser),
    foreign key (winner) references players(id),
    foreign key (loser) references players(id));
