# Crafting Functions


We write so many functions in our programs that they become second nature
before we know it. Like ants in a colony, they are numerous beyond imagination
and they come together to form some surprisingly complex systems.

It begs the question: how do we write good functions? It can seem trivial:
they’re just like ants after-all. But there is leverage in the answer: the
right decisions multiply throughout your codebase and bubble up into great
design.

I think there are about three key ideas you can employ to craft good
functions. I wanted to share them with you.

## Export

Let’s start with an example. We have an app, and we want to export some data
in a JSON format. Here’s what a function for that could look like:

[code]

    function exportFile() { 
      setLoading(true);
      try {
        const data = getData(); // [Data, Data, Data]
        const exportableData = toExportableData(data); // ExportableData
        const jsonStr = JSON.stringify(exportableData); // '{"data": {...
        const fileURL = saveFile("export.json", jsonStr); // https://foo.com/export.json
        setFileURL(fileURL);
      } finally {
        setLoading(false)
      }
    }
[/code]

Seems straight forward: To export as JSON, we first get our data. Now, this
data may have some sensitive info, so we clean that up and transform into
something exportable; ExportableData. Once we have that, we get a string
representation, save the file, and badabing, badaboom, we’re done.

Okay, we’ve got something working well.

## A new requirement

But life moves on and our program needs to evolve. Instead of just exporting
JSON, we need to do more: **we also need to export a CSV file**.

How do we do that?

The first thing we notice, is that exporting a CSV is very similar to
exporting JSON. Can we abstract `exportFile`?

## Idea 1: Configuration

One thing we can do, is to introduce a new flag: something like
`exportFile(/*isCSV=*/ true)`

[code]

    function exportFile(isCSV) { 
      ...
      let fileURL
      if (isCSV) { 
        const csvStr = toCSVStr(exportableData)
        fileURL = saveFile("export.csv", csvStr);
      } else { 
        const jsonStr = JSON.stringify(exportableData);
        fileURL = saveFile("export.json", jsonStr);
      }
      ...
[/code]

By introducing this flag, we can conditionally produce a different `fileURL`:
one for CSV and one for JSON. With that we see the first concept for
abstraction: configuration. You pass some configuration, and you leave it to
your function to figure what to do.

So, is it a good idea?

### The key _advantage_ is that our logic is centralized.

With configuration, the caller is limited in what they can do: they can only
provide flags. All the true logic stays inside `exportFile`. This means that
callers of the function can’t go crazy and do something unsupported. And that
could give us some peace of mind.

### The key _disadvantage_ is that…our logic is centralized.

This will work, but let’s think about it. First, notice that in order to
understand `exportFile` now, we need to understand both the CSV and JSON case.
Imagine if someone opens up `exportFile` to figure out what it does: if they
_only_ cared about JSON, they now have to understand more logic than they
needed. Anyone who changes the logic for CSV, may also end up breaking JSON.
**`exportFile`** **has become**
[**complected**](https://www.infoq.com/presentations/Simple-Made-Easy/) **.**

Notice also, that because the caller of this function can _only_ provide
flags, their hands are tied for use-cases that you didn’t support. This was
supposed to give you peace of mind, but it certainly can frustrate callers.
imagine if they wanted to support XML, what could they do? They’d have to edit
`exportFile` to support this case. (God forbid they edit it to be something
like `exportFile(isCSV, isXML)` — now you have invariant conditions on your
hands). By being so specific, you’ve chosen to make your function less
abstract — this of course means that it is less powerful. **`exportFile`**
**has become hard to extend**

### For better or worse, configuration gives the caller the least amount of
power

If you imagine a sort power spectrum, where the caller has the least power on
the left, and most power on the right, configuration would be on the left. You
control what the caller does so tightly that it gives your certainty, but
makes your function more complex and less useful.

Say you wanted to address the problems, and move to the right of this
spectrum, what could you do?

## Idea 2: Inversion

Well, if you look at what we wrote, we can notice that the only part that is
_really_ different, is the bit about taking `exportData`, and creating a
`fileURL`.

[code]

    ...
    const exportableData = toExportableData(data); // ExportableData
    ... // *This can be different! Somehow we need to get a fileURL* 
    setFileURL(fileURL);
    ...
[/code]

So one thing we can do is this: instead of providing a flag, we can provide a
function:

[code]

    function exportFile(exportableDataToFileURL) { 
      setLoading(true);
      try {
        const data = getData(); // [Data, Data, Data]
        const exportableData = toExportableData(data); // ExportableData
        const fileURL = exportableDataToFileURL(exportableData)
        setFileURL(fileURL);
      } finally {
        setLoading(false)
      }
    }
[/code]

Now, for JSON, we can write

[code]

    exportFile((exportableData) => { 
      return saveFile("export.json", JSON.stringify(exportableData));
    })
[/code]

and for CSV we can write:

[code]

    exportFile((exportableData) => { 
      return saveFile("export.csv", toCSVStr(exportableData));
    })
[/code]

Oky doke, this is cool.

### The key _advantage_ is that you give the caller more power

With this we solve both of the problems we had with configuration. Now if
someone looks under the hood at `exportFile`, they won’t see unrelated code
about csv. If they wanted to extend to XML, they can simply provide a
different function. We’ve given the caller much more power

### The key _disadvantage_ is that it can be either too powerful or not
powerful enough

We’ve abstracted further, but there is a price there. The first is, that we
_think_ we know that what we _really_ need to pass outwards is
`exportableData`, and what we need to return is a `fileURL`. What if we were
wrong? For example, some may need a slightly different data format — instead
of `exportableData` they need `someOtherKindOfExportableData`. By the time we
figured that out, it’s possible that there are numerous new usages of
`exportFile`, which we’ll have to support as we evolve this function.

One way we could have prevented this, is to have stuck with configuration.
This way, anyone who wanted to support something would have to funnel through
this function, which would give us time to think about what the best
abstraction was.

Another way, would have been if this function was abstracted even further, so
callers could have easily supported `someOtherKindOfExportableData`.

### Inversion lies in the middle of the power spectrum

Inversion is more powerful than configuration, but it’s not the most powerful
method. This can be a great choice, but you risk either being too powerful and
exposing errors, or not being powerful enough and restricting callers.

We know the less powerful option: configuration. What would the most powerful
one look like?

## Idea 3: Composition

The next thing we may notice, is that our `exportFile` function is actually
built up some building blocks that could be useful for a bunch of different
things. For example, many functions may want a loading state, or just need to
get `exportableData`, etc. We could create those building blocks:

[code]

    function exportJSONFile() { 
      withLoading(() => saveJSONFile(getExportableData()))
    }
    
    
    function exportCSVFile() { 
      withLoading(() => saveCSVFile(getExportableData()))
    }
[/code]

### The key advantage is that the user gets the most power

The building blocks that we just built, can be used in a myriad of ways. The
user can support CSV, XML, can use `isLoading` with some other function, and
choose to provide a different kind of `exportableData`. We’ve provided a lot
of power for the user.

### The key disadvantage is that you are the most vulnerable to mistakes

The disadvantage though, like in the case of inversion, is that we open
ourselves up to a lot of mistakes. What if `isLoading` was really meant for
files, and other things should have been using a different flag? What if
people start using `saveJSONFile`, and pass data that wasn’t really an export?
These are all cases that we have implicitly allowed with our abstractions.

There’s a further problem: notice that with our first example of `exportFile`,
you the code was more concrete: you could see what was actually happening.
When code is more abstract, it’s a bit harder to reason about what is
_actually_ happening. Now, it can be worth it for the power gains, but if you
optimized prematurely, you’re just paying this price for nothing. An example
of this unnecessary price is `saveJSONFile` and `saveCSVFile` — if we had
[inlined](http://number-none.com/blow/john_carmack_on_inlined_code.html)
those, the overall composition would still be abstract but more
understandable. These are the kind of things to watch out for as you abstract
at this level.

### Composition is at the end of the spectrum

And with that, we see that composition gives us the most power, but gives us
the most opportunities to shoot ourselves in the foot. Boy can it be worth it
though.

## Continuum

It’s funny to notice that with each option, the pro _is_ the con. So how do we
pick? I think one heuristic you can use is this: pick the most powerful option
you can limited by your confidence. For example, if you have a light
understanding of the problem, stay on the lower side of the abstraction
spectrum. As you understand more (say, time to introduce XML) you can evolve
to the powerful side of the spectrum. When you’re _very_ confident, and you
can see good use-cases for your building blocks, lean to the most powerful
side of the spectrum.

_Thanks to Daniel Woelfel, Alex Reichert, Julien Odent for reviewing drafts of
this essay_

