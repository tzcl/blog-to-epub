# What Gödel Discovered


In 1931, a 25-year-old Kurt Gödel wrote a proof that turned mathematics upside
down. The implication was so astounding, and his proof so elegant that it
was...kind of funny. I wanted to share his discovery with you. Fair warning
though, I’m not a mathematician; I’m a programmer. This means my understanding
is intuitive and not exact. Hopefully, that will come to our advantage since I
have no choice but to avoid formality 🙂. Let’s get to it.

## Unification

For the last 300 years, mathematicians and scientists alike made startling
discoveries, which led to one great pattern. The pattern was unification:
ideas that were previously thought to be disparate and different consistently
turned out to be one and the same!

Newton kicked this off for physicists when he discovered that what kept us
rooted on the Earth was also what kept the Earth dancing around the sun.
People thought that heat was a special type of energy, but it turned out that
it could be explained with mechanics. People thought that electricity,
magnetism, and light were different, but Maxwell discovered they could be
explained by an electromagnetic field.

Darwin did the same for biologists. It turned out that our chins, the
beautiful feathers of birds, deer antlers, different flowers, male and female
sexes, the reason you like sugar so much, the reason whales swim
differently...could all be explained by natural selection.

Mathematicians waged a similar battle for unification. They wanted to find the
“core” principles of mathematics, from which they could derive all true
theories. This would unite logic, arithmetic, and so on, all under one simple
umbrella. To get a sense of what this is about, consider this question: How do
we _know_ that 3 is smaller than 5? Or that 1 comes before 2? Is this a “core”
principle that we take on faith (the formal name for this is called an
“axiom”) or can this be derived from some even more core principle? Are
numbers fundamental concepts, or can they be derived from something even more
fundamental?

## Crisis

Mathematicians made great progress in this battle for core principles. For
example, a gentleman called Frege discovered that he could craft a theory of
sets, which could represent just about everything. For numbers, for example,
he could do something like this:

![A demonstration of how to represent numbers with
sets](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk5MjkyOTc0LWZhMTE3MjgwLTI4MGYtMTFlYi05MTM1LTVkYjRkZWFlZjgzYy5wbmc)

Here, he represents 0 the empty set. 1 as the set which contains the set for
0. 2 as the set that contains the set for 1 and 0. From this he could set a
principle to get the “next” number: just wrap all previous numbers in a set.
Pretty cool! Frege was able to take that and prove arithmetic rules like “1 +
1”, “numbers are infinite”, etc.

This looked formidable and cool, but Bertrand Russell came along and broke the
theory in one fell swoop.

He used the rules that Frege laid out to make a valid but _nonsensical_
statement. He proved something analogous to 1 + 1 = 3 [1]. This sounds
innocuous; it was after-all just _one_ statement. But nevertheless it was
disastrous for a foundational theory of mathematics. If you could prove that 1
+ 1 = 3, then you can’t really trust any true statement that results from this
foundation.

This put mathematicians on a tail-spin. They even dubbed this period the
“Foundational Crisis of Mathematics”

## Hilbert’s Program

In an effort to solve this problem, a mathematician called Hilbert laid down
some requirements for what a fundamental theory of mathematics had to look
like [2]. He said that this theory must be a new language, with a set of rules
that satisfied two primary constraints:

The theory would need to be able to prove _any_ true mathematical statement.
For example, imagine the statement 1 + 1 = 2. If this language can’t prove
that statement, then it certainly can’t prove all of mathematics. Hilbert
called this quality **completeness.** The language would need to be complete.

The second hard requirement, as we discussed earlier, was that it _could not_
prove a false mathematical statement. If we could prove 1 + 1 = 3, then all
was for naught. Hilbert called this **consistency.** The language would need
to be consistent.

## Russell and Whitehead

Bertrand Russell, the gentleman who broke Frege’s theory, worked together with
Alfred North Whitehead to develop a theory of their own. They labored for
years to craft an immense volume of work, called Principia Mathematica [3].

They started by writing a new language (let’s call it PM) with a few simple
rules. They took those rules, and proceeded to prove a bunch of things.
Russell and Whitehead took almost nothing on faith. For example, let’s look at
this almost-impossible-to-read proof over here (don’t worry, you don’t need to
understand the syntax for this essay):

![An example, very hard-to-read proof from Principia
Mathematica](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk5MjkzMDA0LTA0Y2MwNzgwLTI4MTAtMTFlYi05ZGJkLTRkMTlmYmQxMDM2My5wbmc)

This proof showed that “1 + 1”, does indeed equal “2”. It took 2 volumes to
get here.

Their language was dense and the work laborious, but they kept on proving a
whole bunch of different truths in mathematics, and so far as anyone could
tell at the time, there were no contradictions. It was imagined that at least
in theory you could take this foundation and eventually expand it past
mathematics: could you encode in pure logic how a dog behaves, or how humans
think?

## Gödel Comes Along

It certainly looked like Principia Mathematica could serve as the foundational
theory for Mathematics. Until Gödel came along.

He proved that Principia Mathematica _did indeed have_ true mathematical
statements which _could not be proven_ in the language. Principia Mathematica
was incomplete.

This was startling, but his proof went even further. He showed that the entire
enterprise behind Hilbert’s Program — to find a formal foundation for
mathematics — could _never_ work.

It’s hard to believe that a person could really prove that something can
“never” happen. Yet here Gödel was...a 25 year-old who proved beyond a doubt
that this enterprise was impossible. He did this by showing that if a language
could represent numbers, then unprovable statements would necessarily pop up.

Let’s think about that for a second: Numbers seem so quaint and easy to prove
— just “1”, “2”, “3”...so on. People thought we could eventually write down
how humans think — imagine how shocked they must have been to see that we
couldn’t prove all truths about...numbers.

Let’s see how Gödel did it.

## PM-Lisp

Now Russel and Whitehead’s language was hard to read. There’s no harm done in
changing some of their symbols around. Let’s map their language to something
more amenable to programmers: Lisp!

You can imagine that Russell and Whitehead came up with a lisp-like language.
Here’s how their syntax looked:

First, they had a few symbols for arithmetic.

 **Symbol**

 **Meaning**

 **Example**  
  
0

zero

`0`  
  
next

the next successor

`(next 0)`  
  
+

plus

`(+ 0 (next 0))`  
  
*

times

`(* 0 (next 0))`  
  
=

equals

`(= 0 (* 0 (next 0)))`  
  
Just from these symbols, they could represent all natural numbers. If they
proved that the symbol `0` worked like 0. and the symbol `next` worked like a
successor function, then `(next 0)` could represent 1, `(next (next 0))` could
represent 2, and so on.

Here’s how they could write `1 + 1 = 2`:

[code]

    (= (+ (next 0) (next 0)) 
       (next (next 0)))
[/code]

Now, for the purpose of this essay, I’ll add one rule. If you ever see me
using a natural number inside PM-Lisp other than 0 (i.e “15”), you can imagine
it’s shorthand to writing `(next (next (next ...))))` that many times. In this
case, “15” means `next` applied to 0, 15 times

 **Symbol**

 **Meaning**

 **Example**  
  
`<natural-number>`

`(next (next ...))` applied to `0` `<natual-number>` times

`3`  
  
 _means_ `(next (next (next 0)))`  
  
(Next (pun-intended)), they came up with some symbols to represent logic:

**Symbol**

 **Meaning**

 **Example**  
  
not

not

`(not (= 0 1))`  
  
or

or

`(or (= 0 1) (not (= 0 1)))`  
  
when

when ... then ..

`(when 0 (or 0 1))`  
  
 _when 0, then there is either 0 or 1_  
  
there-is

there is ... such that ...

`(there-is x (= 4 (* x 2))`  
  
These symbols map closely to the logical statements we are used to in
programming. The most unusual one is `there-is`. Let’s see one of those for an
example:

[code]

    (there-is x (= 4 (* x 2)))
[/code]

This is making a statement, that there is some number `x`, such that `(* x 2)`
equals 4. Well, that is indeed true: `x = 2`. That’s pretty cool — we’ve just
made a general arithmetic statement.

Where did the `x` come from though? Oops, we need to account for that in our
language:

 **Symbol**

 **Meaning**  
  
a...z, A...Z

variable  
  
In order to represent general truths, Russell and Whitehead introduced
variables. Here’s how they could derive `and` for example:

[code]

    (not (or (not A) (not B)))
[/code]

When this statement is `true`, both `A` and `B` must be true!

Very cool. One more trick for our essay. To make it a bit easier to read,
sometimes I’ll introduce new symbols. They won’t actually be a part of the
language, but it can make good shorthand for us in the essay

 **Form**

 **Meaning**

 **example**  
  
`(def <name> <formula>)`

define `<name>` to represent `<formula>`

`(def and (not (or (not A) (not B)))`  
  
 _same as_ `(and <var-a> <var-b>...)`  
  
Now we can write `(and 1 2)` 🙂

## PM-Lisp Axioms

All we saw above were _symbols._ They had no meaning yet.

Russell and Whitehead needed to prove that `0` works like zero, and that `=`
works like equals. In order to breathe life into those symbols, they started
off with some core principles — the axioms.

Here’s what they chose:

**Axiom**

 **Example**  
  
`(when (or p p) p)`

when either apples or apples, then apples  
  
`(when p (or p q))`

when apples, then either apples or bananas  
  
`(when (or p q) (or q p))`

when either apples or bananas, then either bananas or apples  
  
`(when (or p (or q r)) (or q (or p r))`

when either apples, bananas, or pears, then either bananas, apples, or pears  
  
`(when (when q r) (when (or p q) (or p r))`

when apples are a fruit, then bananas or apples implies bananas or fruits  
  
That’s it. This is all we needed to take them on faith for. They took these
rules and laboriously combined them in intricate ways to derive everything
else.

For example, here’s how they derived `=`:

[code]

    (def = (and (when A B) (when B A)))
[/code]

If A implies B, and B implies A, they _must_ be equal! Imagine this done for
hundreds and hundreds of pages.

Note something essential here: their rules are so precise that there is no
room for human judgement; a computer could run them. This was a key component
for a foundational theory of mathematics: if the rules were so simple that
they could be run as an algorithm, then we could side-step errors in human
judgement.

## Gödel’s First Idea

Now, Gödel wanted to study Russell and Whitehead’s language. But, it’s hard to
study symbols. How do you reason about relationships between them?

Well, there there is one thing you can study very well...numbers! So he came
up with an idea: what if he could express all of PM-Lisp with numbers _?_

This is what he did:

### Symbols

First, he took all the symbols and assigned a number to them:

 **Symbol**

 **Gödel Number**  
  
(

1  
  
)

3  
  
0

5  
  
next

7  
  
+

9  
  
*

11  
  
=

13  
  
not

15  
  
or

17  
  
when

19  
  
there-is

21  
  
a

2  
  
b

4  
  
c

6  
  
...

...  
  
Now, say he wanted to write `when`. He could just write `19`. This is good but
doesn’t cover much: how would he represent formulas?

### Formulas

He crafted a solution for formulas too. He made a rule:

Take any formula, like this one:

[code]

    (there-is a (= (next 0) a))
[/code]

and convert each symbol to the corresponding Gödel Number:

 **token**

(

there-is

a

(

=

(

next

0

)

a

)

)  
  
 **Gödel Number**

1

21

2

1

13

1

7

5

3

2

3

3  
  
Then take the list of ascending prime numbers, and set each one to the power
of the Gödel Number:

**prime** **Gödel** **Number**

2¹

3²¹

5²

7¹

11¹³

13¹

17⁷

19⁵

23³

29²

31³

37³  
  
Multiply them all together, and you get this one huuge number:

[code]

    25777622821258399946386094792423028037950734506637287219050
[/code]

There’s something very interesting about this number. Because it is comprised
only of ascending prime numbers, it’s _guaranteed_ to be unique! This means
that he could represent _every_ formula of PM-Lisp, with a unique Gödel
Number!

### Proofs

Formulas are great, but they’re not all of PM-Lisp. We’d also want to support
proofs. In a proof, we would have a “sequence” of formulas:

[code]

    (there-is a (= (next 0) a)) 
    (there-is a (= a (next 0)))
[/code]

He applied the same trick again, but this time over each individual formula:

 **Gödel Formula**

`(there-is a (= (next 0) a))`

`(there-is a (= a (next 0)))`  
  
 **Gödel Number**

25777622821258399946386094792423028037950734506637287219050

76887114166817775146256448336954145299389470803180389491850  
  
 **prime Gödel Number**

225777622821258399946386094792423028037950734506637287219050

376887114166817775146256448336954145299389470803180389491850  
  
Now if we took

[code]

    2^25777622821258399946386094792423028037950734506637287219050 * 3^76887114166817775146256448336954145299389470803180389491850
[/code]

We’d have one ginormous number. Just the first term in this calculation has 7
octodecillion _digits_! (1 octodecillion has 58 digits itself) But we’d have
something more. This ginormous number uniquely represents the proof we just
wrote!

All of a sudden, Gödel could represent symbols, formulas, and _even_ proofs,
uniquely with Gödel Numbers!

## PM-Lisp on PM-Lisp

Now, we can use math to study relationships between numbers: for example “how
are even numbers and prime numbers related?”, “are prime numbers infinite?”
and so on. In the same way that we could use math to study prime numbers,
Gödel realized that he could use math to study “all the numbers that represent
PM-Lisp proofs”!

Now, what language could he use to study these relationships? Well, Russell
and Whitehead made sure PM-Lisp itself was great for studying numbers...and it
certainly worked well for studying primes...so why not use PM-Lisp to study
“all the numbers that represent PM-Lisp proofs”?

And that’s exactly what Gödel did: he used PM-Lisp...to study PM-Lisp!

It’s certainly not what Russell and Whitehead had intended, but it was
nevertheless possible. Let’s take a look at some examples, to get a sense of
what we mean.

### Describing formulas

Say you had a formula like this:

[code]

    (there-is a (= (next 0) a)) 
[/code]

What if we wanted to prove the statement “The second symbol in this formula is
‘there-is’”?

Well, if we had the Gödel Number for this:

[code]

    25777622821258399946386094792423028037950734506637287219050
[/code]

All we’d have to do, is to say in PM-Lisp:

“The largest 3* factor of this Gödel Number is 321”.

If we said that...it would be equivalent to saying that the _second_ symbol
(the prime number 3), is “there-is” (Gödel Number 21)! Very cool.

Well, that relationship is trivial to say in PM-Lisp. Let’s start by writing a
formula to check if a number is a factor of another:

[code]

    (there-is x (= (* x 5) 30))
[/code]

This statement says that there is an `x` such that `(* x 5)` must equal `30`.
If `x = 6`, this works out, so the statement is true. Well, that maps to the
idea that 5 is a factor of 30! So let’s make this a “factoring” shortcut:

[code]

    (def factor? (there-is x (= (* x y) z)))
[/code]

We can then use `factor?` for our statement:

[code]

    (and
      (factor? x 3^21 25777622821258399946386094792423028037950734506637287219050)
      (not (factor? x 3^22 25777622821258399946386094792423028037950734506637287219050)))
[/code]

This statement says that 321 is a factor of our number, and that 322 is not.
If that is true, it means that 321 is the largest 3* factor in
`25777622821258399946386094792423028037950734506637287219050`. And if [that is
true](https://www.wolframalpha.com/input/?i=factorize+25777622821258399946386094792423028037950734506637287219050),
then PM-Lisp just said _something_ about that formula: it said the second
symbol _must_ be `there-is`!

### Constructing formulas

We can go further. We can even _construct_ PM-Lisp formulas in PM-Lisp!
Imagine we had a bunch of helper statements for primes and exponents:

[code]

    (def prime? ...) ; (prime? 5) ; true
    (def largest-prime ...) ; (largest-prime 21) ; 7
    (def next-prime ...) ; (next-prime 7) ; 11
    (def expt ...) ; (expt 10 3) ; 1000
[/code]

Since PM-Lisp is all about math, you can imagine Russell and Whitehead went
deep into primes and gave us these handy statements. Now, we could write a
formula that “appends” a `)` symbol, for example:

[code]

    (* n (expt (next-prime (largest-prime n)) 3))
[/code]

Say `n` was the Gödel Number for `(there-is a (= (next 0) a))`.

Here’s what that statement says:

  * Find the largest prime for `n`: 37
  * get the next prime after that: `41`
  * Multiply `n` by 413

Multiplying `n` by 413 would be equivalent to appending that extra `)`! Mind
bending.

## (successor? a b)

Now, Gödel started wondering: what other kinds of statements could we
construct? Could we make a statement like this:

[code]

    (successor? a b)
[/code]

This would say: “the formula with the Gödel Number `a` implies the formula
with the Gödel Number `b`.”

It turns out...this is a valid, provable statement in PM-Lisp! The
mathematical proof is a bit hard to follow, but the intuitive one we can grasp
well.

Consider that in PM-Lisp, to go from one statement to the next statement, it
_must_ boil down to one of the axioms that Russell and Whitehead wrote out!

For example from the sentence `p`, we can apply the axiom `(when p (or p q))`,
so one valid next statement can be `(or p q)`. From there, we can use more
axioms: `(when (or p q) (or q p)` can help us transform this to `(or q p)`.
And so on.

We already saw that we can use PM-Lisp, to “change” around formulas (like how
we added an extra bracket at the end). Could we write some more complicated
statements, that can “produce” the next possible successors, from a statement
and those axioms?

As one example, to go from `p` to `(or p q)` we’d just need a mathematical
function that takes the Gödel number for `p`, and does the equivalent
multiplications that prepend `(or`, and appends `q)`.

Turns out, this _can_ be done with some serious math on prime numbers! Well,
if that’s possible, then we _could_ check whether the _next_ statement in a
sequence is valid:

[code]

    (def successor?
      (one-of b (possible-successors a)))
[/code]

This statement says “one of the possible successor Gödel Numbers from the
formula with Gödel Number `a` , equals the formula with the Gödel Number `b`.”
If that is true, then indeed `b` must be a successor of `a`.

Nice! PM-Lisp can say that one formula implies another.

## (proves a b)

If we can prove that that a formula is a successor, can we say even more?

How about the statement `(proves a b)`. This would say: “the _sequence_ of
formulas with the Gödel Number `a` _proves_ the formula with the Gödel Number
`b`."

Well, let’s think about it. Getting a “list” of Gödel Number formulas from `a`
is pretty straight-forward: just extract the exponents on prime numbers. PM-
Lisp can certainly do that.

Well, we already have a `successor?` function. We could just apply it to every
statement, to make sure it’s a valid successor!

[code]

    (and 
      (every-pair sucessor? (extract-sequence a))
      (successor? (last-formula a) b))
[/code]

There’s a lot of abstraction over there that I didn’t talk about — `every-
pair`, `extract-sequence`, etc — but you can sense that each one is certainly
a mathematical operation: from extracting exponents to checking that a Gödel
Number is a proper successor.

The statement above would in effect say:

"Every formula in the sequence with the Gödel Number `a` are proper
successors, and imply the Gödel Number `b`."

Gödel went through a lot of trouble to prove this in his paper. For us, I
think the intuition will do. Using PM-Lisp, we can now say some deep truths
about PM-Lisp, like “this proof implies this statement" — nuts!

## (subst a b c)

There’s one final statement he proved. Imagine we had this formula

[code]

    (there-is b (= b (next a)))
[/code]

The Gödel number would be
`26699108848097731568417316859014651425159900891216992323750`

This says “There is a number `b` that is one greater than `a`.”

What if we wanted to replace the symbol `a` with `0`?

Well, this would be a hard but straight-forward thing: we just need to replace
all exponents that equal `2` in this number (remember that `2` is the Gödel
Number for the symbol `a`), with `5`. (the Gödel Number for `0` )

[code]

    (replace-exponent
      26699108848097731568417316859014651425159900891216992323750
      2 
      5)
[/code]

Again, this seems pretty straight-forward mathematical computation, and we can
sense that PM-Lisp could do it. It would involve a lot of math — extracting
exponents, plopping multiplications — but all within reasonable logical
realms.

Gödel proved that _this_ function was also a provable statement in PM-Lisp.
Our expression above for example, would produce the Gödel Number that
represented this formula:

[code]

    (there-is b (= b (next 0)))
[/code]

Wild! `a` replaced with `0`. PM-Lisp could now make substitutions on PM-Lisp
formulas. I imagine that when Russell and Whitehead saw this, they started
getting a little queasy.

## Suspicious use of subst

If they weren’t already queasy, this certainly would make them so:

[code]

    (subst 
      26699108848097731568417316859014651425159900891216992323750
      2 
      26699108848097731568417316859014651425159900891216992323750)
[/code]

This replaces `a`, with the _Gödel Number of the formula itself!_

In this case, the formula would now say:

[code]

    (there-is b (= b (next 25777622821258399946386094792423028037950734506637287219050))) 
[/code]

It’s weird to use the Gödel Number of a formula itself inside the formula, but
it _is_ a number at the end of the day, so it’s all kosher and logical.

Very cool: PM-Lisp can now say if a certain proof is valid, and it can even
replace variables inside formulas!

## Masterpiece

Gödel combined these formulas into a jaw-dropping symphony. Let’s follow
along:

He starts with this:

[code]

    (proves a b)
[/code]

So far saying “the sequence with the Gödel Number `a` proves the formula with
Gödel Number `b`”

Next, he brought in a `there-is`

[code]

    (there-is a (proves a b))
[/code]

So far saying “There is some sequence with the Gödel Number `a` that proves
the formula with the Gödel Number `b`"

Now, he popped in a `not`:

[code]

    (not (there-is a (proves a b)))
[/code]

This would mean

“There is _no_ sequence that proves the formula with the Gödel Number `b`"

Then he popped in `subst`:

[code]

    (not (there-is a (proves a (subst b 4 b))))
[/code]

Wow what. Okay, this is saying

“There is _no_ sequence that proves the formula that results when we take The
Gödel Number for `b`, and replace `4` (the Gödel Number for the symbol “b”)
with the _Gödel Number_ `*b*` itself!

So far so good. But what is `b` right now? It can be anything. Let’s make it a
specific thing:

What if we took the Gödel Number of

[code]

    (not (there-is a (proves a (subst b 4 b))))
[/code]

It would be an ungodly large number. Let’s call it `G`

Now, what if we replaced `b` with `G`?

[code]

    (not (there-is a (proves a (subst G 4 G))))
[/code]

Interesting...what is _this_ saying?

## Gödel’s Formula

Let’s look at it again:

[code]

    (not (there-is a (proves a (subst G 4 G))))
[/code]

This is saying: “There is no proof for the formula that is produced when we
take 'the formula with the Gödel Number `G`'” -- let’s remember that `G` is
the Gödel Number for:

[code]

    (not (there-is a (proves a (subst b 4 b))))
[/code]

“And replace `b` with with `G`"...which would result in the Gödel number for
the formula:

[code]

    (not (there-is a (proves a (subst G 4 G))))
[/code]

Hold on there! That’s the formula _we just started with._

Which means that

[code]

    (not (there-is a (proves a (subst G 4 G))))
[/code]

Is saying: “I am not provable in PM-Lisp”. 😮

## What to Believe

Well, that’s an interesting statement, but is it true? Let’s consider it for a
moment:

“This Formula is not Provable in PM-Lisp.”

If this was true:

It would mean that PM-Lisp was _incomplete_ : Not all true mathematical
statements can be proven in PM-Lisp. This very sentence would be an example of
a statement that couldn’t be proven.

But, if this was false:

Then that would mean that PM-Lisp could _prove_ “This Formula is not Provable
in PM-Lisp”. But, if it _could_ prove this statement, then the statement would
be false! This formula is provable right, so how could we prove that it is not
provable? That would make our language inconsistent — it just proved a false
statement, analogous to 1 + 1 = 3!

Hence Gödel came to a startling conclusion: If PM-Lisp _was_ consistent, then
it _would have to be_ incomplete. If it was complete, it would _have_ to be
inconsistent.

## Power of Numbers

That was a blow for Russell and Whitehead, but what about Hilbert? Could we
just come up with some new language that could avoid it?

Well, as soon as a language can represent whole numbers, it will fall into the
same trap: Gödel can just map the language to numbers, create a valid
`successor?` function, and produce the equivalent “I am not provable in X”.

This flew in the face of many a mathematician’s dreams: even arithmetic had a
quality to it that could not be reduced to axioms.

In programming, this translates to: there are some truths that you can _never_
write down as an algorithm. This is the essence of what Gödel discovered.

He went on to prove some more surprising things. It turns out that he could
write a similar, valid sentence that said “I cannot prove that I am
consistent”. This meant that no formal system, could prove by itself, that it
could only produce true statements.

Now, this doesn’t mean that all is for naught. For example, it may mean that
we can’t write an algorithm that can think like a dog...but perhaps we don’t
need to. The way neurons aren’t aware of a dog’s love of toys, our algorithms
wouldn’t have to be either: perhaps a consciousness would emerge as
epiphenomena in the same way. The idea of “think like a dog” just won’t be
written down concretely.

We can’t prove within a system that it is consistent, but we _could_ prove
that using another system. But it begs the question of course: how could we
prove _that other system_ was consistent? And so on!

I see Gödel’s idea like a guide: it shows us the limit of what we can do with
prescriptive algorithms. And I find what he did so darn funny. Russell and
Whitehead went through a lot of trouble to avoid self-reference in their work.
In a way, Gödel got around that by building the first “meta-circular
evaluator” — a language that interpreted itself — and came up with some
surprising conclusions as a result.

## Fin

I hope you had fun going through this :). If you want to go deeper on Gödel’s
proof, there are a few books you may like. Hofstadter’s [“I’m a Strange
Loop”](https://www.amazon.com/Am-Strange-Loop-Douglas-
Hofstadter/dp/0465030793) gives a very friendly introduction in Chapter 9.
Nagel and Newman’s [“Gödel’s Proof”](https://www.amazon.com/G%C3%B6dels-Proof-
Ernest-Nagel/dp/0814758371) explains the background, alongside a logical
overview very well. For those who want to do go even deeper, I really enjoyed
Peter Smith’s [“Introduction to Gödel’s
Theorems”](https://www.amazon.com/Introduction-Theorems-Cambridge-
Introductions-Philosophy/dp/0521674530). He shows much more substantiated
proofs for `(proves a b)` and `(subst a b c)` — I highly suggest giving that a
read too!

Also, if you want to play with creating your own Gödel Numbers, [here’s a
quick script in Clojure](https://github.com/stopachka/godel-numbers).

* * *

_Thanks to Irakli Popkhadze, Daniel Woelfel, Alex Reichert, Davit Magaltadze,
Julien Odent, Anthony Kesich, Marty Kausas, Jan Rüttinger, Henil, for
reviewing drafts of this essay_

  * [Mandarin Translation](https://yuki.systems/essay/2020/11/18/godel.html)

