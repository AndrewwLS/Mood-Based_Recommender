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

% --- Variante limitata per test controllati ---
has_energy_limited(Track, Energy) :-
    has_energy(Track, Energy),
    sub_atom(Track, 0, 1, _, C),
    member(C, ['A', 'B', 'C', 'D']).

has_mood_limited(Track, Mood) :-
    has_mood(Track, Mood),
    sub_atom(Track, 0, 1, _, C),
    member(C, ['A', 'B', 'C', 'D']).

has_danceability(Track, Dance) :-
    track(Track, _, _, Dance, _, _, _, _).

% --- Regole semplici ---
recommend_by_mood(Mood, Track) :-
    has_mood(Track, Mood).

is_relaxing(Track) :-
    has_energy(Track, Energy),
    Energy =< 0.5.

is_energetic(Track) :-
    has_energy(Track, Energy),
    Energy >= 0.75.

is_danceable(Track) :-
    has_danceability(Track, Dance),
    Dance >= 0.7.

% --- Energia simile (differenza <= 0.1, evita duplicati simmetrici) ---
similar_tracks_by_energy(Track1, Track2) :-
    has_energy(Track1, E1),
    has_energy(Track2, E2),
    Track1 @< Track2,
    Diff is abs(E1 - E2),
    Diff =< 0.1.

% --- Valence alto per mood felice ---
happy_track_with_high_valence(Track) :-
    has_mood(Track, 'felice'),
    has_valence(Track, Valence),
    Valence > 0.8.

% --- Compatibilità tra generi ---
compatible_genre(rock, alternative).
compatible_genre(alternative, rock).
compatible_genre(pop, dance).
compatible_genre(dance, pop).
compatible_genre(X, X).
