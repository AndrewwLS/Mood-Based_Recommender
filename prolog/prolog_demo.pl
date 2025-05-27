% ====================================
% Test delle regole simboliche
% ====================================

:- consult('knowledge_base').
:- consult('rules').

% === Utility: stampa massimo N risultati unici ===
limited_results(Query, Max) :-
    findall(Query, call(Query), All),
    sort(All, Unique),
    print_limited(Unique, Max, 0).

print_limited(_, Max, Max) :- !.
print_limited([], _, _) :- !.
print_limited([H|T], Max, Count) :-
    write('  -> '), write(H), nl,
    Count1 is Count + 1,
    print_limited(T, Max, Count1).

% === Test principali ===
run_all_tests :-
    test_recommend_by_mood,
    test_is_relaxing,
    test_is_energetic,
    test_is_danceable,
    test_similar_tracks_by_energy_limited,
    test_happy_track_with_high_valence.

test_recommend_by_mood :-
    write('Test recommend_by_mood:'), nl,
    limited_results(recommend_by_mood(felice, T, A), 20).

test_is_relaxing :-
    write('Test is_relaxing:'), nl,
    limited_results(is_relaxing(T, A), 20).

test_is_energetic :-
    write('Test is_energetic:'), nl,
    limited_results(is_energetic(T, A), 20).

test_is_danceable :-
    write('Test is_danceable:'), nl,
    limited_results(is_danceable(T, A), 20).

test_happy_track_with_high_valence :-
    write('Test happy_track_with_high_valence:'), nl,
    limited_results(happy_track_with_high_valence(T, A), 20).

% === Test su subset limitato per similar_tracks_by_energy ===
test_similar_tracks_by_energy_limited :-
    write('Test similar_tracks_by_energy su sottoinsieme ridotto:'), nl,
    findall(T, has_energy_limited(T, _), AllTracks),
    sort(AllTracks, Unique),
    prefix(Unique, LimitedTracks, 50),
    find_limited_similar_pairs(LimitedTracks, Pairs),
    prefix(Pairs, FinalPairs, 20),
    print_pairs(FinalPairs).

find_limited_similar_pairs([], []).
find_limited_similar_pairs([T1|Rest], AllPairs) :-
    has_energy_limited(T1, E1),
    findall((T1, T2), (
        member(T2, Rest),
        has_energy_limited(T2, E2),
        Diff is abs(E1 - E2),
        Diff =< 0.1
    ), Pairs1),
    find_limited_similar_pairs(Rest, PairsRest),
    append(Pairs1, PairsRest, AllPairs).

% Utility comuni
prefix(List, Prefix, N) :- length(Prefix, N), append(Prefix, _, List), !.
prefix(List, List, _) :- !.

print_pairs([]).
print_pairs([(A,B)|T]) :-
    format('  -> ~w ~w~n', [A, B]),
    print_pairs(T).
