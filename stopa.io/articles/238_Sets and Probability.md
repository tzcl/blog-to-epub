# Sets and Probability


I’ve been a big fan of Nassim Taleb’s Incerto. He wrote a series of essays on
life, where all the topics revolve around decision making under uncertainty. I
wanted to dig deeper on some of the more technical concepts he alluded too, so
last year I explored a few textbooks on probability theory.

I was surprised with how elegant the field was. The most inspiring idea to me
was how the originators interpreted probability through set theory. Not only
is it a beautiful way to look at things, but by seeing it this way, they could
apply few axioms, leverage set theory, and badabing badaboom they had a whole
field’s worth of discoveries.

I wanted to share with you an example from one of the textbooks, that
illustrated the power of seeing probability through this lens, and
demonstrated how you could begin deriving complex ideas from the simplest
kernel.

### Boxes and balls

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzgzMDUxODM5LTYwNThjZDgwLWEwMDMtMTFlYS04YjE0LWQ2ODhiZGY0Y2MwMC5wbmc)

Let’s say you have 2 boxes. In Box 1, you have 99 red balls, and 1 white ball.
In Box 2, you have 99 white balls, and 1 red ball.

 **You pick a box at random, then, you pick a ball from that box.**

### Question 1: What’s the chance that you pick a red ball?

#### Memory

This can get a bit tough to reason about. There’s a 50% chance you pick Box 1.
In Box 1, you have a 99% chance. If you picked Box 2, you have a 1% chance.
How do we combine these probabilities together?

If you reason the way you were taught in high school, you may think like this:

Well, there’s a 50% chance I pick Box 1, and a 99% chance after that to pick a
red ball And, there’s a 50% chance I pick Box 2, and a 1% chance after that to
pick a white ball.

So the total probability can be `50% * 99% + 50% * 1%`

Which is 49.5% + 0.5% which is…50%

Now this will work, but notice how the probability was 50% — Did you really
need to do all that work to figure this out? (1)

#### Intuition

Let’s reimagine what _probability_ here means. First, let’s consider: what are
_all_ _the possible outcomes_?

For out experiment, an outcome must contain two choices: The box we chose, and
the ball we chose after that. We could represent it like this:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzgzMDUxODc0LTZlYTZlOTgwLWEwMDMtMTFlYS05YTNlLTA1MjEyY2MxM2M2OC5wbmc)

This is _one outcome — we picked Box 1, then picked Red Ball 1._

How many of these outcomes do we have?

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzgzMDUxOTE2LTdiYzNkODgwLWEwMDMtMTFlYS05ZTU0LWE0ZWQzNzVhOTBkMS5wbmc)

We can list it out: we pick Box 1, Red Ball 1, Box 1…Red Ball 99, etc. In
total, we would have 200 possible outcomes.

Now that we have all the outcomes in mind, we can answer the question: _what’s
the probability that we pick a red ball?_

Well, how many outcomes contain a “red ball”?

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzgzMDUxOTYwLTg4NDgzMTAwLWEwMDMtMTFlYS05NjVhLTczNGJiNjRlMDE3ZC5wbmc)

Looks like 100. This means that 100 of 200 outcomes would give us the result
“we got a red ball” — 100/200 makes 50%

Note how this boiled down to just “counting” the outcomes we cared about. Is
it really that easy? Let’s try with a harder example.

### Question 2: You picked a red ball, what’s the probability that it came
_from_ Box 1?

#### Memory

This question can get pretty hairy to answer from what we learned in high
school. _Given_ that we chose a red ball, what’s the chance that it was Box 1?
Well, there are 99 red balls in Box 1, and only 1 red ball in Box 2, so the
chance that it came from Box 1 is _very high._ But how high?

We may recall Bayes Theorem here, but the formula can be hard to remember.

#### Intuition

However, if we think in sets, we can _kind of_ derive Bayes Theorem. Let’s
look at our outcomes again:

![](https://stopa.io/api/image/aHR0cHM6Ly9wYXBlci1hdHRhY2htZW50cy5kcm9wYm94LmNvbS9zX0RERUJEQUI4NDM4RTBDRTI1QkUzNjUyNDEyQ0NDNkE4NENCMEE2OTBBQjlFMTBGMzFFMzE0NENCRTE5NjJGOURfMTU5MDUyODI4MDUzNF9pbWFnZS5wbmc)

How many of these outcomes contain “red ball”?

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzgzMDUyMTQ1LWJkZWQxYTAwLWEwMDMtMTFlYS04NGU3LTVlNDIzNzQ3N2VjNi5wbmc)

Yup, 100 total. Since we _know_ we got a red ball, this means that we could
have _only gotten_ one of these 100 outcomes.

Out of these outcomes, how many come from “Box 1”?

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzgzMDUyMTcyLWM2ZGRlYjgwLWEwMDMtMTFlYS04MTU3LTg0YWVjMjA4YTBlZi5wbmc)

That's 99 outcomes. So out of 100 outcomes that could have happened, 99 of
those came from Box 1. 99/100 and you have a 99% chance that given a red ball,
it came from Box 1.

This too, just came down to counting the number of outcomes. Now, it can get a
lot more difficult — what if you can’t possibly count the number of outcomes?
what if each outcome has a different probability? But, just from this notion
of events forming a set of possible outcomes, we can chug along and derive out
quite a bit.

(1) Alexandre came up with a pretty beautiful intuitive solution to question
1: consider symmetry — since the problem is symmetric (you can reverse white
and red), it implies the only solution could be 50%

 _Thanks to Daniel Woelfel, Alexandre Lebrun, Bipin Suresh, Mark Shlick, Davit
Magaltadze for reviewing drafts of this essay_

