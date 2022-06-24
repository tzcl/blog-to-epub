# Bel in Clojure


9 months ago, I took a gander at PG’s [guide to
Bel](http://www.paulgraham.com/bel.html). If you haven’t read it, here’s the
premise:

In 1958 when McCarthy invented Lisp, he started with a mathematical, rather
than a practical definition. His paper was more similar to the spec for a
Turing Machine than a spec for Fortran. For example, McCarthy didn’t even
think that Lisp would run on real computers until his graduate student
suggested it.

This was the secret to Lisp’s power. Because McCarthy was unconcerned with how
Lisp would work on the computers of 1958, he made a language so powerful that
it’s still magic for the computers of 2021.

The original spec for Lisp stopped short of a complete language. There were no
numbers or errors for example. So PG thought: what would happen if I continued
McCarthy’s tradition, and formally defined a _complete_ language? Numbers,
errors, and all.

This idea spoke to my Lisper heart, and I was intrigued. I opened up the guide
and got reading. An hour in, and I knew I needed to get my hands dirty to
really understand this. So I told myself, hey, why don’t I just take a weekend
and implement the spec?

Well...9 months later, I present you Bel in Clojure!

![](https://stopa.io/api/image/firstFrame/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzE0ODI2MTc1MC1hMzVkZmIxNC0zMDg1LTQ0OGQtOGQxNi00NTFjMGU0OGU4ZjcuZ2lm)

It’s still rough, and about 85% there, but it’s ~tolerably fast for small
functions, and even supports multi-threading! Want to try it yourself? [Here’s
the code](https://github.com/stopachka/bel-clojure).

## The Journey

Working on Bel felt like going on a country walk, and running into an old
friend who suggests skydiving. You think to yourself, sure a bit out of the
ordinary but why not, skydiving is fun. As soon as you step on the plane, you
discover the pilot is an intrepid adventurer and offers you a glide over
London. Well, you wouldn’t have predicted this, but you did always want to
visit London. After your plane lands, you run into a person who speaks to your
soul. You blink, and find yourself on a scooter over a dirt road in Thailand,
driving off into the sunset with the love of your life.

Okay this may be a bit too much for a paragraph in a technical essay. What do
I mean?

### EBNF

My first plan was a 2-day project: I would use Clojure’s reader, keep Clojure
data structures, and write a standard recursive interpreter — no more than a
few hundred lines probably.

And there came my first surprise. I couldn’t use Clojure’s reader. PG supports
quasiquotes (``(foo ',a ,@b)`) custom characters (`\bel`), dotted lists (`(a .
b)`), and a powerful shorthand syntax (`x|~f:g!a` typechecks, composes 3
functions, quotes and invokes). I realized I’d need to write my own parser
[1].

Thankfully, I discovered
[instaparse](https://github.com/Engelberg/instaparse), and EBNF notation.
EBNF, if you haven’t heard of it, is a declarative way to describe programming
language syntax. Years have made me suspicious of purported “declarative DSLs”
— often a hodpodge of incidental complexity. But, my friends EBNF joins SQL in
my eyes as a real solution.

### Continuations

So, with the parser out of the way, I marched forward with confidence. One
more weekend, and I’d surely be done. Oops, I hit another surprise: my simple
recursive interpreter wouldn’t work.

PG supports continuations. Continuations let you “move back” to different
points in your program’s execution. (If you haven’t heard of them, no worries,
I’ll describe them in more detail later in the essay). What this meant for me,
was that I couldn’t just have a simple interpreter that recursed over itself,
as I’d need to be able to “go back” to states in the recursion.

Now I saw one more weekend wouldn’t do the trick, and took a break.

### SICP to the rescue?

A few months later, I got back to the project, but this time opened up my
trusty guide: Structure and Interpretation of Computer Programs. I perused
their chapter on the [amb
intepreter](https://mitpress.mit.edu/sites/default/files/sicp/full-
text/book/book-Z-H-28.html), and saw how they used the “continuation-passing-
style”. Yes, this could do the trick.

Okay, off I went, and re-implemented my interpreter in the continuation-
passing-style. If you haven’t heard of it, here’s the idea: every step,
instead of returning, calls a “done” callback. This lets you save callbacks
and move between different states in the execution.

Once I made this refactor, continuations were easy peasy.

### -J-Xss900M

Well, very soon I came to the next setback. After just 100 or 200 lines of
reading the Bel source, running simple programs would cause my interpreter to
stack overflow. PG heavily takes advantage of recursion in his code, which
exacerbated my poor callback-based interpreter.

At first, I started raising the JVM stack size, hoping I could get through.
But, I was beginning to hit stack overflows even when I set the stack size to
900 megabytes. [2] To make matters worse, writing an interpreter with
continuation-passing-style is a nightmare to debug and reason about. Here’s an
example of [one function](https://github.com/stopachka/bel-
clojure/blob/22f72f6fcae25dff5b725e33104537ab4c588c55/src/bel_clojure/instance.clj#L519-L550)
— this kind of recursion makes my head spin.

So, off on another break I went.

### Stacks

Then, I opened the project up a week ago. This time, I thought to myself: why
don’t I implement my own call stack?

Keeping my own call stack (which is just how PG does it in the Bel source),
turned out to be the watershed moment. It was easier to debug, and a bunch of
the implementation became simpler. For example, supporting multi-threading was
only [~50 lines](https://github.com/stopachka/bel-clojure/pull/19/files)!

At this point, I was emboldened. Much of Bel was working, but it was slow. In
the formal spirit, PG implements the environment as a list for example. This
meant every lookup was O(n). Numbers were also implemented as lists, and just
`+` would take too long to run. I was worried that if my interpreter ran PG’s
source, it would be intolerably slow.

### Clojure Inspiration

So I thought to myself, why don’t I try to make it faster? I loved Clojure’s
design decisions, when it came to interop with java. Clojure strings are java
strings, clojure numbers are java numbers.

So, I went with that spirit. I leaked `java.util.HashMap` into Bel, and used
that as the environment. That was a huge speedup. After that, I leaked java
numbers, strings, and chars [3]. Bel began to take a pragmatic shape.

### The Current State

At this point, the interpreter supports much of Bel, but has diverted from the
formal specification in a few ways. Numbers are Clojure numbers, and Strings
are a separate type. The most crucial missing feature are streams: I think
we’d want to seep Java streams, but I haven’t thought deeply about it yet.

It’s still slow [4], and I’m certain there many bugs to overcome. But, it’s
fun to use as a REPL 🙂

## Impressions

Implementing Bel has given me quite an appreciation for the source. Bel is
_powerful._ When defining the whole language in itself, the language designer
is forced to expose access to all the constructs they need, and that means the
user of the language is as powerful as the designer.

### lit

For example, PG introduces a new construct called `lit`. It’s like a
persistent quote:

[code]

    (quote a)
    > a 
    (lit a) 
    > (lit a)
[/code]

Why would you need this? Well, if you’re trying to define “primitive types” in
your language, like functions or numbers, you’d want them to evaluate to
themselves. So PG takes advantage of `lit` to do just this. For example,
here’s how he represents functions:

[code]

    (lit clo nil (x) (+ x 1))
[/code]

Functions are lists, just like something the language user could write. If you
wanted to create your own primitive type — say “keywords”, it would look
conceptually similar:

[code]

    (lit kw foo)
    > (lit kw foo)
[/code]

### globe, scope

And how about closures? To support that, whenever a function is defined, PG
needs a way to “inject” the current lexical scope. So, he introduces `globe`
and `scope`: variables that expose the actual interpreter environment. Now he
can write something like this:

[code]

    (mac fn (params body)
      `(list 'lit 'clo scope ',params ',body))
[/code]

So when a `fn` is defined, it just generates a list, with the current scope
plopped inside:

[code]

    ((fn (y) (fn (x) (+ x y)) 1)
    > (lit clo {y 1} (x) (+ x y))
[/code]

I don’t know of a different language that gives you access to the environment
in this way. It was pretty cool to see how simple it was to define something
like `fn`

### mac

I was also surprised with his macros. I traditionally thought macros ran once
during compile time. But his macros are “ever-present”, and are available at
runtime. He defines a macro as a simple `lit` which keeps a closure. This
closure is run over the arguments it receives, before they’re evaluated.

[code]

    (lit mac (lit clo ...))
[/code]

This isn’t unique to Bel, But I thought the way we could define `defmacro`,
was pretty cool:

[code]

    (set defmacro
      (lit mac
        (lit clo nil (n p e)
          (list 'set n
                (list 'lit 'mac
                      (list 'lit 'clo nil p e))))))
[/code]

This is a macro-defining macro!

### err

The “defining the language” thinking shows up with how PG specs out errors.
For example, he says that whenever there’s an error, the interpreter can’t
just give up. Instead, it must call the `err` function with a message.

[code]

    (car 'a) ;; uh oh, this is an error, interpreter calls (err 'bad-arg)
[/code]

By making this axiom, it now lets PG control _how_ errors happen. For example,
say we want to do something special with the `err` function. We could do this:

[code]

    (dyn err (fn (x) 'hello) (car 'a))
    > hello
[/code]

Here, we redefined `err`, to a function that returns `'hello`. All of a
sudden, we have half of what we need to implement error catching.

### Continuations

The other half, comes from continuations. Before Bel I had heard of
continuations, but I never seriously used a language that supported them. As I
said before, continuations let you go to a certain point in a program’s
execution.

To get a better sense of what I mean, let’s look at an example PG uses in his
guide:

[code]

    (list 'a (ccc (fn (c) (set cont c) 'b)))
    > (a b)
[/code]

Here, we start a computation `(list 'a ...)`. This runs `(ccc (fn () ...))`
and returns the result `'b`, which completes `(list 'a 'b)`, and returns `(a
b)`.

But now watch this:

[code]

    (cont 'z)
    > (a z)
    (cont 'w)
    > (a w)
[/code]

The callback in `ccc` gave us `c`, a continuation. Whenever we call it, it’s
as though we “went back” to when our interpreter was computing `(list a ...)`,
but this time instead of returning `'b` , we return `'z`. We then do that
again but with `'w`.

Why do we need it? Well, let’s say you want to do some kind of error catching.
Here’s how you could do it:

[code]

    (ccc (fn (c) 
            (dyn err (fn (x) (c 'uhohgotanerror))
              (car 'b))))
    > uhohgotanerror
[/code]

All of a sudden, you can implement a whole suite of cool macros, like `eif`,
`safe,` and `onerr`, with a [few lines of
code](https://github.com/stopachka/bel-
clojure/blob/main/resources/core.bel#L250-L267):

[code]

    (onerr 'oops (car 'a))
    > 'oops
[/code]

At first I was skeptical with continuations, but one thing is clear: they are
a more _fundamental_ abstraction than exceptions. You can implement exceptions
with continuations, but you can’t implement continuations with exceptions. If
power is your priority, than they are more powerful.

### Utilities

I’m not sure how much this is a consequence of writing a language in itself,
but I found a grab-bag of great functions and macros I hadn’t seen before in
other languages. Here are some really fun ones.

The `eif` macro, returns one branch if there’s an error:

[code]

    (eif x (car 'a)
            'oops
            x)
    > oops
[/code]

The `aif` macro, which evaluates the test expression, but lets you access the
result as the variable `it`:

[code]

    (map (fn (x)
            (aif (cdr x) (car it)))
      '((a) (b c) (d e f) (g)))
    > (nil c e nil)
[/code]

The `of` function, which applies one function to all arguments, and gives
those results to another one:

[code]

    ((of + car) x y z)
    ;; same as -> 
    (+ (car x) (car y) (car z))
[/code]

And `upon`, which lets you save arguments and apply them to different
functions:

[code]

    (map (upon '(a b c)) 
         (list car cadr cdr))
    > (a b (b c))
[/code]

### Abbreviations

Perhaps the most fun thing I saw, which I immediately wished was available in
clojure was the shorthand syntax:

For example, composition:

[code]

    foo:bar:baz
    ;; same as ->
    (compose foo bar baz)
[/code]

And whenver you need to get the “opposite” of a function:

[code]

    ~foo
    ;; same as ->
    (compose no foo)
[/code]

There’s two really nice list creation abbreviations too:

[code]

    foo.a
    ;; same as ->
    (foo a)
    foo!a 
    ;; same as ->
    (foo 'a)
[/code]

This kind of stuff seems small and inconsequential, but it's significant in
practice. I think it may be because though it seems like it's about saving
keystrokes, it's actually about giving your mind a shorthand to think with.

### My one big gripe

The one thing that made me hesitant, was the underlying pair primitive in Bel.
It’s mutable. On one hand, I can understand the decision, as if you’re trying
to answer “how can I formally define a complete language?”, I think
immutability wouldn’t be critical.

But, after immutability in Clojure, I’m convinced it’s the way that we should
all be programming. It models [reality
better](https://www.youtube.com/watch?v=ScEPu1cs4l0), and it makes concurrency
a magnitude simpler [5].

Still, I’m not sure an implementation of Bel necessarily has to have
mutability as core to the language. It may be just as good to “seep” clojure’s
Peristent Seq, atom, and make threads actual system threads. We’d come to a
pretty darn cool language.

### One Fun Experiment

Perhaps the most interesting meta lesson, is to approach projects with naivete
and play. If I had known this would have taken 3 different interpreter
implementations, I would have been more hesitant to have started, but boy am I
glad I did. I learned a lot. It’s still a toy, and there’s still a lot of work
to do, but the journey itself was worth it.

I suggest you try it out, and hey, if you want to take it further, the source
is out there 🙂.

_Thanks Alex Reichert, Alexandre Lebrun, Daniel Woelfel, Dennis Heihoff, Joe
Averbukh, Julien Odent, Martin Raison, Sean Grove for reviewing drafts of this
essay_

