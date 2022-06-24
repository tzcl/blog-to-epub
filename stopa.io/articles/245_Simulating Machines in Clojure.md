# Simulating Machines in Clojure


[My cofounder Joe and I recently finished
SICP.](https://twitter.com/stopachka/status/1295411936625074178) It was a
mind-bending experience: you start from just 3 concepts, and you recursively
build up algebraic equation solvers, circuit simulators, 4 interpreters, and a
compiler.

At some point you experience a visceral feeling: If you were dropped in a
forest…you could create your own computer. The project that contributed most
significantly to this feeling was creating a machine simulator.

We diverged from the book by writing the simulator in Clojure rather than
Scheme. Immutable data structures and higher-level concepts available to us in
Clojure compressed the solution, to the point where I think you can build your
own in a few days worth of hacking.

This essay will guide you through doing just that: let’s build a machine
simulator, over a good few days worth of hacking! I hope this inspires you to
play with Clojure and to take a deeper look at SICP.

## Concrete Machine

Before we simulate general machines, let’s think about a concrete machine.
**How could we create a machine that could figure out factorials?**

If we were writing code, factorial could look something like this:

[code]

    (defn factorial [n]
      (loop [res 1
             counter 1]
        (if (> counter n)
          res
          (recur
            (* counter res)
            (inc counter)))))
[/code]

Let’s see if we could build factorials using _physical_ devices.

## A: Storing Numbers

Well, we need a way to keep track of `counter`, `res`, and `n`. To do that,
we’ll need a device that stores information.

### Bulbs

Imagine a device that has some light bulbs inside of it.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUwNDUyLTFlNzkzODgwLTA3ZTgtMTFlYi04MjI4LWQwYzE4ZTcwNTZhYS5wbmc)

We can say that if a light bulb is _on,_ that represents the number 1, and if
a light bulb is _off_ that represents the number 0.

If we had a bunch of light bulbs in the device, we could interpret the state
of these bulbs as larger and larger binary numbers. The light bulbs in the
device I just showed you for example, would represent “10101”, which is binary
for “21”.

### Incoming Current

Now, imagine that at all times there are a bunch of other wires connected to
this device. These wires carry “new” charges for the light bulbs, but with a
twist: the incoming charges _do not_ affect the light bulbs inside just yet.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUwNjIxLTVhMTQwMjgwLTA3ZTgtMTFlYi05ZjM2LTU2MDFkZTIyOWUwOS5wbmc)

Notice how the _incoming charge_ for the “a” light bulb is “off”, but the bulb
inside is still on. Conversely, the incoming charge "b" is "on", but the bulb
is off. If our device can do this, it means that whatever the charges for the
light bulbs are inside is a _stored value_. Very cool!

### Save

Now, we need these incoming wires to do something at some point. What if this
device had a “save” button.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUwNjQ1LTYzMDRkNDAwLTA3ZTgtMTFlYi04NjVjLWE3YTg3OTE5Njg3ZC5wbmc)

Once we pressed “save”, the incoming current would transfer inside the box:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUwNjU0LTY3Yzk4ODAwLTA3ZTgtMTFlYi04MjU1LTExNmEzMGUxNTcwMy5wbmc)

Here, light bulb “a” changes from “on” to “off”, and the light bulb "b"
changed from "off" to "on".

Great, now we have a way to “save” new numbers inside!

### Outgoing current

We also need a way to share the state of what’s inside to other devices. All
we’d need to do to make that work, is to have a bunch of wires that leave our
device, which carry the sames charges as the light bulbs:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUxNzQ2LWY5ODVjNTAwLTA3ZTktMTFlYi05YzczLTY4ZWYwNzc3OGJlMi5wbmc)

Now, if we hooked those outgoing charges to some other device, that device
would receive the “number” that was stored in this one.

### Registers

What we just described is analogous to a computer’s _register_ (1). Registers
let us store and share information.

Now, we could use three registers to store the value of `res` `counter` and
`n`.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUwODUxLWIxYjI2ZTAwLTA3ZTgtMTFlYi04NzRjLTQxODgyODAxNTQ2OC5wbmc)

## B: Adding Numbers

Next up, we’ll need a device that that can “add” two registers. Imagine a
device that had two register’s worth of incoming wires, and one register’s
worth of outgoing wires:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUwODY5LWI4ZDk3YzAwLTA3ZTgtMTFlYi05ZDM0LTQwMDE0YmQ5NDAyOC5wbmc)

### Adder

If the device could connect those incoming wires in such a way, that the
outgoing wires represented the “addition” of those registers, we’d have an
“adder” device!

In the example above, the left register represents “10101” (21), and the right
represents “00001” (1). The output wires are charged as “10110”…which
represent 22!

## C: Multiplying numbers

Similarly, we could have a device that has two register’s worth input wires,
and one register’s worth of output wires:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUwODkyLWMxMzFiNzAwLTA3ZTgtMTFlYi05OTQ1LTI4ZDljNmU4N2IzNy5wbmc)

### Multiplier

If we could connect the incoming wires in such a way, that the outgoing wires
represent the result of a multiplication, boom we would have a multiplying
device!

The left register above represents “00101” (5), the right register represents
“00010” (2), and the charge of the outgoing wire is “01010” (10). Nice! That
gives us a multiplier machine.

### Comparator

We need one more device. Imagine a device that takes two register’s worth of
input wires, and only has _one_ output wire:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUwOTE1LWNhMjI4ODgwLTA3ZTgtMTFlYi05Y2RiLWM2ZDEwZTYxNzc1Yi5wbmc)

If we could combine the input wires in such a way, that the output wire was
“on” when the left register was bigger, and off otherwise, we could use this
as a comparator machine!

## E: Data Paths

If we had all these machines, we can wire them in such a way, that lets us
compute factorials:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUwOTg1LWRlZmYxYzAwLTA3ZTgtMTFlYi05MDRjLTE2NmUzNTIyMjJkOS5wbmc)

Here, we wired the output wires of `res` and `counter` to the `*` machine. We
wired the output wires of the `*` machine, to _be_ the input wires of `res`.

This way, if we press “A”, we would “store” the result of multiplying
`counter` with `res`!

Similarly, we wired up the output wires of `counter` and a register that keeps
the value `1`, to the `+` machine. We wired the output wires of the `+`
machine, to _be_ the input wires of `counter`.

Now, If we pressed “B”, `counter` would be stored with the result of adding
`1`!

Next up, we also wired up `counter` and `n` with the `>` machine. If we hooked
up a light bulb to the output wire of the `>` machine for example, then
whenever it was on, we would know that `counter` was larger than `n`.

We’ve just drawn out the “data path” of our machine.

## F: Controller

### Manual Recipe

Let’s remember our code for factorial:

[code]

      (loop [res 1
             counter 1]
        (if (> counter n)
          res
          (recur
            (* counter res)
            (inc counter))))
[/code]

Imagine if we had our “data path” machine. What would happen if we followed
the following recipe:

  1. Take a look at the output of the `>` machine. 
  2. If the light bulb connected to the `>` machine is on, **stop**

 _Otherwise…_

  1. "Press A". This will update `res` with the result of the `*` machine on `res` and `counter`
  2. “Press B“. This will update `counter` with the result of the `+` machine on `1` and `counter`
  3. Go back up to the start of the recipe

 **If we did this over and over again, once the light bulb connected to the
output of the** **`>`** **machine turns on,** **`res`** **would contain the
result of factorial!**

### Automation

Pretty cool, but this kind of manual work would be annoying. If you look at
these instructions though, there’s a pretty significant insight: _all of those
instructions are simple: "look at charge of light bulb", "press button..."_

In fact, they’re so simple that we could wire up a machine that goes through
that recipe! Imagine if we created a machine that could “press” buttons for
us, depending on whether the output wire of the `>` machine is on:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUxMDIwLWU5MjExYTgwLTA3ZTgtMTFlYi04MDJlLTI4YzIyNjZiNzQwOC5wbmc)

We would be able to automate computing factorials 🙂

### Balls and Hills

Now, at this stage, you may be wondering: exactly _how_ would `*` produce
output wires that represent the multiplication? How would `+` work, and how
would the `controller` move along?

If you think about it, these can all be reduced to very simple machines. They
don’t even necessarily have to be electronic:

Imagine you had a ball rolling down some hill. You could construct something
like the `>` machine, by putting `res` and `counter` on a scale: based on
what’s bigger, the ball would take a different path

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUxMDQ4LWY4MDdjZDAwLTA3ZTgtMTFlYi04NTg3LWRiYjE2ZDU3NGZkMy5wbmc)

With sufficient energy, space, time, and ingenuity you really could build all
of this with a ball on a hill. Now, you wouldn’t necessarily do that (2), but
you can imagine how the electronic parts that make up our machines are
similarly simple, logical machines: _turn on if off, turn off if on, etc_.
These logical machines are called “logic gates”. You can look them up, but
hopefully I’ll have an essay for you about these machines soon 🙂.

## Language Simulation

Now, we drew out our machine and saw how we could build them with simple
devices. How could we simulate these machines?

To simulate these machines, we need to transform our _picture descriptions_
into something that computers can manipulate. Computers can manipulate text
much better: let’s create a _language_ for describing these machines.

If we remember the pictures again:

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUxMTg3LTJmNzY3OTgwLTA3ZTktMTFlYi05ZTNlLTg3Zjg0NDkxZjQxYS5wbmc)

we could transform them into a language that looks like this:

[code]

    (def factorial-instructions
      '(
         start
    
         (test (op >) (reg counter) (reg n))
         (branch (label done))
    
         (assign res (op *) (reg counter) (reg res))
         (assign counter (op +) (reg counter) (const 1))
         (goto (label start))
    
         done))
[/code]

When the `test` instruction runs, we run the `>` machine with `counter` and
`n`.

Our `branch` instruction checks if the `test` instruction said `yes`. If it
did, it moves to `done`. Otherwise it no-ops and the machine moves forward by
one.

After that, our `(assign res` expression is analogous to “press A”. `(assign
counter` is analogous to “press B”, and `(goto (label start)` is analogous to
the arrow bringing us back to the start.

With this textual representation, we can build an interpreter and simulate our
machine. Let’s do this!

## 0: Machine State

What does the state of our machine look like in Clojure? Well, how do we
represent most things in Clojure? With maps! Let’s represent the state of our
machine as a map:

[code]

    (def ex-machine-state-v0
      {:registry-map {'n 10 'res 1 'counter 1}
       :label->idx {'start 0 'done 5}})
[/code]

`registry-map` could keep a mapping of registers to values. `label→idx` could
keep a mapping of labels to their `idx` in the instruction list

## 1: primitive

With this, we can get the most foundational part of our language to work: We
use `(const…` `(reg...` and `(label…` all over the place.

  1. If our machine sees `(const 1)`, it should return the actual value `1`
  2. If our machine sees `(reg foo)`, it should look up whatever is in the `foo` register, and return that 
  3. If our machine sees `(label foo)`, it should return the correct index in our instruction list.

Let’s write this out in Clojure:

[code]

    (def tag first) ; (tag '(const 1)) => const
    (defn tag-of? [sym s] (= sym (tag s))) ; (tag-of? 'const '(const 1)) => true
    
    (defn parse-primitive [{:keys [registry-map label->idx] :as machine-state}
                           prim-exp]
      (condp tag-of? prim-exp
        'const
        (second prim-exp)
        'reg
        (get registry-map (second prim-exp))
        'label
        (label->idx (second prim-exp))))
[/code]

Our `parse-primitive` function takes the machine-state, and does the right
thing based on the `tag` of the expression.

[code]

    (parse-primitive ex-machine-state-v0 '(const 1))
    ; => 1
    (parse-primitive ex-machine-state-v0 '(reg n))
    ; => 10
    (parse-primitive ex-machine-state-v0 '(label done))
    ; => 5
[/code]

## 2: operation

Okay, we have primitives working, let’s move up a level. Our simulator gives
us access to some other machines, like `*` `+` and `>`

[code]

    '(... (op >) (reg counter) (reg n))
    '(... (op *) (reg counter) (reg res))
    '(... (op +) (reg counter) (const 1))
[/code]

When our simulator sees these instructions, it’ll need to look up the machine
that corresponds to the `op`, and run it with the primitive arguments that
were provided.

To do this, let’s evolve our machine-state:

[code]

    (def ex-machine-state-v1
      {:registry-map {'n 10 'res 1 'counter 1}
       :label->idx {'start 0 'done 5}
       :op-map {'* * '+ + '> >}})
[/code]

We’ve now introduced `op-map`. This maps `op symbols` to these other machines.

Now we could implement a function that parses operations:

[code]

    (def operation-sym (comp second first)) ; ((op >) ...) => >
    (def operation-args rest) ; ((op >) (reg counter) (reg n)) => ((reg counter) (reg n))
    
    (defn parse-operation [{:keys [op-map] :as data} op-exp]
      (let [op-fn (get op-map (operation-sym op-exp))
            evaled-args (map (partial parse-primitive data)
                             (operation-args op-exp))]
        (apply op-fn evaled-args)))
[/code]

And with that, our simulator can run operations:

[code]

    (parse-operation ex-machine-state-v1 '((op >) (reg counter) (reg n)))
    ; => false
    (parse-operation ex-machine-state-v1 '((op *) (reg counter) (reg res)))
    ; => 1
    (parse-operation ex-machine-state-v1 '((op +) (reg counter) (const 1)))
    ; => 2
[/code]

## 3: assign

Now it’s time to move up even higher, and start implementing our actual
instruction expressions.

Let’s start with assign. Assign has two forms. We can either assign a
primitive value:

[code]

    (assign counter (const 1)) ; {'counter 1}
[/code]

Or the result of an operation:

[code]

    (assign counter (op +) (reg counter) (const 1)) ; {'counter 2}
[/code]

Once assign completes, our machine state needs to “move forward” to the next
instruction.

To implement assign, we need to evolve our machine state again:

[code]

    (def ex-machine-state-v2
      {:registry-map {'n 10 'res 1 'counter 1}
       :label->idx {'start 0 'done 5}
       :op-map {'* * '+ + '> >}
       :idx 0})
[/code]

We now have a `idx` state, that tracks the machine’s current index in the
instruction list. This will let us “move” forward, by simply incrementing the
index.

Here’s how assign can look:

[code]

    (def assign-reg-name second) ; (assign foo ...) => foo
    (def assign-operator #(nth % 2)) ; (assign foo (const 1)) => (const 1)
    
    (def operation-exp?
      (comp (partial tag-of? 'op) assign-operator)) ; (assign foo (op ... => true
    
    (def assign-operation-exp (partial drop 2)) ; (assign foo (op *) ...) => ((op *) ...
    
    (defn exec-assign
      "Assign comes in two forms:
    
      (assign reg-name <primitive-op>)
      i.e (assign foo (const 1))
    
      (assign reg-name <operation> <args...>)
      i.e (assign foo (op *) (const 2) (reg foo))"
      [data ins]
      (let [reg-name (assign-reg-name ins)
            val (if (operation-exp? ins)
                    (parse-operation data (assign-operation-exp ins))
                    (parse-primitive data (assign-operator ins)))]
        (-> data
            (assoc-in [:registry-map reg-name] val)
            (update :idx inc))))
[/code]

And badabing badaboom, assign works as we expect:

[code]

    (select-keys (exec-assign ex-machine-state-v2 '(assign counter (const 0)))
                   [:registry-map :idx])
    ; => {:registry-map {n 10, res 1, counter 0}, :idx 1}
    (select-keys (exec-assign ex-machine-state-v2 '(assign counter (const 10)))
                   [:registry-map :idx])
    ; => {:registry-map {n 10, res 1, counter 10}, :idx 1}
[/code]

Note how `counter` changed, and `idx` moved up by 1

## 4: goto

Next up, let’s make `goto` work:

`(goto <primitive-exp>)` should set the `idx` in our machine to the resulting
value of a primitive expression:

[code]

    (def goto-dest second) ; (goto (label done)) => (label done)
    
    (defn exec-goto [data ins]
      (assoc data :idx (parse-primitive data (goto-dest ins))))
[/code]

Easy peasy:

[code]

    (select-keys (exec-goto ex-machine-state-v2 '(goto (label done)))
                   [:label->idx :idx])
    => {:label->idx {start 0, done 5}, :idx 5}
[/code]

`idx` was set to the value of `done`.

## 5: test-passed?

We are so close! Next up, let’s consider the `test` and `branch` instruction:

[code]

    (test (op >) (reg counter) (reg n))
    (branch (label done))
[/code]

Remember that when `test` runs, we need to figure out whether the `op`
returned a `yes` or `no`, and we move the machine forward. When `branch` runs,
we need to see if the last `test` instruction said yes. If it did, we jump to
the `branch destination`. Otherwise we no-op and move the instruction list
forward by one.

To implement this, we need to evolve our machine state one final time:

[code]

    (def ex-machine-state-v3
      {:registry-map {'n 10 'res 1 'counter 1}
       :label->idx {'start 0 'done 5}
       :op-map {'* * '+ + '> >}
       :idx 0
       :test-passed? false})
[/code]

`test-passed?` keeps track of the result of a `test` instruction.

## 6: test

With that, we can implement `test`:

[code]

    (def drop-tag rest) ; (test (op >) ...) => ((op >) ...)
    
    (defn exec-test [data ins]
      (-> data
          (assoc :test-passed? (parse-operation data (drop-tag ins)))
          (update :idx inc)))
[/code]

And bam:

[code]

    (:test-passed? (exec-test ex-machine-state-v3 '(test (op >) (reg counter) (reg n))))
    ; => false
    (:test-passed? (exec-test ex-machine-state-v3 '(test (op >) (reg n) (reg counter))))
    ; => true
[/code]

the machine’s `test-passed?` state is is set to the value of the operation.

## 7: branch

We can also implement `branch`:

[code]

    (def branch-dest second) ; (branch (label done)) => (label done)
    
    (defn exec-branch [data ins]
      (let [dest (parse-primitive data (branch-dest ins))]
        (if (:test-passed? data)
          (assoc data :idx dest)
          (update data :idx inc))))
[/code]

Let’s try it out:

[code]

    (exec-branch
        {:label->idx {'done 5} :test-passed? false :idx 0}
        '(branch (label done)))
    ; => {:label->idx {done 5}, :test-passed? false, :idx 1}
    (exec-branch
        {:label->idx {'done 5} :test-passed? true :idx 0}
        '(branch (label done)))
    ; => {:label->idx {done 5}, :test-passed? true, :idx 5}
[/code]

When `test-passed?` was true, `idx` was set to the value of `done`

## 8: exec

We’ve now implemented all the instructions we need to make our factorial
machine work. Let’s create a function that puts them all together:

[code]

    (defn exec-ins [data ins]
      (let [type->f {'assign exec-assign
                     'test exec-test
                     'branch exec-branch
                     'goto exec-goto}
            f (or (type->f (tag ins))
                  (throw (Exception. "Unexpected instruction")))]
        (f data ins)))
[/code]

Now, we can use this function to `route` to the right instruction:

[code]

    (:registry-map (exec-ins ex-machine-state-v3 '(assign counter (const 5))))
    ; => {n 10, res 1, counter 5}
[/code]

## 9: extract instructions

Oh boy, Okay, we are ready to go…almost!

Now, remember we started out with a language that looks like this:

[code]

    '(
       start
    
       (test (op >) (reg counter) (reg n))
       (branch (label done))
    
       (assign res (op *) (reg counter) (reg res))
       (assign counter (op +) (reg counter) (const 1))
       (goto (label start))
    
       done)
[/code]

But we require `label→idx` mapping. For these `indexes` to make sense, we’ll
also want some representation of _just_ the executable instructions. Let’s
write those:

[code]

    (defn extract-instructions [raw-instructions]
      (vec (remove symbol? raw-instructions)))
    
    (defn extract-label->idx [raw-instructions]
      (second
        (reduce
          (fn [[idx label->idx] part]
            (if (symbol? part)
              [idx (assoc label->idx part idx)]
              [(inc idx) label->idx]))
          [0 {}]
          raw-instructions)))
[/code]

Here’s what our factorial instructions would return:

[code]

    (extract-label->idx factorial-instructions)
    ; => {start 0, done 5}
    (extract-instructions factorial-instructions)
    ; =>
    [(test (op >) (reg counter) (reg n))
     (branch (label done))
     (assign res (op *) (reg counter) (reg res))
     (assign counter (op +) (reg counter) (const 1))
     (goto (label start))]
[/code]

Once we have these…we are ready to put it all together.

## 10: loop

Okay, `exec` can take a machine-state and an instruction, then return a whole
new machine state. `extract-label→idx` can create our `label→idx` mapping, and
`extract-instructions` can provide us with _just_ the executable expressions.

Let’s put it all together:

[code]

    (defn run [registry-map op-map raw-instructions]
      (let [label->idx (extract-label->idx raw-instructions)
            instructions (extract-instructions raw-instructions)
            initial-machine-state {:registry-map registry-map
                                   :op-map op-map
                                   :idx 0
                                   :test-passed? nil
                                   :label->idx label->idx}]
        (loop [machine-state initial-machine-state]
          (if-let [ins (nth instructions (:idx machine-state) nil)]
            (recur (exec-ins machine-state ins))
            machine-state))))
[/code]

We take in a registry, an op-map, and some raw instructions. After that, we
run in a loop, executing the `instruction`, based on the `idx`, and return
when `idx` no longer returns an executable instruction.

Let’s try it out!

[code]

    (get-in
      (run
        {'n 5 'counter 1 'res 1}
        {'* * '> > '+ +}
        factorial-instructions)
      [:registry-map 'res])
    ; => 120
[/code]

…You’ve just made your own machine simulator!

![](https://stopa.io/api/image/firstFrame/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0Lzk1MjUyNjMwLTNhY2FhNDgwLTA3ZWItMTFlYi05MWE5LWMwMDZkZmVhYjZkYy5naWY)

## Fin

Wow, that was a journey. Hope you had fun! 🙂. If you’d like to see the whole
thing, take a look at the [](https://github.com/stopachka/simple-
simulator/blob/main/src/machine_simulator.clj)[github
repo](https://github.com/stopachka/simple-
simulator/blob/main/src/machine_simulator.clj).

Up for a challenge? Try implementing a few other machines: fibonacci
sequences, exponentiation, etc. Try writing the recursive version of these
algorithms: to do that, you’ll need a `stack` construct in our machine-state,
and a `(save <reg-name>)` `(restore <reg-name>)` instruction. After that, heck
you could implement a lisp evaluator!

If this kind of stuff interests you, reach out on twitter or email — am always
happy to chat with like-minded hackers 🙂

* * *

_Thanks to Joe Averbukh, David Magaltadze, Ian Sinnot, Raghavan Lakshmana for
reviewing drafts of this essay._

(1) Computer registers also have an `enabler`, but I decided not to include
that in the essay. I didn’t think it was necessary to grasp the essence. I
plan on writing another essay that would go lot deeper : )

(2) The maximum speed you could probably get on a ball is [~200 km /
hour](https://www.youtube.com/watch?v=cSzwIBeihXA&ab_channel=masamiso), while
light travels 300 000 km… in one second. You can imagine how this kind of
speed can change the game: from making calculating machines impractical to
producing iphones.

