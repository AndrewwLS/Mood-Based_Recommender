% ====================================
% Regole simboliche di raccomandazione musicale
% ====================================

% --- Accessori base ---
has_mood(Track, Mood) :-
    track(Track, _, _, _, _, _, _, MoodString),
    string(MoodString),
    string_lower(MoodString, MoodLower),
    atom_string(Mood, MoodLower).

has_genre(Track, Genre) :-
    track(Track, _, _, _, _, _, Genre, _).

has_valence(Track, Valence) :-
    track(Track, _, _, Valence, _, _, _, _).

has_energy(Track, Energy) :-
    track(Track, _, _, _, EVal, _, _, _),
    number(EVal),
    Energy is EVal.

has_danceability(Track, Dance) :-
    track(Track, _, _, Dance, _, _, _, _).

% --- Variante limitata per test controllati ---
has_energy_limited(Track, Energy) :-
    has_energy(Track, Energy),
    sub_atom(Track, 0, 1, _, C),
    member(C, ['A', 'B', 'C', 'D']).

has_mood_limited(Track, Mood) :-
    has_mood(Track, Mood),
    sub_atom(Track, 0, 1, _, C),
    member(C, ['A', 'B', 'C', 'D']).

% --- Regole simboliche con artista ---

recommend_by_mood(Mood, Track, Artist) :-
    track(Track, Artist, _, _, _, _, _, MoodString),
    string(MoodString),
    string_lower(MoodString, MoodLower),
    atom_string(Mood, MoodLower).

is_relaxing(Track, Artist) :-
    track(Track, Artist, _, _, EVal, _, _, _),
    number(EVal),
    EVal =< 0.5.

is_energetic(Track, Artist) :-
    track(Track, Artist, _, _, EVal, _, _, _),
    number(EVal),
    EVal >= 0.75.

is_danceable(Track, Artist) :-
    track(Track, Artist, _, Dance, _, _, _, _),
    number(Dance),
    Dance >= 0.7.

happy_track_with_high_valence(Track, Artist) :-
    track(Track, Artist, _, Valence, _, _, _, MoodString),
    string(MoodString),
    string_lower(MoodString, 'felice'),
    number(Valence),
    Valence > 0.8.

% --- Compatibilità tra generi ---
compatible_genre(rock, alternative).
compatible_genre(alternative, rock).
compatible_genre(pop, dance).
compatible_genre(dance, pop).
compatible_genre(X, X).
