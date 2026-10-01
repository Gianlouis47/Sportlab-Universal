# MLB pitcher profiles

Each starter receives both raw metrics and a style profile.

## Raw metrics
- ERA / xERA / FIP when available
- K%, BB%, K-BB%
- K/9
- whiff%, CSW%
- pitch mix and velocity
- called-strike/contact/chase metrics when available
- IP/start, BF/start, pitch count
- handedness and splits
- L5/L10 starts or recent workload window
- pitcher vs opponent history
- expected IP and expected BF

## Pitcher style

Do not label from reputation alone.

Derived profile:
- STRIKEOUT: high K%, whiff/CSW and swing-miss profile
- CONTACT: low K%, lower whiff, relies more on balls in play
- HYBRID: between both

Store a continuous strikeout_orientation score 0–100 plus the categorical label.

## Strikeout projection

Expected K should combine:
- pitcher talent baseline;
- opponent K/contact;
- handedness split;
- pitch-mix matchup;
- whiff/CSW;
- pitcher-vs-opponent prior;
- expected IP/BF;
- pitch-count/workload;
- bullpen/context.

For each sportsbook line, calculate win/push/loss separately. A line of 5.0 is not equivalent to 5.5.
