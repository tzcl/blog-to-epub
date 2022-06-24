# Macros by Example


I was in a conversation recently about the power of macros, and the use of
syntactic abstraction in building simpler systems.

We quickly realized though: it’s tough to convey in a conversation _what’s so
special about macros._ What can you do with macros that you couldn’t do with
functions?

In this essay, we’ll use 2 examples, alongside some imaginary javascript
syntax and lisp [1] to explore that question!

 ** _Note:_** _This tutorial assumes you have a light understanding of lisp
syntax. Go through[this tutorial](https://www.braveclojure.com/do-things/) to
brush up if you haven’t gotten to explore lisp yet._

 ** _Note:_** I’ve been meaning to write this for weeks, but was worried that
it would be confusing. I am going to apologize now if that’s how you end up
feeling when you read this. There may be a better way to explain it, but I
needed to get this out of the head. If you have any feedback on how I could
make this simpler, please let me know 🙂

[1] The specific language is Clojure, but anything done here can be done with
any lisp

## Example 1: nullthrows

With this example, let’s gain an intuition for _when_ macros run and why that
can be powerful.

### Context

In any language with nulls, there’s a nullthrows abstraction: If some value
evaluates to null, throw it.

Here’s how we could implement that as a function in javascript:

[code]

    function nullthrows(result) {
      if (result === null || result === undefined) {
        throw new Error("uh oh");
      } 
      return result;
    }
[/code]

So if we run it, and it evaluates to null, we’ll throw an exception

[code]

    nullthrows(getUser(db, 'billy'))
    // if it's null, throw Exception
[/code]

This works great…but there’s a problem. _What would our stacktrace look like?_

[code]

     index.html:700 Uncaught Error: uh oh
        at nullthrows (index.html:700)
        at someStuff (index.html:1325)
        ...
[/code]

When some value is null, the stacktrace won’t have much helpful information.
It will say which line threw, but we’d have to do some digging each time to
find out where the code was.

One way we can fix that, is to pass in a message argument

[code]

    nullthrows(getUser(db, 'billy'), 'expected billy');
    
    function nullthrows(result, message) {
      if (result === null || result === undefined) {
        throw new Error(`uh oh: ${message}`);
        ...
[/code]

This could work…buut

### Challenge

What if I told you: **I don’t want to _have_ to pass in a message.**

Instead, when the _source code_ that `nullthrows` wraps is specific enough,
I’d be just as happy if the error printed the offending piece of code.

For example, with `nullthrows(getUser(db, ‘billy'))`, `nullthrows` is wrapping
the source code `getUser(db, ‘billy’))`

If the error printed out `“Uh oh, this returned null: getUser(db, ‘billy’)”`,
it would be specific enough, and I wouldn’t need a custom error message.

### Problem

Well, by the time `nullthrows` is run, `getUser(db, ‘billy’)` will be long
gone: all the function will see is the _evaluation_ of `getUser(db, ‘billy’)`.
Since the evaluation will be null, there’s not much information we can gain.

### Javascript Solution

To actually _capture_ and work on source code, we need a new kind of
abstraction.

This would be some kind of function, that does two things:

  1. It would take snippets of source code as input, and return new snippets of source code as output
  2. This abstraction would be called at the build step, and replace the source code snippets that it takes in, with those new source code snippets.

Let’s say Javascript had that. instead of `function nullthrows`, we would have
`macro nullthrows`. It could look something like this:

[code]

    macro nullthrows(sourceCodeSnippet) {
      return `
        const result = ${sourceCodeSnippet}; 
        if (result === null || result === undefined) {
          throw new Error("Uh oh, this returned null:" + ${stringify(sourceCodeSnippet)});
        } else {
          return result;
        }
      `;
    }
[/code]

Here, the input would be the _actual source code._

Whenever it’s called, we would replace that piece of code, the source code
snippet that this abstraction generates.

For example, during the build step `nullthrows(getUser(db, ‘billy’))` would be
replaced with:

[code]

    const res = getUser(db, 'billy'); 
    if (res === null || res === undefined) {
      throw new Error("Uh oh, this failed:" + "getUser(db, 'billy')");
    } else {
      return res;
    }
[/code]

Now, you might see some potential problems here:

Snippets are just text! It’s really had to programmatically add/remove/edit
text without causing a bunch of syntax errors. Imagine if you wanted to change
the source code, based on _what_ it was — is it a functional call or a value?
— there would be no way to tell with just text.

With javascript, you can work on the abstract syntax tree itself with babel
transforms, but that will make the implementation quite different from what we
want our code to be doing.

We really want to use some better data-structures to represent our code. Turns
out, this idea isn’t new: there’s a whole family of languages — the lisp
family — that wanted code to be represented with data-structures so we could
read/generate code snippets more easily.

It seems like a lot of work just to make a built-in code-snippet-generator for
a language, but let’s see what our challenge looks like if we use lisp’s
approach:

### Lisp solution

Since all code in lisp, are just lists, our lisp macro takes in a _list of
code,_ and returns a new _list of code_

We would write nil-throws like this:

[code]

    (nil-throws (get-user "billy"))
[/code]

The function variant would look like this:

[code]

    (defn nil-throws [res]
      (if (nil? res)
        (throw "uh oh")
        res))
[/code]

Now, I’m going to show you how the macro variant would look like: (don’t worry
about a few of the symbols you’ll see, they’re all simple and I’ll explain
them in just a few words below)

[code]

    (defmacro nil-throws [form]
      `(let [result# ~form] ;; assign the evaluation of form to result#
        (if (nil? result#)
          (throw
            (ex-info "uh oh, we got nil!" {:form '~form})) ;; save form for inspection
          result#)))
[/code]

Here’s how we can think about it:

  1. Similar to how we wrote ``` in javascript, the backtick here does the same thing: it says, hey, here’s the code I want to return, don’t evaluate it right away.

  2. `#` is a handy way to generate some symbol, that won’t interfere with any other symbol when this code gets replaced in a different scope.

  3. `~` is like our interpolation `${}` in javascript, but for lists

  4. `‘` is a way to say: hey, I want to treat something as a list, and don’t want to evaluate it

This would make it so when we write: `(nil-throws (get-user db “billy”))`

It would be replaced (~approximately) with:

[code]

    (let [result# (get-user db "billy")]
      (if (nil? result#)
        (throw (ex-info "uh oh, we got nil!" {:form '(get-user db "billy")})) 
        result#))
[/code]

Wow…we just wrote code that wrote more code…that’s pretty cool

### Lessons learned so far

Macros take _code_ as input, and return _code_ as output. They run during the
build step

## Example 2: pipe syntax

Now, let’s explore the kind of power this can give us.

### Context

The [pipe operator](https://docs.hhvm.com/hack/expressions-and-operators/pipe)
is quite common in a bunch of languages.

It takes code that you would normally write like this:

[code]

    createBill(addToCart(cart, updatePrice(item, 100)))
[/code]

And let’s you invert the flow visually:

[code]

    item |> updatePrice($$, 100) |> addToCart(cart, $$) |> createBill
[/code]

### Challenge

What if our language didn’t have this, and we wanted to implement it? Maybe
we’d want our syntax to look like this:

[code]

    |> [
      item, 
      updatePrice($$, 100), // updatePrice(item, 100)
      addToCart(cart, $$), // addToCart(cart, updatePrice(item, 100))
      createBill, // createbill(addToCart(cart, updatePrice(item, 100)))
    ]
[/code]

### Problem

Now, we could do this by implementing a pipe function:

[code]

    pipe(item, (item) => updatePrice(item, 100))
[/code]

But we would need to introduce anonymous functions, and the code would be less
concise.

 _The only way to do this to spec, would be to change the syntax itself._

### Javascript Solution

Now, with our imaginary javascript syntax, we could write something like this:

[code]

    macro |> (listOfForms) {
      return listOfForms.reduce(
        (lastForm, thisForm) => {
          if (isFunctionalCall(thisForm)) {
            return `
              let $$ = ${lastForm};
              ${thisForm};
            `;
          } else {
            return `${callFunction(thisForm, lastForm)}`;
          };
      });
    }
[/code]

Here, would start with a list of the forms, un-evaluated:

[code]

    [item, updatePrice($$, 100), addToCart(cart, $$), createBill]
[/code]

Reduce would start with the arguments `lastForm = item, thisForm =
updatePrice($$, 100)`

Now, we would need a way to know: is this a form of a function call
`updatePrice($$, 100)`, or just a function: `createBill`

If it’s a function call, we can create new code, which defines `$$` as the
last form, and evaluate the function call within that scope.

Otherwise, we can create new code, which calls that function with the last
form.

### Lisp Solution

What we want would be something like this:

[code]

    (|> item
        (update-price $$ 100)
        (add-to-cart cart $$)
        create-bill)
[/code]

And our macro could look like this:

[code]

    (defmacro |> [form & forms]
      (reduce
        (fn [last-v form]
          (if (seq? form) ;; am I being called: (update-price $$ 100)
            `(let [~(symbol "$$") ~last-v]
               ~form)
            `(~form ~last-v))) ;; or am I just a function: create-bill
        form
        forms))
[/code]

Our lisp code would follow the same idea as our Javascript solution. Let’s see
the code we didn’t have to write:

[code]

    (create-bill 
      (let [$$ (let [$$ item]
                 (update-price $$ 100))]
        (add-to-cart cart $$)))
[/code]

…that’s pretty cool. We get the best of both worlds: efficient, well-erroring
code that’s short to write and — most importantly — clear to read.

### Lessons learned so far

Macros let you _change the language itself._ You can transform code and change
the syntax.

## Conclusion

Macros let you change your language to suit your problem. This is extremely
powerful: You can build up your language so you can express your problem as
clearly as possible. This makes your code more concise and simple, which in
turn makes your system more malleable.

At the same time, macros…change the language itself. There are few moments
where this level of abstraction is warranted, so if you use them when simpler
abstractions would do, you risk adding unnecessary complexity.

Yet… when they _are_ warranted, having them as an option can change the game.

## Further Reading and Practice

If this got you interested, here’s some reading and practice you may enjoy:

  * Read Norvig’s Paradgims of AI Programming, and do the homework
  * Read Clojure for The Brave and True’s Macro Guide, and do the homework
  * Look into how Clojure uses macros to define the language itself (when, and, or, etc)
  * Write async await syntax for promises

## Credits

 _Shoutout to Daniel Woelfel: I saw his nil-throws macro years back when we
worked together, and it opened my eyes to the power of syntactic abstraction._

 _Thanks to Sean Grove, Daniel Woelfel, Martin Raison, Alex Reichert, Mark
Shlick for a beautifully deep review of this essay._

 _Thanks to Paul McJones, perfunctory and tzs, for their feedback on the code
examples._

