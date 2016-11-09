create table players(
    id serial primary key,
    name text);

-- references players to keep winner and loser for every match
create table matches(
    id serial primary key,
    winner integer,
    loser integer,
    foreign key (winner) references players(id),
    foreign key (loser) references players(id));

-- views to simplify queries

-- player id and number of match wins
create view win_counts as
    select players.id, count(matches.winner) as wins
    from players left join matches
    on matches.winner = players.id
    group by players.id;

-- player id and number of match loses
create view lost_counts as
    select players.id, count(matches.loser) as loses
    from players left join matches
    on matches.loser = players.id
    group by players.id;

-- player id and number of matches played
create view match_counts as
    select lost_counts.id, lost_counts.loses + win_counts.wins as matches
    from lost_counts, win_counts
    where lost_counts.id = win_counts.id
    group by lost_counts.id, lost_counts.loses, win_counts.wins;

-- player standings as needed by playerStandings()
create view player_standings as
    select players.id, name, win_counts.wins, match_counts.matches
    from players, win_counts, match_counts
    where players.id = match_counts.id
       and players.id = win_counts.id
    group by players.id, win_counts.wins, match_counts.matches
    order by wins desc, matches desc;
