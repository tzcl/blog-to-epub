# LLisp: Lisp in Lisp


Last week I had a thought: “What’s the simplest Lisp interpreter I could
write, which supports macros?"

A weekend of Clojure hacking and some confusion later, a REPL was born. In
this essay, we’ll go through the same journey and make our own Lisp
interpreter, which supports macros…in Clojure! Let’s call it, LLisp: a lisp in
a lisp.

By the end, you’ll write your own macros in your own darn programming
language! Let’s get into it.

## Sketch

Okay, let’s sketch out the basic idea behind what we need to do:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzE1MDY1NTc1NC1lMTg0NmZlNC0yM2I3LTQ3ZTctYjJmNy1lMjJiMDJlZmU2NmQucG5n)

A programmer writes some code. So far, it’s just text, and there’s not much we
can do with that. We _read_ the programmer’s text, and convert it into data-
structures. We can do something with data-structures: we can _evaluate_ data-
structures, and return whatever the programmer intended.

If we can convert `"(+ 1 1)"` into `2`, we have ourselves the roots of a
programming language.

## Reader

Let’s handle “2. Read”. If a programmer writes text like `"(+ 1 1)"`, we want
to convert it to data-structures. Something like:

[code]

    (read-string "(+ 1 1)")
    ; =>
    (+ 1 1)
[/code]

We _could_ write `read-string` ourselves. For the simplest case it’s pretty
easy [1]. But, we’re in Clojure after all, and Clojure already understands how
to read Lisp code. Let’s just cheat and use Clojure’s `edn`:

[code]

    (ns simple-lisp.core
      (:refer-clojure :exclude [eval read read-string])
      (:require [clojure.edn :refer [read read-string]]))
[/code]

And voila, `read-string` does what we want:

[code]

    (read-string "(+ 1 1)")
    ; =>
    (+ 1 1)
[/code]

## Evaluation

Okay, now to “3. Evaluate”. Remember, our goal is to take data-structures,
evaluate **them and return whatever the programmer intended. We can begin with
a simple function like this:

[code]

    (defn eval [form] 
      ;; TODO 
      )
[/code]

### Evaluating Literals

Let’s get the easy things out of the way. Some things just evaluate to
themselves: if a programmer wrote `12` for example, all we’d have to do is to
return the number `12`. This is the same for strings (`"foo"`), characters
(`\b`), and booleans (`true`). They’re literals _._

Here’s how we can evaluate literals. Let’s detect them first:

[code]

    (def literal?
      (some-fn string? number? boolean? char? nil?))
[/code]

If you haven’t seen `some-fn` before, this is one of clojure’s many [handy and
powerful](https://clojuredocs.org/clojure.core/some-fn) utilities. Now we can
handle literals in `eval`:

[code]

    (defn eval [form]
      (cond
        (literal? form) form))
[/code]

And boom, our programming language starts to do something:

[code]

    (eval (read-string "12"))
    ; => 12
[/code]

### Introducing Quote

Let’s get to `quote`. Quote is a crucial form in Lisp. It lets you write code
that _does not_ evaluate. For example:

[code]

    (quote (+ 1 1))
    ; => 
    (+ 1 1)
[/code]

Because `(+ 1 1)` was inside `quote`, we didn’t evaluate it to return `2`.
Instead we returned the expression itself. This seems weird if you come from
languages that don’t support quotes, but it’s used all the time in Lisp. In
fact, there’s a shortcut for it:

[code]

    '(+ 1 1) 
[/code]

When this is read, it converts to

[code]

    (quote (+ 1 1))
[/code]

Thankfully, edn’s `read-string` does this for us. 🙂

### Evaluating Quote

So, how do we _evaluate_ quote? Let’s first create a function that can detect
them:

[code]

    (defn seq-starts-with? [starts-with form]
      (and (seqable? form) (= (first form) starts-with)))
    
    (def quote? (partial seq-starts-with? 'quote))
[/code]

We see if our form is a list, and the first element is the symbol `quote`

[code]

    (quote? (read-string "'(+ 1 1)"))
    ; => 
    true
[/code]

Works like a charm. Now let’s update `eval`:

[code]

    (defn eval [form]
      (cond
        (literal? form) form
        (quote? form) (second form)))
[/code]

If our form is a `quote`, we return the “second” part of it. And voila,

[code]

    (eval (read-string "(quote (+ 1 1))"))
    ; => (+ 1 1)
[/code]

### Introducing Symbols

Next, we come to symbols. Symbols are a special Lisp data type. They’re like
variables, in the sense that when we _evaluate a_ symbol _,_ we **look it up.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzE1MDY1NTc2MS01YmQ2ODhlOS00ZDEzLTQ3ZjMtYTg4My1lYTZhMTdlYWRjNjEucG5n)

Look it up where? Our interpreter will need some kind of `environment`, that
keeps track of all the variables we defined. If we had an environment, where
the symbol `fav-num` pointed to `41` for example, here’s what evaluating `fav-
num` would look like:

[code]

    (eval env (read-string "fav-num"))
    ; => 
    41
[/code]

### Evaluating Symbols

Let’s first create this `environment`. We can use java’s `Hashmap` to keep a
mapping of symbols to their values.

Let’s import java’s Hashmap:

[code]

    (ns simple-lisp.core
      (:refer-clojure :exclude [eval read read-string])
      (:require [clojure.edn :refer [read read-string]])
      (:import (java.util HashMap)))
[/code]

And make a quick function to create an `env` map:

[code]

    (defn env [] {:globe (HashMap. {'fav-num 41})})
[/code]

Now, we can accept an `env` map in `eval`, and start to handle symbols:

[code]

    (defn eval [env form]
      (cond
        (literal? form) form
        (quote? form) (second form)
        (symbol? form) (lookup-symbol env form)))
[/code]

Clojure already has a handy `symbol?` function, which we can use. When that’s
true, we’ll `lookup-symbol`. Here’s how `lookup-symbol` could look:

[code]

    (defn lookup-symbol [{:keys [globe]} sym]
      (let [v (when (contains? globe sym) [(get globe sym)])]
        (assert v (format "expected value for sym = %s" sym))
        (first v)))
[/code]

And with that, symbols work!

[code]

    (eval (env) (read-string "fav-num"))
    ; => 
    41
[/code]

### Evaluation Primitives

Next up, let’s take an important step to making `(+ 1 1)` work. We’ll want to
have `+` mean something. What should the symbol `+` point too?

How about Clojure functions?

[code]

    (defn env [] {:globe (HashMap. {'+ + 'fav-num 41})})
[/code]

If we did that, now whenever we evaluate the symbol `+`, it would return a
clojure function:

[code]

    (eval (env) (read-string "+"))
    ; => #object[clojure.core$_PLUS_ 0x4efcb4b5 "[[email protected]](/cdn-cgi/l/email-protection)"]
[/code]

And if we “received” a clojure function in eval, we can just treat it as a
literal:

[code]

    (def literal?
      (some-fn string? number? boolean? char? nil? fn?))
[/code]

[code]

    (eval (env) +)
    ; => #object[clojure.core$_PLUS_ 0x4efcb4b5 "[[email protected]](/cdn-cgi/l/email-protection)"]
[/code]

This is one small step in our essay, but a giant step for our Lisp. Every
element in `(+ 1 1)` can now be evaluated.

### Primitive Applications

So how do we run these functions? Well, let’s update `eval` , to handle lists
like `(+ 1 1)`:

[code]

    (defn eval [env form]
      (cond
        (literal? form) form
        (quote? form) (second form)
        (symbol? form) (lookup-symbol env form)
        :else (eval-application env form)))
[/code]

Easy. If we _can’t_ figure out what the `form` is, it _must_ be list, and it
must mean we want to run it! Here’s how `eval-application` could work:

[code]

    (defn eval-application [env [f & args]]
      (let [f-evaled (eval env f)]
        (cond
          (fn? f-evaled) (apply f-evaled (eval-many env args)))))
[/code]

In `eval-application` , we evaluate the _first_ part of our list. In our
example, this would be the symbol `+`, which would return a clojure function.

If `f-evaled` is a clojure function (which it is), we would run:

[code]

    (apply f-evaled (eval-many env args))
[/code]

`eval-many` is just a helper to evaluate a list of forms:

[code]

    (defn eval-many [e forms] (map (partial eval e) forms))
[/code]

`args` would be `(1 1)`, so `eval-many` would return `(1 1)`, and that means
we’d get the equivalent of:

[code]

    (apply + '(1 1))
[/code]

That would return `2`, and babam, we have `(+ 1 1)` working!

[code]

    (eval (env) (read-string "(+ 1 1)")
    ; => 
    2
[/code]

Remember, we evaluate recursively, so we can do some intricate stuff already:

[code]

    (eval (env) (read-string "(+ 1 (+ 1 fav-num))")
    ; => 
    43
[/code]

### Introducing def

Oky doke, we have an environment, we got symbols that can look stuff up in
that environment, and we can even evaluate `(+ 1 (+ 1 fav-num))`.

But, how are we going to _define_ variables? For example, let’s say we wanted
to have the symbol `second-fav` point to `42`.

Well, we can introduce a special form. Something like this:

[code]

    (def second-fav (+ 1 fav-num))
[/code]

If we receive this `def` form, we’d just update our environment, to point the
symbol `second-fav` to whatever the evaluation of `(+ 1 fav-num)` would be.

### Evaluating def

That sounds like a plan. Let’s detect this form first:

[code]

    (def def? (partial seq-starts-with? 'def))
[/code]

And update `eval` to handle it:

[code]

    (defn eval [env form]
      (cond
        (literal? form) form
        (quote? form) (second form)
        (symbol? form) (lookup-symbol env form)
        (def? form) (eval-def env form)
        :else (eval-application env form)))
[/code]

And here’s all `eval-def` would need to do:

[code]

    (defn eval-def [env [_ k v]]
      (assert (symbol? k) (format "expected k = %s to be a symbol" k))
      (.put (:globe env) k (eval env v)))
[/code]

Here, we know the first argument to `def` is the symbol, `k`. The second is
the _value_ `v` we want to save. So, we update our environment’s `globe`
Hashmap, and point the symbol `k`, to whatever `(eval env v)` is. In our case,
`k` would be `second-fav`, `v` would be `(+ 1 fav-num)`, and `(eval env v)`
would become `42`.

Prettyy cool, this works!

[code]

    (let [e (env)] 
        (eval e (read-string "(def second-fav (+ 1 fav-num))"))
        (eval e (read-string "second-fav")))
    ; => 
    42
[/code]

### Introducing if

Okay, let’s implement one more special form. We need something to handle
conditional logic:

[code]

    (if (= fav-num 41) 'yess 'noo))
[/code]

When we get `if`, we’ll can evaluate the test form: `(= fav-num 41)`. If
that’s true, we’ll then evaluate the true case `'yess`. Otherwise, we’ll
evaluate the false case: `'noo`. Sounds like a plan.

### Evaluating if

To implement if, as usual let’s detect it first:

[code]

    (def if? (partial seq-starts-with? 'if))
[/code]

Then use it in `eval`:

[code]

    (defn eval [env form]
      (cond
        (literal? form) form
        (quote? form) (second form)
        (symbol? form) (lookup-symbol env form)
        (def? form) (eval-def env form)
        (if? form) (eval-if env form)
        :else (eval-application env form)))
[/code]

And here’s what `eval-if` could look like:

[code]

    (defn eval-if [env [_ test-form when-true when-false]]
      (let [evaled-test (eval env test-form)]
        (eval env (if evaled-test when-true when-false))))
[/code]

Just a few lines, following our description to a tee. We see if `evaled-test`
is true. Then, we either evaluate `when-true`, or `when-false`.

While we’re at it, let’s add a bunch of nice primitive functions in our `env`:

[code]

    (defn env [] {:globe (HashMap. {'+ + '= = 'list list 'map map 'concat concat
                                    'first first 'second second 'not not 'fav-num 41})})
[/code]

And bam. Our little interpreter can do quite a lot now!

[code]

        (eval (env) (read-string "(if (= fav-num 41) 'yess 'noo)"))
        ; => yess
[/code]

### Introducing Functions

Let’s take things up a notch. We have Clojure’s `+` and so on, but what if our
programmer wanted to write _their own_ functions? Here’s an example:

[code]

    ((clo (x) (+ x fav-num) 2))
[/code]

Here, the programmer wrote a function that takes `x` and adds `fav-num` to it.

Say they wrote this. How can we run their function? Well, their definition has
an `arguments` and a `body`. In this case, it’s `(x)` and `(+ x fav-num)`
respectively. In this example, the function is called with `2`.

Here’s the insight: If we could just evaluate `(+ x fav-num)`, in an
environment where `x` points to `2`, voila, it’ll be like we _ran_ the
function! Here’s a diagram to explain the idea:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzE1MDY1NTc2OC00MzBkN2ZjMC05MDQyLTQ0ZGUtYmYyOS0zNjM4ZjA5YTllYzkucG5n)

How can we point `x` to `2`? We can’t just update our our `globe` Hashmap,
because then `x` would be _permanently_ set to `2`, even when the `body` was
done evaluating.

So we want a new idea. A `scope`. We can think of `scope` as an environment,
where the changes we make only last while `body` is being evaluated. If we can
introduce a concept like this, we’ll have functions!

### Evaluating Functions

Okay, let’s get this to work. First, let’s make sure that if someone writes
`(clo (x) (+ x 1))`, we don’t actually try to `eval-application`. Instead, we
should treat this as a new `closure` literal.

We can detect it:

[code]

    (def closure? (partial seq-starts-with? 'clo))
[/code]

And update our `literal?`:

[code]

    (def literal?
      (some-fn string? number? boolean? char? nil? fn? closure?))
[/code]

Now, if a user just writes a function, it’ll return itself:

[code]

    (eval (env) (read-string "(clo (x) (+ x fav-num))"))
    ; => (clo (x) (+ x fav-num))
[/code]

Next, let’s update our `environment`, to have a new `scope` map:

[code]

    (defn env [] {:globe (HashMap. {'+ + '= = 'list list 'map map 'concat concat
                                    'first first 'second second 'fav-num 41})
                  :scope {}})
[/code]

And let’s update `lookup-symbol`, to _also_ look up variables in scope:

[code]

    (defn lookup-symbol [{:keys [globe scope]} sym]
      (let [v (some (fn [m] (when (contains? m sym) [(get m sym)]))
                    [globe scope])]
        (assert v (format "expected value for sym = %s" sym))
        (first v)))
[/code]

Closer and closer. Now let’s make it run. If we wrote this:

[code]

    ((clo (x) (+ x fav-num)) 1)
[/code]

This list would go to `eval-application`. Let’s update it:

[code]

    (defn eval-application [env [f & args]]
      (let [f-evaled (eval env f)]
        (cond
          (fn? f-evaled) (apply f-evaled (eval-many env args))
          (closure? f-evaled) (eval-closure env f-evaled (eval-many env args)))))
[/code]

`f-evaled` would be `(clo (x) (+ x fav-num))`. This would mean `(closure?
f-evaled)` would become true.

We’d evaluate every argument with `(eval-many env args)`, which would be
`(1)`, and give this off to `eval-closure`. Here’s how `eval-closure` could
look:

[code]

    (defn eval-closure [env [_ syms body] args]
      (eval (assoc env :scope (assign-vars syms args)) body))
[/code]

We’d do exactly as we did in the diagram. We’d get `syms`, which would be
`(x)`, and `args`, which would be `(1)`. We’d then create a new scope:

[code]

    (defn assign-vars [syms args]
      (assert (= (count syms) (count args))
              (format "syms and args must match syms: %s args: %s"
                      (vec syms) (vec args)))
      (into {} (map vector syms args)))
[/code]

That’s `{x 2}`. We’d merge it into our environment, and then evaluate `body`.

All of a sudden, `(+ x fav-num)` will become `43`!

[code]

    (eval (env) (read-string "((clo (x) (+ x fav-num)) 2)"))
    ; => 43
[/code]

### Introducing Lexical Scope

Now, these functions are fine and all, but we can do _more._ Many languages
support lexical scoping. For example, we can do this in javascript:

[code]

    const makeAdder = (n) => (a) => n + a
    const addTwo = makeAdder(2);
    addTwo(4) 
    // => 
    6
[/code]

Here, `makeAdder` returned a function. This function remembered the value of
`n` _where it was defined_. How can we make this work in our own language?

Okay, first things first, let’s say that we let the programmer see the current
scope. Here’s an example of what I mean:

[code]

    ((clo (x) scope) 2)
    ; => 
    {x 2}
[/code]

This special `scope` symbol, when evaluated returned `{x 2}`, the _current_
scope!

Nice now, what if we updated our function literal? It could look something
like this:

[code]

    (clo {n 2} (a) (+ n a))
[/code]

Here, we have a special spot for the `scope`! When we define the function, if
we could just “plop” the scope of wherever it was defined in there, badabing
badaboom, we’d support lexical scoping!

Here’s how our `make-adder` could work:

[code]

    (def make-adder (clo nil (n) 
                      (list 'clo scope '(y) '(+ y n)))) 
    (def add-two (make-adder 2))
    (add-two 4)
    ; => 
    6
[/code]

When we run `(make-adder 2)` we’d evaluate `(list 'clo scope '(y) '(+ y n))`.
That would return `(clo {n 2} (y) (+ y n))`! All of a sudden, we support
lexical scoping.

You may think it’s weird that we wrote `(list 'clo scope '(y) '(+ y n)))` —
quote verbose. But, hey, we’ll support macros soon, and that help us write
this in a spiffy way. Just you wait 🙂.

### Implementing Lexical Scope

Okay. that’s a lot of explaining, but the changes will be simple. First we
need to make sure that if we get a `scope` symbol, we return the current
scope:

[code]

    (defn lookup-symbol [{:keys [globe scope]} sym]
      (let [v (some (fn [m] (when (contains? m sym) [(get m sym)]))
                    [{'scope scope} globe scope])]
        (assert v (format "expected value for sym = %s" sym))
        (first v)))
[/code]

And now all we need to do, is to update `eval-closure`:

[code]

    (defn eval-closure [env [_ scope syms body] args]
      (eval (assoc env :scope (merge scope (assign-vars syms args))) body))
[/code]

Here we take the `scope` _from_ the closure itself! With that, lexical scoping
works!

[code]

    (((clo nil (x)
            (list 'clo scope '(y) '(+ y x))) 2) 4)
    ; => 
    6
[/code]

### Introducing Macros

Now, we have all we need to implement macros! Let’s think about what macros
really are.

Imagine writing the function `unless`:

[code]

    (def unless (clo nil (test v)
                  (if (not test) v)))
[/code]

Will it work? If we ran `(unless (= fav-num 41) 'yes)`, it _would_ return the
symbol `yes`.

But what if we ran this?

[code]

    (unless (= fav-num 41) (throw-error))
[/code]

Since `unless` is a function, we would evaluate each argument first right? In
that case, we’d evaluate `(= fav-num 41)`, which would be `true`. But, we’d
_also_ evaluate `(throw-error)`. That would break our program. This defeats
the whole purpose of `unless` , as `(throw-error)` was supposed to run _only_
when `test` was false.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzE1MDY1NTc3Mi1hNTlmNGJkOC1mNDc1LTQxMGMtODFmYi02YWI2NjlhNDY1OTEucG5n)

Now, imagine we wrote the _macro_ unless:

[code]

    (def unless (mac (clo nil (test v)
                        (list 'if (list 'not test) v))))
[/code]

If we ran `(unless (= fav-num 41) (throw-error))`, here’s what would happen:

The value of `test` would not be `true`, it would actually be the list `(=
fav-num 41)`. Similarly, we wouldn’t evaluate `(throw-error)` . `v` would just
be the actual list `(throw-error)`.

_The arguments to a macro are not evaluated._ When the macro runs, it returns
_code._ The result of

[code]

    (list 'if (list 'not test) v))
[/code]

would become

[code]

    (if (not (= fav-num 41)) (throw-error))
[/code]

And when we evaluated _that,_ things would work as expected! `(throw-error)`
would never evaluate.

This is the key difference between functions and macros. Functions take
_evaluated values_ as arguments and return evaluated values. Macros receive
_unevaluated_ arguments, return _code, and that code is evaluated._

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzE1MDY1NTc3OS1mMDMxNWQyNS1lZjZlLTQzYjktOTBiNy1jMmYyMDE2YTkyOGIucG5n)

An important piece to note is that we eval _twice._ We give the macro the
unevaluated arguments, which returns new code, and we once again _evaluate_
that.

So, how can we support this?

### Evaluating Macros

So much explanation, for such little code. Are you ready? Let’s add macros.

First, let’s use this new structure for a macro: a macro is a list that begins
with `mac`, and has closure inside:

[code]

    (mac (clo nil (...))
[/code]

We can detect macro, and mark it as a literal:

[code]

    (def macro? (partial seq-starts-with? 'mac))
        
    (def literal?
      (some-fn string? number? boolean? char? nil? fn? closure? macro?))
[/code]

Next, we’ll want to update `eval-application`:

[code]

    (defn eval-application [env [f & args]]
      (let [f-evaled (eval env f)]
        (cond
          (fn? f-evaled) (apply f-evaled (eval-many env args))
          (closure? f-evaled) (eval-closure env f-evaled (eval-many env args))
          (macro? f-evaled) (eval-macro env f-evaled args))))
[/code]

Before we always ran `(eval-many env args)`. But this time, if it’s a macro,
we pass in `args` directly! That’s the ”code” itself 🙂.

And now for `eval-macro`:

[code]

    (defn eval-macro [env [_ clo] args]
      (eval env
            (eval env (concat [clo] (map (partial list 'quote) args)))))
[/code]

Oh my god. 3 lines!! We do exactly as we said in our diagram:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzE1MDY1NTc5MC02MWFhOTQ5OC05NDgzLTQ4ODYtOGRiMC1lYmM3NzE1OTM2MzkucG5n)

We take the “closure” out of our macro, and _run_ it with _unevaluated_ args.
We can do that just by wrapping each `arg` in a quote: `(map (partial list
'quote) args)`.

Once we have the resulting code, we _evaluate_ that again, and boom, we have
macros.

[code]

    (def unless (mac (clo nil (test v)
                        (list 'if (list 'not test) v))))
    ; works!
    (unless (= fav-num 41) (throw-error))
[/code]

## Your own Macros

Okay, we have a Lisp that supports macros. Let’s go ahead and write some of
our own!

### defmacro

Let’s get meta off the bat. Notice what we do when we define a macro:

[code]

    (def unless (mac (clo nil (test v)
                          (list 'if (list 'not test) v))))
[/code]

This whole `(mac (clo nil …))` business is a bit unnecessary. Let’s just write
macro that does this for us!

[code]

    (def defmacro
          (mac (clo nil (n p e)
                    (list 'def n
                          (list 'mac (list 'clo nil p e))))))
[/code]

This generates the code `(def n (mac (clo nil …)))`. Now we could write:

[code]

    (defmacro unless (test v) 
      (list 'if (list 'not test) v))
[/code]

Cool!

### fn

Okay, remember how we wrote our function for lexical scoping?

[code]

    (def make-adder (clo nil (n)
                          (list 'clo scope '(y) '(+ y n))))
[/code]

Let’s have a macro write this for us:

[code]

    (defmacro fn (args body)
                  (list 'list ''clo 'scope
                        (list 'quote args)
                        (list 'quote body)))
[/code]

Here’s what happens if we wrote:

[code]

    (def make-adder (clo nil (n)
                        (fn (y) (+ y n))))
    
    (def add-two (make-adder 2))
[/code]

When the macro expansion for `fn` runs, the `args` would would be `(y)` and
`body` `(+ y n)`. So

[code]

    (list 'list ''clo 'scope
          (list 'quote args)
          (list 'quote body))
[/code]

would expand to

[code]

    (list 'clo scope '(y) '(+ y n))
[/code]

and that’s _exactly_ what we wrote by hand! Bam, now we can use `fn` instead
of this whole `'clo scope` business.

### defn

Now if we wanted to define functions, we could write:

[code]

    (def add-fav-num (fn (x) (+ x fav-num)))
[/code]

But we can make it tighter. Let’s add a `defn` macro, so we could write:

[code]

    (defn add-fav-num (x) (+ x fav-num))
[/code]

Easy peasy:

[code]

    (defmacro defn (n args body)
      (list 'def n (list 'fn args body)))
[/code]

### let

One more cool macro. Right now, there’s no real way to define temporary
variables. Something like:

[code]

    (let ((x 1) (y 2)) 
      (+ x y))
    ; => 
    3
[/code]

How could we support it? Well, what if we _rewrote_ `(let …)` to:

[code]

    ((fn (x y) (+ x y)) 1 2)
[/code]

We could just use the argument list of a function to create these variables!
Perfecto. Here’s the macro:

[code]

    (defmacro let (pairs body)
      (concat (list (list 'fn (map first pairs) body))
                    (map second pairs)))
[/code]

## Fin

What a journey. 80 lines, 4000 words, and hopefully a fun time 🙂. You now have
a Lisp with macros, and you’ve written some cool ones yourself. Here’s the
[full source](https://github.com/stopachka/llisp/blob/main/src/llisp/core.clj)
if you’d like to follow along from there.

 **Credits**

The idea to represent macros and closures like this, came from PG’s
[Bel](http://www.paulgraham.com/bel.html).

_Thanks to Mark Shlick, Daniel Woelfel for reviewing drafts of this essay._

