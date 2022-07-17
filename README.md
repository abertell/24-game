# 24-game
Fast 24 game solver in Python, feasible for up to 8 numbers (realistically 7).

Allowed operations are +, -, \*, /, ^. No fractional exponentiation, since Python has no idea how to evaluate (-8)\*\*(1/3), and I'm not rewriting exponentiation from the ground up (yet).

I could make this an order of magnitude faster by searching from the end as well, but that would require inverse exponentiation, which, as mentioned above, is a pain.
