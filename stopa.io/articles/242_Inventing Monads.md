# Inventing Monads


I got into a discussion about monads recently. On a search to find some
resources to share, I realized that most essays explained them with type
signatures and rules. A missing ingredient to grok them, I think, is to
understand the intuition behind them. How could you end up _inventing_ monads?

Okay, let’s try to build that intuition. We’ll avoid both types and category
theory.

## Problem

Say you have a few functions to get a user, a profile, and a display picture:

[code]

    function getUser(id) { 
      return USERS[id] 
    }
    
    function getProfile(user) { 
      return user.profile
    }
    
    function getDisplayPicture(profile) { 
      return profile.displayPicture
    }
[/code]

Now, given an id, how would you get the profile picture?

You could write this:

[code]

    getDisplayPicture(getProfile(getUser(id)))
[/code]

Buut, this would throw an error: all these functions _could_ return null. If
`getUser` returned null for example, you would see:

[code]

    Uncaught TypeError: Cannot read property 'profile' of undefined
[/code]

To fix this, you may end up writing something like this:

[code]

    function getDisplayPictureFromId(id) { 
      const user = getUser(id)
      if (!user) return
      const profile = getProfile(user)
      if (!profile) return
      return getDisplayPicture(profile)
    }
[/code]

But, this is getting pretty ugly. All these conditional returns distract from
what you’re really trying to do. **What if there was a way to get rid of these
conditionals?**

## Chainer

So, that’s our challenge: let’s get rid of these conditionals. One way we can
do this, is to make some kind of helper. This helper would let us chain these
functions together:

[code]

    new Chainer(getUser(id))
      .whenExists(user => getProfile(user))
      .whenExists(profile => getDisplayPicture(profile))
[/code]

This looks pretty good. Let’s implement it.

### whenExists

`.whenExists` would only run the callback if the value exists. Here’s how you
could write this:

[code]

    class Chainer {
      constructor(v) { 
          this.value = v
      }
      whenExists(f) { 
          if (!this.value) return this;
          return new Chainer(f(this.value))
      }
    }
[/code]

And voila, with just this, we can now write

[code]

    function getProfilePictureFromId(id) { 
      return new Chainer(getUser(id))
        .whenExists(user => getProfile(user))
        .whenExists(profile => getDisplayPicture(profile))
    }
[/code]

### More Problems

Notice that `getDisplayPictureFromId` now returns a `Chainer`.

Imagine we had another function `resizeDisplayPicture`, that _also_ returned a
Chainer

[code]

    function resizeDisplayPicture(pic) { 
        return new Chainer(pic).whenExists(pic => ...
    }
[/code]

What would happen, if we wrote:

[code]

    getProfilePictureFromId(id).whenExists(pic => resizeDisplayPicture(pic))
[/code]

Let’s look at whenExists again:

[code]

    whenExists(f) { 
      if (!this.value) return this;
      return new Chainer(f(this.value))
    }
[/code]

If `getProfilePictureFromId(id)` did exist, we would run

[code]

    new Chainer(f(this.value))
[/code]

which in this case is

[code]

    new Chainer(resizeDisplayPicture(this.value)) 
[/code]

Which becomes

[code]

    new Chainer(new Chainer(this.value)...
[/code]

 **Uh oh. We now have a Chainer inside of a Chainer.** Ideally, we’d want a
function that somehow “merged” these chainers together.

### whenExistsMerge

So let’s do that. We can call it `whenExistsMerge`

[code]

    class Chainer {
      constructor(v) { 
          this.value = v
      }
      whenExists(f) { 
          if (!this.value) return this;
          return new Chainer(f(this.value))
      }
      whenExistsMerge(f) { 
          if (!this.value) return this;
          return f(this.value)
      }
    }
[/code]

And with that, we can write

[code]

    getProfilePictureFromId(id)
      .whenExistsMerge(pic => resizeDisplayPicture(pic))
      .whenExists(resizedPic => ...)
[/code]

## Eureka

 **Aand voila, you’ve just invented a specific type of monad.** Kind of (1).
Chainer is analogous to the `Maybe` monad. `whenExists` is analogous to its
`fmap` operation, and `whenExistsMerge` is analogous to its `bind` operation.
If you’re curious about the type-based technicalities now, [see this
essay](http://adit.io/posts/2013-04-17-functors,_applicatives,_and_monads_in_pictures.html).

## More uses

So, now we’ve found this cool `Chainer`. We can stop here, or think a bit
further. What’s so special about it?

Well, it’s like a box that wraps around some information. We can interact with
that box with `whenExists` and `whenExistsMerge`.

How else can we use the idea of `box` and `whenExists?`

Here’s one. Let’s say you were dealing with callback hell:

[code]

    fetchUser(id, (err, user) => {
      if (err) ... 
        fetchProfile(profile, (err, profile) => { 
          if (err) ...
            fetchDisplayPicture(...
        }
    }
[/code]

What if we created something like an `Async Chainer`: it stores the result of
some future computation. Then, you could use the `whenExists*` functions,
which let you interact with the value _when_ it is computed. We turn the
callback hell into

[code]

     fetchUser(id).whenExistsMerge(fetchProfile).whenExistsMerge(fetchDisplayPicture)
[/code]

Well, replace `whenExistsMerge` with `then`, and you're on a road to discover
`Promise`, which is also a monad. Kind of (2).

## Abstract all the way

Now, it’s pretty cool to notice that both the nullable use case and the async
use case have the same interface. The name `whenExists` may be a bit too
specific. Really, what it does is give you an interface to `map` over the
value. If you use the word `map`, `whenExistsMerge` really lets you `flatMap`
over the value.

This begins to get us to the fundamental abstraction of a monad: a box, with
an interface for `map`, and `flatMap`. As you look deeper, you’ll notice that
this abstraction can handle a lot of other things. If you’re curious, research
the `Result` monad for example.

## Fin

And with that, you’ve invented monads : )

### Aside: Do you _really_ need this?

As you went through this, you may have realized that there are other ways to
solve the problems that monads solve. Instead of `Chainer`, your language
could have a [safe call](https://kotlinlang.org/docs/reference/null-
safety.html#safe-calls) abstraction. Instead of `Promise`, your language could
have an `async/await` abstraction. Sometimes those can be a better [better
choice](https://www.youtube.com/watch?v=YR5WdGrpoug). Nevertheless, if your
language doesn’t have those abstractions, you can use monads to solve them.
And of course, like any powerful abstraction, you can invent new monads to
simplify your business logic.

* * *

(1) I cheated a bit with `Chainer`, by avoiding the subtypes `Just` and
`Nothing`. This makes it so you can’t express something like `Just(null)`.
Still, it gets at the essence : )

(2) Likewise, `Promise` isn’t quite a monad, because it mixes both `flatMap`
and `map` with `then`. This makes it so you can’t have a
`Promise<Promise<Res>>`. Again though, it gets at the essence

 _Thanks to Joe Averbukh, Mark Shlick, Daniel Woelfel, Irakli Safareli, Jacky
Wang for reviewing drafts of this essay_

