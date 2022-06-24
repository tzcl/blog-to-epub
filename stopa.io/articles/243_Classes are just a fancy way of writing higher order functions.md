# Classes are just a fancy way of writing higher order functions


Joe and I recently [kicked off a re-read of
SICP](https://twitter.com/stopachka/status/1295411936625074178). I can say
that it is _the_ most interesting textbook I have gone through. Imagine, you
begin with just 4 or 5 constructs, and you end up building algebraic equation
solvers, circuit simulators, and even logic programming languages. Because you
start off with such few constructs, the added benefit is that you begin to see
the fundamentally simple, shared essence in programming.

I wanted to give you one example that surprised me in the book. We tend to
think that **classes belong in a** **fundamentally different category** **from
functions.**

But are they so different?

For example, let’s say we have a class like this:

[code]

    class Person { 
      constructor(firstName, lastName) {
        this.fName = firstName; 
        this.lName = lastName;
      }
      getFullName() { 
        return this.fName + ' ' + this.lName;
      }
      setFirstName(firstName) {
        this.fName = firstName;
      }
    }
[/code]

Well, if we think about it, this is really just a higher order function. a
`Person` higher order function accepts arguments (constructor), and returns a
list of functions that can manipulate those arguments (methods). We could
write `Person` like this:

[code]

     function Person(firstName, lastName) {
      let fName = firstName; 
      let lName = lastName;
    
      function getFullName() { 
        return fName + ' ' + lName;
      }
      
      function setFirstName(firstName) { 
        fName = firstName
      }
    
      return function(method) { 
        switch (method) { 
          case 'getFullName': 
            return getFullName;
          case 'setFirstName': 
            return setFirstName;  
        }
      }
    }
[/code]

Now,

[code]

    const person = new Person("Ben", "Bitdiddle")
    person.getFullName()
[/code]

becomes

[code]

    const person = Person("Ben", "Bitdiddle")
    person('getFullName')()
[/code]

Here, instead of invoking a method, we are “passing” a message. This is why by
the way, many classic OO folks talk about object orientation really being
about message passing.

Yup, really. Classes are just higher order functions, which accept arguments
(constructor) and return a list of functions that can manipulate those
arguments (methods).

When you previously thought two concepts were different, but they turn out to
be the same, you’re ripe to discover new ideas: you can find the deeper
abstractions between them, apply ideas from across those seemingly different
categories, and move between concepts more fluidly. So, not only are
epiphanies like this fun, but they’re much more useful than you’d think.

If you liked this, there are a _ton_ of similar epiphanies in the textbook. To
experience it best, I suggest picking a partner and working through the book
together.

 _Thanks to Daniel Woelfel, Alex Reichert, Jacky Wang for reviewing drafts of
this essay_

