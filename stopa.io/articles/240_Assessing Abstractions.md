# Assessing Abstractions


Some abstractions are ticking time bombs, while others help you move fast. How
can you tell? What follows is my personal exploration for how I assess
abstractions.

### Problem

We add abstractions in our programs to solve problems. So, let’s start with
the fundamental value proposition: what problem does our abstraction solve?

Let’s take a look at one example abstraction:

[code]

    NLP.parse(...) // => { intent: "set_alarm", at: "1593538633430" }
[/code]

This could be a natural language processing abstraction, which lets us take a
piece of text, and extract meaning from it. The inherent problem of natural
language processing is pretty darn complex, so an abstraction that helps us
solve it would be very valuable. This is a sign of a good abstraction.

Now let’s compare that to

[code]

    StringSplitter.easySplit(str, splitStr)
[/code]

Maybe this abstraction, adds a light layer on top of string.split. For
example, it may make it so you don’t have to worry about regexes, and can turn
common string patterns into regexes. The value of a `StringSplitter`
abstraction is pretty darn low. Maybe `StringSplitter` treats `splitStr` in a
way that’s a bit more in-line with the someone’s thinking, but at the end of
the day this boils down to an indirection.

This leads us to the first principle. The more complex the problem it solves
for you, the better the abstraction (1).

### Interface

After we’re convinced that the abstraction we are about to add solves a tough
problem for us, the next thing to consider is the interface: _how_ do we
interact with the abstraction? Imagine if `NLP.parse` was called like this:

[code]

    NLP.parse(lang, text)
[/code]

This is a great interface. It’s small. We don’t need to understand any
internals. For the main use-case, all we need to do is to provide language and
text. Compare that with

[code]

    NLP.parse(
      text,
      lang, 
      strategy,
      shouldUseFlagA,
      ...
      shouldUseFlagZ
    )
[/code]

In order to use this version, we’d need to deeply understand the internals of
NLP.parse. This lowers the value of the abstraction, because we need to do
more work to solve the same level of complexity.

This leads us to the second principle: **great abstractions have small
interfaces.**

### Breakthrough Cost

Now that we have an abstraction with a simple interface that solves a hard
problem, we need to ask a possibly fatal question: what happens when we need
to break through the abstraction?

All abstractions are leaky at some point. What will happen when you need the
abstraction to behave differently? What will happen when it doesn’t work as
you expect?

For example, for `NLP.parse(lang, text)`, what if we needed to sort and score
the results differently? What if there’s a bug, and we aren’t getting the
entity we expect, can we look through and debug?

Understanding the answer to this, will give us the breakthrough cost. To do
this, we need to peak through the code. How is `NLP.parse` implemented?

[code]

    parse(lang, text) { 
      return format(scoreEntities(fetchEntities(lang, text)))
    }
[/code]

In one solution, it could be composed of other abstractions that we can take
advantage of. This is a great sign, because we can reuse the underlying
abstractions in cases where we need to do something more complicated. Compare
that to

[code]

    parse(lang, text) { 
      internalParse(lang, text, flagA, flagB, ...flagZ)
    }
[/code]

This feels more dangerous. If these flags all head to the same function, it’s
a sign that a bunch of different features are complected together. It’s also
worrying: what if one of these flags don’t do what you want? you may have to
fork the abstraction.

This leads us to the third principle: **great abstractions are transparent.**
I think this principle is the most overlooked. It’s easy to take the
productivity win upfront, but if the abstraction you add can’t be changed, and
can’t be introspected, it’s very likely to bite you at some point.

### Generality

The final principle is orthogonal to the last three, but maybe it’s the most
important. Hardy said _there is no permanent place in the world for ugly
mathematics —_ So it is with abstractions. The beauty in math relates to how
“general” and “tight” the solution is. I think this parallels well with
abstractions.

If you use an abstraction that is “essentially” simpler, it’s more likely to
last, and it’s likely to be more powerful.

Consider if the abstraction for `NLP`, was made up of specific algorithms,
_just_ for natural language processing. This would still be very valuable, but
what would be _even more_ valuable, is if the abstractions that this library
was composed of was more general: if the parts that compose it were deep
learning abstractions, you could reuse them for other problems.

### Fin

And we reach the end. To pick great abstractions: pick the ones that solve a
complex problem for you. Make sure they have a simple interface, and take a
look at the internals, so you’re confident you can jig things up if needed.
The more general and simple you can get for the same amount of power, the
better.

Want to see some great abstractions in the wild? First, chances are you are
using many of them: TCP, higher order functions like map & filter, React. Some
you may not have explored: Go’s CSP, Rich Hickey’s Datomic, or his `seq`
abstraction in Clojure. As you pick up abstractions, I encourage you to run
each one as an experiment: ask yourself at the end how things went, discuss
them with your friends, and soon you’ll develop a much more nuanced taste.

(1) The rabbit hole gets deeper. Even if an abstraction solves a complex
problem you have, you may need to take a step back and also ask: why do I have
this problem? For example, kubernetes may be a great solution to building
distributed systems, but why do you have a distributed systems problem? Many
times the problem itself can be avoided. For the answer to that, [Hacker’s
Paradise](https://stopa.io/post/241) tries to covers it.

 _Thanks to Alex Reichert, Daniel Woelfel, Martin Raison, Sean Grove for
reviewing drafts of this essay_

