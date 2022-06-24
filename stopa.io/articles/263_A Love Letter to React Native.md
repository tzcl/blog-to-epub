# A Love Letter to React Native


Since its inception, I scowled skeptically at React Native. I thought it was
yet-another magical framework that promised to boil the ocean for you. All I
needed was a tolerating ear, and I’d set off: “With these magical frameworks,
you end up with tarpits”:

The first tarpit, was the tarpit of the “golden path”. Things are smooth when
you’re building a todo app, but what about when you need do something special?
Suddenly you find yourself sludging through poorly created abstractions,
debugging some object-oriented reaction between React Native and iOS/Android
text inputs, cursing your past self for putting you on this path.

The second tarpit, was the tarpit of “a thousand papercuts”. You’d accrue a
slew of small bugs: flickery modals, slow loading times, and weird input
behavior. Invariably you realize that the app just “doesn’t feel native” _—_ a
euphemism for “it sucks”. You may have to chuck the whole thing, with the eyes
of your teammates who trusted and respected you burning through your soul.

This was the state of my thoughts for years. But like the river cutting
through rock, time cut through my ideas.

### Dipping our toes in Mobile

The first erosion came when I viscerally experienced just how painful mobile
development could be. To adopt one of Paul Graham’s metaphors: we web
engineers are like folks in rich countries, who have no idea what goes on in
the favellas of mobile development.

Imagine minute-long build times even for simple apps. Just this can unnerve a
web developer. But imagine further, that all of those builds are happening on
brittle infrastructure, where you’re bound to come across a random transient
issue every day [1].

And all that pain feels like an inconvenient itch, when you compare it to the
the deployment story. Imagine that to push a bugfix, people who _don’t work at
your company_ and _have no sense of urgency for you_ , decide what you can
ship. App broken for half your users? “We’ll get back to you”. Ask for an
“expedited review” and hope for the best.

We dipped our toes in native development a year ago with a simple app [2].
Yes, Swift’s functional reactive programming and sum types were a joy. But the
build times and the back-and-forths with App Review were painful enough, that
we told ourselves for any new app we built, we’d do all that we could to stay
on web. There was just no way to iterate quickly enough on mobile.

### PWAs

This was why, when we first built Consistent [3], it was PWA first. The app
certainly “didn’t feel native” — but at least we could ship a change whenever
we wanted.

This state of things went on for a month or so, but we couldn’t ignore the
reality of native UX. Any self-respecting fitness app should be able to sync
data with HealthKit and Google Fit — how the heck would do that without
Native? And what about notifications?

The stack of feature ideas piled up until we were forced to consider Native
again.

### Discord

Wanting to make our app great, remembering the pain of mobile development, and
considering the inonvenience of having to write both iOS and Andorid weighed
on my mind.

During one reflection I remembered something: wait, Discord was built on React
Native.

It’s no todo app. Thousands of users hang around in channels, send their
emojis, and it all _feels native._ The most painful worry for me was the
tarpit of a “thousand papercuts”, forcing me to chuck a whole app. But it
looked like Discord hadn’t hit this tarpit. What if I was wrong?

I forked up a fresh React Native app, and began to experiment with Consistent
on mobile.

### Hot Reloading

The first breath of fresh air came with React Native’s development experience.
Seeing a change on mobile come alive within a blink, felt so good that I
couldn’t help but tell people about it. My parents, who live in a village in
Eastern Europe heard the shpiel. At parties in New York, I would nudge
conversation away from techno music and onto iterative development.

With just hot reloading, you get back the experience of of coding by discovery
and exploration, and this can change your engineering velocity by a magnitude.

### Code Push

It got better. Both iOS and Android allow you to ship changes to interpreted
languages (that means Javascript) without any review process. This means that
you can ship updates to your React Native app instantly!

You get back ownership for your deploys. I can still viscerally remember the
feeling I had when our app was insta-crashing, but I knew we could be saved
with Code Push.

When you _know_ you can fix a bug instantly, you both program more
aggressively and sleep better at night — and that too changes your engineering
velocity.

### Two Platforms

And to my astonishment, it _actually_ delivered the promise of single codebase
shipping across platforms. I didn’t believe this would be possible. I imagined
a hodgepodge of edge cases would divide the app, officially stamped as “cross-
platform”, in the same way that the Soviet Union’s newspaper was called
“Pravda”.

The primitives just work well across platforms. After 3 months of app
development, I searched our codebase, to see we only have 5 if statements,
which check specifically for the platform the app is running on.

I think it’s inarguable to say that being able to ship seamlessly on two
platforms at least halves your engineering time. But, I think it’s a bigger
win than that. If a single engineer gets to work on both platforms, they only
need to gain context once. There’s fewer changes of errors, and the app is
more consistent to boot.

### A Fundamental Abstraction

But, what about that abstraction cost? Would we find ourselves having to debug
esoteric object-oriented issues with text inputs?

Well, I’d argue that with hot reloading, code push, and cross-platform
support, you’d have to debug years of esotertic bugs to pay down the win. But,
the risk for catastrophe is lower in React Native.

I dug deeper into how it worked, and I was astounded. It was beautiful.

Their concepts are fundamental: just two threads, with React figuring out what
to do, and sending those instructions over a Native bridge. You can build
their layout engine yourself.

It made me realize that this was no framework, but a fundamental abstraction:
more similar to an interpreter than an MVC framework.

### An Interpreter for UI

And if an abstraction is like an interpreter, you get some serious wins.

When the abstraction is conceptually simple, you need fewer people to maintain
it. For example, just a few folks tend to maintain powerful programming
languages. Similarly, React Native is conceptually simple enough that if
Facebook were to dump the whole project, I’m confident a few folks could
maintain it.

A powerful abstraction pushes complexity down. Just a few hundred lines of an
interpereter can run hundreds of thousands of lines of programs. Similarily,
hunderds of thousands of lines of UI gets handled by React Native’s platform.
This means that when you come across an issue, you can solve it at a platform
level: instead of your product engineers worrying about performance for
example, a few platform engineers can worry and solve it for everyone.

My experience at Facebook showed me constantly the benefit of pushing
complexity down in this way. For example, we did this for privacy. Facebook
had a slew of issues for “which user can see what data”. Product engineers had
to constantly worry about this when writing UI.

To solve this, some FB engineers built “ViewerContexts”. These handy things
made it impossible to fetch data a viewer wasn’t allowed to see. All the
complexity for privacy was pushed down to this new abstraction, and product
engineers didn’t have to worry about it. You get to do this for hard problems
in your UI development.

### A Grand Tradition

We’re inundated with astronaut frameworks: projects that promise to change the
way we think about programming and make life a leasiurely stroll in a flower
garden, but fail after you get past a todo app.

This means we’re right to be wary when we hear big promises: after all a
fundamental abstraction in how we program is less likely to come up, compared
to a loudly touted astronaut framework.

Yet, fundamental abstractions _do_ come around. We’re not writing in assembly,
or worrying about TCP after all. We work on abstraction-over-abstraction-over-
abstraction all day long.

Each abstraciton can help us move a mangitude faster, so you can imagine the
opportunity ahead i you can spot one. I think React has proven to be an
instance of such an abstraction. You can tell by how conceptually simple the
fundamental ideas are, and how it redefines the way you solve problems. React
Native builds beautifully on top of it.

We’re 3 months into our product at this point. Have we found estoteric issues?
Yes. Many an hour I have spent learning about the intricate relationship
between ScrollViews, KeyboardAvodingViews, and TextInputs. But, was it worth
it? The development speed, and the core concepts we get to use have changed
how we develop applications on mobile. We’re betting our product on it.

### Two caveats

I would heartily recommend React Native at this point, but would make two
suggestion.

First: _do not be afraid of native._ If you can, build a purely Native app on
iOS and Android to learn. In order to move quickly, I believe you need to
understand at least one level below the abstraction that you use. Time will
come when indeed you must go outside of React Native — whether it’s because no
library does the right job, or you need to move off some work from Native. If
you know iOS and Android, you’ll be fearless about it.

Second: _embrace delightful UX._ Mobile apps are a gold standard for
delightful user experience. It’s a different paradigm and if you’re coming
purely from web, there’s a lot to learn. Discord has proven that you can make
a delightful app on React Native, but it won’t happen by accident. Things that
you may have not even gotten to on web — like animations — you’ll want to
prioritize highly on mobile. Alex Koliarskyi has a great talk [4] on this.

With those two caveats, you’re off to the races.

 _Thanks Alex Kotliarskyi, Daniel Woelfel, Jacky Wang, Joe Averbukh, Phil
Nachum, Sean Grove for reviewing drafts of this essay_

