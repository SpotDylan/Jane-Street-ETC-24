# JaneStreet-ETC-24
Dylan's Submission for the Jane Street Electronic Trading Competition during the Academy of Math and Programming 2024


# Intuition
Initially, we figured a spread strategy could be the most profitable. The idea would be to buy at the last market price and liquidate/cover for `+$1/-$1`. This strategy was largely unsuccessful because the fair market price was not exactly just the last transaction price. We attempted to re-implement the strategy, but we used the average of the last 5 trade prices for a security to determine an average.

# Post-Mortem
We placed 12th place with a final profit of $676,069. Our competition strategy was fairly simplistic, but it at least earned a net profit. After the competition, I tried to implement further strategies besides our simple spread strategy used in competition.

# Versions
There are two versions of this code. `bot` was directly what we submitted during the competition. All other versions were made after the competition. `bot-arbitrage-strategy` attempts to utilize an arbitrage strategy. `bot-spread-strategy` attempts to use a bid-ask strategy to make high-frequency trades. `botImproved` tries to merge the two. All post-mortem strategies are currently untested as I've been unable to access test servers.
