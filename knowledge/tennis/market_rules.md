# Tennis market settlement and slate checks

For each requested ATP/WTA slate, use the user's timezone, an official order of
play, the current draw and results. Distinguish fixed start times from
"followed by". Exclude players eliminated earlier in the event. Review all
scheduled singles matches before selecting a small parlay; never use ranking
or one external projection alone as proof that a result is guaranteed.

Keep three match markets separate:

| Market | Calculation | Example: A wins 6-3, 4-6, 6-2 |
| --- | --- | --- |
| Moneyline | Match winner | A wins two sets to one |
| Player A total games | Sum only A's games across completed sets | 6 + 4 + 6 = 16 |
| Match total games | Sum both players' games across completed sets | 16 + (3 + 6 + 2) = 27 |

At 6-6, each player has won six games in the current set. A regular tiebreak
adds one game to the winner: 7-6 means seven individual games for the set
winner, six for the loser and thirteen jointly. Tiebreak *points* do not
count as additional games. Example: A wins 7-6, 6-3, so A has 13 individual
games, the opponent has nine, and the match total is 22. These ATP/WTA tour
singles matches normally use best of three sets. For a line of 15.5, exactly
16 games wins the over; for 16.5 it loses. Check the operator's exact market
label, withdrawal and push rules before grading a bet.

A high ML estimate does not determine a 2-0 score, a tiebreak, the match
total or either player's total. Assess those separately from serve and return
rates, opponent quality, surface, recent nonoverlapping samples and a
calibrated scoring model. If unavailable, display NO ESTIMABLE rather than
deducing a total from ML. For a parlay, all legs must win; report the combined
chance only when constituent probabilities and dependence are defensible.

Betcris settlement reference:
https://ayuda.betcris.com/es/aprende-a-apostar/apuestas-deportivas/tenis/
