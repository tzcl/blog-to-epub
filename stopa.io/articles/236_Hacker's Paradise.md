# Hacker's Paradise


 _Note: this essay tries to answer the question “What is the essence of System
Design, and how do you do it?”. It covers broad strokes. At some point I hope
to go much deeper. Meanwhile, I hope you find this enjoyable :)_

* * *

What is a hacker’s paradise?

My vote would be the beginning years of a startup.

The whole system fits in your head. All your problems are important, and you
can solve them any way you like. You’re spinning clay while the world is
pouring concrete. If you love to create it’s easy to see: despite all the
schleps of a startup, an environment with speed, independence, and
changeability is paradise.

### Elephant

But we know this doesn’t last long. When those same startups become big, most
of them slow down to a crawl. Why is that?

In one of Rich Hickey’s talks, he made a metaphor that could explain it.
Paraphrased, he said “Your system grows into an elephant. Every new feature is
you teaching it new tricks”.

The larger and hairier the elephant, the harder it is to teach it tricks. And,
of course some tricks become off-limits: you can’t teach an elephant to do
backflips.

So companies slow down because their systems get large and hairy. Is that the
only reason? I don’t think so, but it is certainly one of the biggest. An
argument could be made for organizational issues: there’s a cost to lots of
people working together. But systems grow exponentially in size, so even if
everyone agreed and they worked together perfectly, I’d bet that system
complexity would take a fair amount of the blame.

### System Design

Taming that elephant, I think, is the essence of system design. So how do we
_do s_ ystem design?

A lot of complex ideas come to mind when we think about what’s involved:
Robustness, performance, stability, safety, scale. These are all important
concepts, but I think they are not the central goal.

The central goal is much simpler. It’s singular and defensive. Remember that
when we started, we already _had_ a hacker’s paradise, Our goal is to hold the
fort. To do this, just one idea encapsulates it all: changeability.
Changeability maximizes the impact an engineer can have on your system, and at
the end of the day it’s those engineers who can affect _any_ improvement to
your system. This means that robustness, performance, stability, safety,
scale, and all else are dependent on changeability.

System design is then the constant answer to the question: “How can I make my
system as changeable as possible?”. That’s a simpler question, but the answer
is no less difficult. Note one more surprising bit about it: we must answer
this question differently over time. This means that design is dependent on
time and context. Your answer can be right if applied at T0, but wrong if
applied at T200.

### Guide

Now, if making our system as changeable as possible is our primary act, how do
we do it?

First, we’ll need to start off with the _maximum level of changeability._
Systems that are maximally changeable are as simple as possible. A simple
system is the system that solves a problem with the minimum amount of specific
concepts, in a way that keeps all these concepts as decoupled as possible.

That implies a few things: we would want to choose the most powerful language
we can to solve our problem. This lets us use the most powerful abstractions,
which will allow us to keep the number of specific concepts that define our
program at a minimum. We would want to use powerful, immutable data
structures, which will help us keep our abstractions concise and decoupled. It
also means that we would want to use the simplest infrastructure we need to
solve our problem. Simpler infrastructure allows us to avoid introducing
concepts that aren’t needed to solve our problems. The same applies for the
abstractions we choose: we’d want to use the abstractions that best solve for
our specific use cases, rather than solve generally for potential future
usecases we don’t have.

Note that if you follow these ideas, your initial system may look like a toy.
It certainly won’t use kubernetes. Remember that system design is context-
dependent, and at this point in time this _is_ the best solution.

Now, we must iterate. At every step of the way, ask: what’s slowing down our
productivity? Pick the highest impact issues and start to address them.
Privacy getting too hairy? Introduce an abstraction that centralizes the
complexity of privacy, and removes it from the realm of product engineering.
Site going down too much? Introduce infrastructure for detection and
debugging. Once that’s not enough, consider incident management systems.

The common theme here: centralize and push complexity down. You take pieces of
complexity that _every_ engineer needs to deal with, and create an interface
they can use which abstracts the complexity away. As you do that, you try to
make that infrastructure accessible: this means it’s written in a place where
every engineer can access, in a language that every engineer can change. That
will enable all engineers to use your abstraction, while having the option to
dive deeper.

The fact that system design is iterative has two importance consequences.

The first is that you cannot escape technical debt. Because a solution at T0
becomes more and more incorrect as context changes, you are constantly
accruing technical debt. Because of this, _there can be no perfect system._
It’s your job to constantly manage the tradeoff between quality and debt, and
this iterative cycle is your sword.

The second is that applying blanket solutions will lead to failure. As you get
more technical debt, you will invariably end up with a desire to enforce a new
paradigm on the system: microservices being the common one today. Because a
paradigm solves _multiple_ general * _issues, you invariably introduce some
concepts that don’t_ specifically _solve your issues, and have their own
tradeoffs. The solution is again to lean in to the iterative model: apply_
specific _solutions to_ specific _problems_.*

### Debt

As you iterate, you’ll constantly run into the struggle between accruing and
paying down debt: do you slow down your velocity _now_ to improve future
changeability _later_? The context we work in is so complicated that there
can’t be a simple formula here. But, like in most craft, we can lean in rules
of thumb.

The first problem comes when you are considering _introducing_ new debt. The
key rule to consider here is the nature of the debt. Not all debt are created
equal — some have higher interest. Let’s compare two examples to illustrate.
The first involves introducing a staging environment, or improving
performance. This does not get appreciably harder _later._ Compare that to
knowingly introducing a data model change, that you _know_ you’ll need to
migrate later. This involves significantly more incidental work: dual writes,
backfills, shadow testing, the whole schebang. Based on the nature of the debt
and the importance of your current commitments, you need to balance and make a
choice.

The second problem comes when you are considering _paying down_ debt. The key
rule to consider here is pain. You already have a sense of the debt that is
either causing the biggest slow down, or is about too. It’s difficult to
measure your success here, as if you do your job well, no one will even feel
the pain. Nevertheless this skill can be learned from your mistakes. First fix
what causes the most pain immediately. Then, get better and better at pre-
empting the largest amount of pain earlier. That, granted is a lofty goal — I
have never worked at a company where there wasn’t at least one glaring way to
make things a magnitude better.

### Fin

So we come down to the central idea. To keep your hacker’s paradise you need
to tame your system complexity elephant. To do that, you need to keep your
system as changeable as possible. To do that, you need to start out with a
simple system, and evolve it iteratively as you grow. There’s so much more I
want to go deeper into, but that will have to wait for another. I hope this
gives you a good model to think with.

 _Thanks to Mark Shlick, Jacky Wang, Daniel Woelfel, Irakli Popkhadze, David
Magaltadze, Irakli Safareli, for reviewing drafts of this essay_

