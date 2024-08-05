# JaneStreet-ETC-24
Submission for the Jane Street Electronic Trading Competition 2024

# Intuition
Initially, we figured a spread strategy could be the most profitable. The idea would be to buy at the last market price and liquidate/cover for '+$1/-$1'. This strategy was largely unsuccessful because the fair market price was not exactly just the last transaction price. We attempted to re-implement the strategy, but we used the average of the last 5 trade prices for a security to determine an average.

# Post-Mortem
We placed 12th place with a final profit of $676,069. Our competition strategy was fairly simplistic, but it at least earned a net profit.

# Versions
There are two versions of this code. `bot` was directly what we submitted during the competition. `botImproved` is what I improved on post-competition, although this is untested as we have not been able to pass this through the servers.
