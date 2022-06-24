# Fun with Lambda Calculus


In 1935, a gentleman called Alonzo Church came up with a simple scheme that
could compute…just about anything. His scheme was called Lambda Calculus. It
was a phenomenal innovation, given that there weren’t even computers for him
to test out his ideas. Even cooler is that those very ideas affect us today:
anytime you use a function, you owe a hat tip to Mr. Church.

Lambda Calculus is so cool that many hackers use it as their secret handshake
— a “discreet signal” if you will. The most famous, of course, is PG’s Y
Combinator. In this essay, we’ll find out what it’s all about, and do things
with functions that we’d never have imagined. In the end you’ll have built
just about every programming concept: numbers, booleans, you name it…just with
functions.

## 0: Intuition with Pairs

City dwellers who drive SUVs rarely consider their cars as ferocious machines
that traverse rocky deserts and flooded rivers. It’s the same with programmers
and functions. Here’s what we _think_ functions do:

[code]

    (def square (fn [x] (* x x)))
[/code]

Safe, clean, and useful. We’re so accustomed that it would surprise us to find
the myriad of ways we can bend functions to do just about anything.

Let’s step out into the wilderness a bit. Say you wanted to make a data
structure for pairs:

[code]

    (def pair (make-pair 0 1))
    (first pair) ; => 0
    (second pair) ; => 1
[/code]

How would you do it? It’s sensible to use a map or a class or a record to
represent a pair. But…you could use functions too.

Here’s one way we can make a pair:

[code]

    (def church-pair (fn [a b]
                       (fn [selector]
                         (selector a b))))
[/code]

No maps or classes…it just returns a function!

[code]

    (def ex-pair (church-pair 0 1))
    ex-pair
    ; => #object[church_factorial$church_pair...
[/code]

Now our `ex-pair` takes a `selector` argument. What if we ran ex-pair with
this selector:

[code]

    (ex-pair (fn [a b] a))
[/code]

Well, `(ex-pair (fn [a b] a))` would expand too:

[code]

    ((fn [a b] a) a b)
[/code]

Which would return… `a`!

That just gave us the `first` value of our pair! We can use that to write a
`church-first` function:

[code]

    (def take-first-arg (fn [a b] a))
    (def church-first (fn [pair]
                        (pair take-first-arg)))
[/code]

[code]

    (church-first ex-pair)
    ; => 0
[/code]

And do something similar for second:

[code]

    (def take-second-arg (fn [a b] b))
    (def church-second (fn [pair]
                         (pair take-second-arg)))
[/code]

[code]

    (church-second ex-pair)
    ; => 1
[/code]

We just used functions to represent pairs. Now, since the grammar for Lisp is
just a bunch of pairs plopped together, that also means we can represent the
grammar of Lisp…with just functions!

## 1: Factorial

What we just did was analogous to a city dweller driving their SUV…on a snowy
day. It gets a _lot_ crazier.

We said we could represent _everything_. Let’s go ahead and try it!

Here’s what can do. Let’s take a function we know and love, and implement it
from top-to-bottom in Lambda Calculus.

Here’s factorial:

[code]

    (defn factorial-clj [n]
      (if (zero? n)
        1 
        (* n (factorial-clj (dec n)))))
[/code]

[code]

    (factorial-clj 5)
    ; => 120
[/code]

By the end of this essay, we’ll have built factorial, only with functions.

## 2: Rules

To do this, I want to come up front and say I am cheating a little bit. In
Church’s Lambda Calculus, there is no `def`, and all functions take one
argument. Here’s all he says:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk2Mzc4MjA4LTc0M2VkMDgwLTExNTgtMTFlYi05YTI2LTFlMGUyOWFmNDQ0MC5wbmc)

In his rules, you define anonymous functions by popping a little `λ` in front.
What follows is the argument, following by a `.` .After the `.` is the
application.

This is very much akin to a single-argument anonymous function in Clojure: `λ
x. x` => `(fn [x] x)`

We could follow those rules, but writing factorial like that is going to get
hard to reason about very quickly. Let’s tweak the rules just a little bit.
The changes won’t affect the essence of Lambda Calculus but will make it
easier for us to think about our code. Here it goes:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk2Mzc4MjE3LTc5OWMxYjAwLTExNTgtMTFlYi05N2U5LWY0ZDIxZGE2YmJkOC5wbmc)

1) for a single argument function, `(fn [x] x)` maps pretty well to Church’s
encoding. We can go ahead and use it as is.

2) Since Church’s lambdas only take one argument, For him to express a
function with two arguments, he has to write _two_ anonymous functions:

[code]

    (λ f. λ x. f x)
[/code]

This would map to:

[code]

    (fn [f] (fn [x] (f x))
[/code]

But, nesting our functions like this can get annoying in Clojure [1]. To make
life easier for us, we’ll allow for multi-argument functions:

[code]

    (fn [f x] (f x))
[/code]

3) Finally, Church has no concepts of variables outside of what’s provided by
a function definition.

For him to express

[code]

    (make-pair a b)
[/code]

He would have to “unwrap” `make-pair`

[code]

    ((λ a. λ b. λ selector . selector a b)
     a b)
[/code]

To keep our code sane, we’ll allow for `def`, but with one rule:

**You can use** **`def`** **, as long as you can “replace” it with an
anonymous function and nothing breaks.**

For example, imagine if `make-pair` _referenced itself_ :

[code]

    (def make-pair (fn [a b]
                     (make-pair ...)))
[/code]

This would break because if we replaced `(def make-pair …)` with an anonymous
function, there would be no variable called `make-pair` anymore!

That’s it, these are our rules. With that, we’re ready to make factorial!

## 3: Numerals

The first thing we need is the concept of a number. How can we do that?

Church thought of a pretty cool idea. What if “numbers”, were higher-order
functions with two arguments: a function `f`, and a value `v`.

[code]

    (def zero (fn [f v] v))
    
    (def one (fn [f v]
               (f (zero f v))))
    
    (def two (fn [f v]
               (f (one f v))))
[/code]

 **We can figure out what number each function represents by “counting” the
number of times** **`f`** **was composed.**

For example, 0 would compose `f` zero times: it would just return `v`. 1,
would compose f once: `(f v)`. 2 would compose twice: `(f (f v))`, and so on.

To help us see these numbers in our REPL, let’s create a quick converter
function:

[code]

    (defn church-numeral->int [church-numeral]
      (church-numeral inc 0))
[/code]

Since a church numeral composes `f` the number of times it is called with `v`
as the first argument, all we need to see what number it is in Clojure, is to
provide `inc` as `f` and `0` as `v`! Now `2` would do `(inc (inc 0))` for
example, and get us the corresponding Clojure number.

[code]

    (map church-numeral->int [zero one two])
    ; => (0 1 2)
[/code]

Cool!

## 4: Inc

Take a look at how we wrote two:

[code]

    (def two (fn [f v]
               (f (one f v))))
[/code]

What we did here, is _delegate_ f’s composition to the numeral before (in this
case `one` ), and then just called `f` _one more time._

What if we abstracted the `one` out?

[code]

    (def church-inc
      (fn [church-numeral]
        (fn [f v]
          (f (church-numeral f v))))) 
[/code]

Voila. Give this function a numeral, and it will return a new numeral that
calls `f` _one more time_. We’ve just discovered `inc`!

[code]

    (church-numeral->int (church-inc (church-inc one)))
    => 3
[/code]

Cool.

Now that we have this function, we can also write a quick helper to translate
Clojure numbers to these numbers:

[code]

    (def int->church-numeral
      (fn [clojure-int]
        (if (zero? clojure-int)
          zero
          (church-inc (int->church-numeral (dec clojure-int))))))
[/code]

[code]

    (church-numeral->int (int->church-numeral 5))
    => 5
[/code]

That’ll come in handy for our REPL.

## 5: Dec: Intuition

Next up, we need a way to “decrement” a number. Well, with `inc` we create a
numeral that composes `f` _one more time_. If we can make some kind of
function that composes `f` _one less time,_ then we’d have `dec`!

To do that, we’ll need to go on a short diversion.

## 6: Dec: shift-and-inc

Remember our `pair` data structure? Let’s create a function for it (we’ll use
this in just a moment below): `shift-and-inc`. All it would do, is take pair
of numbers, and “shift” the pair forward by one:

For example, applying `shift-and-inc` to `(0 1)`, would produce `(1 2)`. One
more time, it would produce `(2 3)`, and so on.

Sounds simple enough:

[code]

    (def shift-and-inc (fn [pair]
                         (church-pair
                           (church-second pair)
                           (church-inc (church-second pair)))))
[/code]

Bam, we take a pair. The second item is shifted over to the first positions
and is replaced with its `inc`ed friend. Let’s try it out:

[code]

    (let [p (shift-and-inc (church-pair one two))]
      (map church-numeral->int [(church-first p) (church-second p)]))
    ; => (2 3)
[/code]

Works like a charm!

## 7: Dec: putting it together

Now that we have `shift-and-inc`, what if we did this:

[code]

    (def church-dec
      (fn [church-numeral]
        (church-first
          (church-numeral shift-and-inc
                          (church-pair zero zero)))))
[/code]

Remember that our `church-numeral` would call `shift-and-inc` N times,
representing its numeral value. If we started with a pair `(0, 0)`, then what
would the result be, if we composed `shift-and-inc` `N` times?

Our result would be the pair `(N-1, N)`. This means that if we take the first
part of our pair, we have `dec`!

[code]

    (church-numeral->int (church-dec (int->church-numeral 10)))
    ; => 9
[/code]

Nice.

## 8: Multiplication

Next up, multiplication. Say we multiply `a` by `b`. We’d need to produce a
church numeral that composes `f`, `a * b` times. To do that, we can leverage
the following idea:

Say we made a function `g`, which composes `f` _b_ times. If we fed that
function to `a`, it would call `g`, _a_ times.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk2Mzc4MjI2LTdmOTFmYzAwLTExNTgtMTFlYi05MmY2LTVlZDdhNzA0YWE1MC5wbmc)

If `a` was “2” and “b” was 3, how many times would `f` get composed? Well, `g`
would be composed twice. Each time `g` is composed, `f` is composed 3 times.
That comes out to a total of 6 times!

Bam, if we did that, it would represent multiplication.

[code]

    (def church-*
      (fn [num-a num-b]
        (fn [f v]
          (num-a (partial num-b f) v))))
[/code]

Here, `(partial num-b f)` represents our `g` function.

[code]

    (church-numeral->int
        (church-* (int->church-numeral 5) (int->church-numeral 5)))
    => 25
[/code]

Works like a charm!

## 9: Booleans

We’ve got numbers, we’ve got `*` and we’ve got `dec`. Next up…booleans!

To do this, we need to be creative about what `true` and `false` is.

Let’s say this. Booleans are two argument functions:

[code]

    (def church-true (fn [when-true when-false]
                       when-true))
    
    (def church-false (fn [when-true when-false]
                        when-false))
[/code]

They take a “true” case and a “false” case. Our `church-true` function would
return the true case, and `church-false` function would return the false case.

That’s it. Surprisingly this is enough to handle booleans. Here’s how we could
convert them to Clojure bools.

[code]

    (defn church-bool->bool [church-bool]
      (church-bool true false))
[/code]

Our `church-true` would return the first argument (true), and our `church-
false` would return the second one!

[code]

    (church-bool->bool church-true)
    ; => true
    (church-bool->bool church-false)
    ; => false
[/code]

Do they look familiar? Those are our `selector` functions for `church-first`
and `church-second`! We could interchange them if we wished 😮

## 10: if

If you are like me, you were a bit suspicious of those booleans. Let’s put
them to use and quiet our fears. Here’s how could create an `if` construct:

[code]

    (def church-if (fn [church-bool when-true when-false]
                     (church-bool when-true when-false)))
[/code]

All we do to make `if`, is to simply shuffle things around and provide the
`when-true` and `when-false` cases to our boolean! `church-true` would return
the `when-true` case, and `church-false` would return the `when-false` case.

That would make `if` work pretty well:

[code]

    (church-numeral->int
        (church-if church-true one two))
    ; => 1
    (church-numeral->int
        (church-if church-false one two))
    ; => 2
[/code]

## 11: zero?

We have almost _all_ the constructs we need to implement `factorial`. One
missing piece: `zero?`. We need a way to tell when a numeral is zero.

The key trick is to remember that the `zero` numeral _never_ calls `f`.

[code]

    (def zero (fn [f v] v))
[/code]

We can use that to our advantage, and create a `zero?` predicate like this:

[code]

    (def church-zero?
      (fn [church-numeral]
        (church-numeral (fn [v] church-false) church-true)))
[/code]

If a number is greater than zero, `f` would be called, which would replace `v`
with `church-false`. Otherwise, we’d return the initial value of `v`, `church-
true`.

[code]

    (church-bool->bool (church-zero? zero))
    ; => true
    (church-bool->bool (church-zero? one))
    ; => false
[/code]

Wow…I think we’re ready?

## 12: factorial-v0

Let’s look at `factorial-clj` again:

[code]

    (defn factorial-clj [n]
      (if (zero? n)
        1
        (* n (factorial-clj (dec n)))))
[/code]

Well, we have `numerals`, we have `if`, we have `zero?` we have `*`, we have
`dec`. We could translate this:

[code]

    (def factorial-v0
      (fn [church-numeral-n]
        ((church-if
           (church-zero? church-numeral-n)
           (fn [] one)
           (fn []
             (church-*
               church-numeral-n
               (factorial-v0 (church-dec church-numeral-n))))))))
[/code]

Wow. That follows our recipe pretty much to a key.

The only weird thing is that we wrapped the `when-true` and `when-false` cases
in an anonymous function. This is because our `church-if` is a little
different than Clojure’s `if`. Clojure’s if _only_ evaluates one of the `when-
true` and `when-false` cases. Ours evaluates both cases, which triggers an
infinite recursion. We avoid this by wrapping both cases in a lambda, which
“delays” the evaluation for us. [2]

Will it work?

[code]

    (church-numeral->int (factorial-v0 (int->church-numeral 5)))
    ; => 120
[/code]

Wow! 🤯 We did it

## 13: Broken rules

Okay, almost. We cheated. Remember our `Rule 3`: **If we replace our variables
with an anonymous function, everything should work well.** What would happen
if we wrote `factorial-v0` as an anonymous function?

[code]

    (fn [church-numeral-n]
      ((church-if
         (church-zero? church-numeral-n)
         (fn [] one)
         (fn []
           (church-*
             church-numeral-n
             ; :< :< :< :< uh oh
             (factorial-v0 (church-dec church-numeral-n)))))))
[/code]

Dohp. `factorial-v0` would not be defined.

Here’s one way we can fix it. We could update this so `factorial` is _provided
as an argument to itself._

[code]

    (fn [factorial-cb]
     (fn [church-numeral-n]
       ((church-if
          (church-zero? church-numeral-n)
          (fn [] one)
          (fn []
            (church-*
              church-numeral-n
              (factorial-cb (church-dec church-numeral-n)))))))
      ????)
[/code]

That _would work,_ but we only punt the problem down. What the heck would
`????` be? We need some way to pass a reference of `factorial` to _itself_!

## 14: Y-Combinator: Writing it out

Let’s see if we can do make this work. First, let’s write our factorial, that
accepts some kind of “injectable” version of itself:

[code]

    (def injectable-factorial
      (fn [factorial-cb]
        (fn [church-numeral-n]
          ((church-if
             (church-zero? church-numeral-n)
             (fn [] one)
             (fn []
               (church-*
                 church-numeral-n
                 (factorial-cb (church-dec church-numeral-n)))))))))
[/code]

If we can somehow provide that `factorial-cb`, we’d be golden.

To do that, let’s create a `make-recursable` function, which accepts this
`injectable-f`

[code]

    (def make-recursable
      (fn [injectable-f]
        ????))
[/code]

Okay, all we did now is move the problem into this `make-recursable` function
😅. Bear with me.

Let’s imagine what the solution would need to look like. We’d want to call
`injectable-f` with some `factorial-cb` function handles the “next call”.

[code]

    (def make-recursable
      (fn [injectable-f]
        ; recursion-handler
        (injectable-f (fn [next-arg]
                        ????))))
[/code]

That seems right. Note the comment `recursion-handler` . This is in reference
to this form:

[code]

        (injectable-f (fn [next-arg]
                        ????)
[/code]

If we somehow had access to this form, we can use that in `????`! Well, let’s
punt the problem down again:

[code]

    (def make-recursable
      (fn [injectable-f]
        (????
         (fn [recursion-handler]
           (injectable-f (fn [next-arg]
                           ((recursion-handler recursion-handler) next-arg)))))))
[/code]

Here, we wrap our `recursion-handler` into a function. If it could get a copy
of itself, we’d be golden. But that means we’re back to the same problem: how
could we give `recursion-handler` a copy of itself? **Here’s one idea:**

[code]

     (def make-recursable
      (fn [injectable-f]
        ((fn [recursion-handler] (recursion-handler recursion-handler))
         (fn [recursion-handler]
           (injectable-f (fn [next-arg]
                           ((recursion-handler recursion-handler) next-arg)))))))
[/code]

Oh ma god. What did we just do?

## 15: Y-Combinator: Thinking it through

Let’s walk through what happens:

The first time we called:

[code]

    (make-recursable injectable-factorial)
[/code]

this would run

[code]

    (fn [recursion-handler] (recursion-handler recursion-handler))
[/code]

`recursion-handler` would be:

[code]

    (fn [recursion-handler]
      (injectable-f (fn [next-arg]
                      ((recursion-handler recursion-handler) next-arg))))
[/code]

And `recursion-handler` would call itself:

[code]

    (recursion-handler recursion-handler)
[/code]

So now, this function would run:

[code]

    (fn [recursion-handler]
           (injectable-f (fn [next-arg]
                           ((recursion-handler recursion-handler) next-arg))))
[/code]

And this function’s `recursion-handler` argument would be… **a reference to
itself!**

🔥🤯. Oh boy. Let’s continue on.

Now this would run:

[code]

           (injectable-f (fn [next-arg]
                           ((recursion-handler recursion-handler) next-arg))
[/code]

`injectable-factorial` would be called, and it’s `factorial-cb` function would
be this callback:

[code]

    (fn [next-arg]
      ((recursion-handler recursion-handler) next-arg))
[/code]

Whenever `factorial-cb` gets called with a new argument,

[code]

    (recursion-handler recursion-handler)
[/code]

This would end up producing a new `factorial` function that had a `factorial-
cb`. Then we would call that with `next-arg`, and keep the party going!

Hard to believe. Let’s see if it works:

[code]

    (def factorial-yc (make-recursable injectable-factorial))
[/code]

[code]

    (church-numeral->int (factorial-yc (int->church-numeral 5)))
    ; => 120
    (church-numeral->int (factorial-yc (int->church-numeral 10)))
    ; => 3628800
[/code]

 **Very cool!**

This `make-recursable` function is also called the Y Combinator. You may have
heard a lot of stuff about it, and this example may be hard to follow. If you
want to learn more, I recommend [Jim’s
keynote](https://www.youtube.com/watch?v=FITJMJjASUs&ab_channel=Confreaks).

## 16: Just Functions

Wow, we did it. We just wrote `factorial`, and _all we used were anonymous
functions._ To prove the point, let’s remove some of our rules. Here’s how our
code would end up looking without any variable definitions:

[code]

    (church-numeral->int
      (((fn
          [injectable-f]
          ((fn [recursion-handler] (recursion-handler recursion-handler))
           (fn [recursion-handler] (injectable-f (fn [next-arg] ((recursion-handler recursion-handler) next-arg))))))
        (fn
          [factorial-cb]
          (fn
            [church-numeral-n]
            (((fn [church-bool when-true when-false] (church-bool when-true when-false))
              ((fn
                 [church-numeral]
                 (church-numeral (fn [v] (fn [when-true when-false] when-false)) (fn [when-true when-false] when-true)))
               church-numeral-n)
              (fn [] (fn [f v] (f ((fn [f v] v) f v))))
              (fn
                []
                ((fn [num-a num-b] (fn [f v] (num-a (partial num-b f) v)))
                 church-numeral-n
                 (factorial-cb
                   ((fn
                      [church-numeral]
                      ((fn [pair] (pair (fn [a b] a)))
                       (church-numeral
                         (fn
                           [pair]
                           ((fn [a b] (fn [selector] (selector a b)))
                            ((fn [pair] (pair (fn [a b] b))) pair)
                            ((fn [church-numeral] (fn [f v] (f (church-numeral f v)))) ((fn [pair] (pair (fn [a b] b))) pair))))
                         ((fn [a b] (fn [selector] (selector a b))) (fn [f v] v) (fn [f v] v)))))
                    church-numeral-n)))))))))
       ((fn [church-numeral] (fn [f v] (f (church-numeral f v))))
        ((fn [church-numeral] (fn [f v] (f (church-numeral f v))))
         ((fn [church-numeral] (fn [f v] (f (church-numeral f v)))) (fn [f v] (f ((fn [f v] (f ((fn [f v] v) f v))) f v))))))))
[/code]

[code]

    ; => 120
[/code]

😮

## Fin

Well, we just took our functions through the Mojave desert! We made numbers,
booleans, arithmetic, and recursion…all from anonymous functions. I hope you
had fun! If you’d like to see the code in full, take a look at the [GH
repo](https://github.com/stopachka/church-
factorial/blob/master/src/church_factorial.clj).

## Bonus: Fun with Macros

I’ll leave with you with some Clojure macro fun. When the time came to
“replace” all our `defs` with anonymous functions, how did we do it?

In wimpier languages we might have needed to do some manual copy pastin [3].
In lisp, we can use _macros._

First, let’s rewrite `def`. This version will “store” the source code of every
`def` as metadata:

[code]

    (defmacro def#
      "A light wrapper around `def`, that keeps track of the
      _source code_ for each definition
    
      This let's us _unwrap_ all the definitions later : >"
      [name v]
      `(do
         (def ~name ~v)
         (alter-meta! (var ~name) assoc :source {:name '~name :v '~v})
         (var ~name)))
[/code]

Then, we can create an `unwrap` function, that recursively replaces all `def`
symbols with with their corresponding source code:

[code]

    (defn expand
      "This takes a form like
    
      (church-numeral->int (factorial-yc (int->church-numeral 5)))
    
      And expands all the function definitions, to give
      us the intuition for how our 'lambda calculus' way would look!"
      [form]
      (cond
        (symbol? form)
        (if-let [source (some-> (str *ns* "/" form)
                                symbol
                                find-var
                                meta
                                :source)]
          (expand (:v source))
          form)
    
        (seq? form)
        (map expand form)
    
        :else form))
[/code]

Aand…voila:

![](https://stopa.io/api/image/firstFrame/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk2Mzc4NDE3LWMwZDZkYjgwLTExNTktMTFlYi04YmVlLWE4MTEwOTVkOTI5Yi5naWY)

To learn about what’s going on there, check out [Macros by
Example](https://stopa.io/post/229)

* * *

 _Thanks to Alex Reichert, Daniel Woelfel, Sean Grove, Irakli Safareli, Alex
Kotliarskyi, Davit Magaltadze, Joe Averbukh for reviewing drafts of this
essay_

