# Founder Diaries: The First 2 Months of Consistent


 _Note: we are close to finishing up our initial cohort
of[consistent](https://consistent.fit)! I wanted to take stock of what’s done,
and this essay resulted. Hopefully it (a) gives a sense of how startups are
like at the very early stages, and (b) is entertaining to read for ya 🙂._

Consistent was born in early June.

### Zeneca Days

Previously we were working on [Zeneca](https://zeneca.io), a better Goodreads.
Within a month we hit a thousand users, and did a bunch of fun stuff with
Clojure. This felt great, but very soon we were awakened to one the most
important startup lessons: you gotta look at the _right_ metrics. Sure, number
of users were nice, but what about weekly active users? If weekly active users
weren’t high, it would mean (for our case) that what we were doing wasn’t
valuable. And if the number wasn’t growing, it would mean we were _losing_
users.

Alas, our weekly active users number was not growing. The problem we solved —
creating beautiful [lists](https://zeneca.io/joe) for books — was _nice_ but
not _gripping_ need for users. We iterated, but didn’t find a specific hit.
Eventually, we took stock and realized that this space wasn’t what we’d want
to fight for over the next 10 years. The decision was tough but after a good
week of reflection, we did it. The product was in a stable place, so we kept
it running and moved on.

### The Walk

Back to the drawing board. This time, we wanted to work on a _hair-on-fire_
kind of problem for users. To come up with ideas, Joe was reading Data
Intensive Applications, and I was mulling over problems with
[databases.](https://stopa.io/post/279) And of course, we did what every
startup founder would do: religiously read Paul Graham essays over and over.

One day, on the nth re-read of one of PG’s [ideas
essays](http://www.paulgraham.com/startupideas.html), a question stood out:
“What’s unusual about you”. If you’re unusual in some way, and more people
will be that way in the future, it’s fruitful ground for new ideas.

I went on a walk to reflect, and sure enough an idea struck: “Wait, for years
I’ve spent close to thousand dollars a month on fitness...that can’t be
normal.”

The more I unraveled that thread, the more excited I became. Joe had the same
kind of unnatural dedication to fitness — he logged for years and built a
whole suite of [tools](https://joelogs.com). Since we were both in high
school, we had a bucket-list item to have six-pack abs, and gosh darn it we
would get em.

Why were we paying so much, and why were we spending so much time? It’s
because though fitness was in a sense simple (in that increasing stressors
helps you grow, and it’s ultimately guaranteed to be achievable), it was
elusively difficult (in that your body is reflexive, you’re likely to plateau,
and need to get multiple things right for enough of a time to see results.)

To achieve our goals, we had built a system where a personal trainer would
guide our workout progressions and nutritional goals, and we had tools we
hacked together to build visibility for how we were doing. It was expensive
and filled with schleps, but it was getting us better and better results. In
one view, we were paying a sort of tax to live in the future.

I thought to myself, “what would a magical experience look like?”. I imagined
an app that could take you from where you were, and guide you into the best
shape of your life. It would bring together all the disparate information you
need to know, alongside tools that gave you visibility and guidance.

I knew there was nothing like this today. Apps were fragmented and went
nowhere near what it took to achieve results. Even with hiring a personal
trainer and a dietician, you still had to do personal research, and would
likely use crappy tech. Could we create this magical experience? An app that
gets you into the best shape of your life… It became clearer to me that this
was where the world was headed.

### Things that don’t scale

So, we had a guiding light — there was opportunity to innovate in Fitness. How
do we start?

The closest-at-hand solution was to start small and build some sort of app.
Perhaps we could start with a fasting or workout app for example, and expand
from there.

The downside on this path, was that it was unlikely to produce a truly
differentiated product. There are a lot of options, and by definition a subset
solution can’t produce grand changes. We feared that users would only mildly
like it. That would mean that they wouldn’t be as engaged, which would make
both acquisition and learning harder. We’d be doing Zeneca all over again.

Another option was to go all-in on a machine-learning based solution. There
were some subsets that could be tackled: generating workout plans, calorie
detection, nutritional guide generation. I had spent 4 years working in the ML
space (though as an engineer, not a researcher) and had a carpenter’s sense of
what was possible. I didn’t think you could reach the kind of experience a
personal trainer could deliver, but I did think there was ripe opportunity to
build exceptional tools.

The big problem with the ML direction, was that it would take a long time to
experiment and launch a truly differentiating product, and it presupposed
fitness expertise. We were enthusiasts in fitness, but we were not yet experts
(we didn’t even have six-packs yet! [1]). It would take us too long to build
up the knowledge of users we needed to create a winning product by following
this path.

So, then, we considered one more approach: what if we just started a cohort,
and tried to deliver this magical experience to them? By going this route,
we’d get a deep sense of how it was like to coach others, and exactly what was
needed to help people succeed. We would _really_ be able to work towards a
compelling result, and from day one, we would be delivering a product that was
truly exceptional. From there, with highly engaged users, we could iterate
towards more and more scaled solutions.

At Facebook I helped build M, a personal assistant that could answer any
question. We did this by augmenting human support agents. Though we had
trouble automating when the tasks were too varied, we got good in verticals:
from restaurant orders to appointments to event hosting. It was a bet, but I
thought that it _could_ be possible to scale an experience that felt like
support from a personal trainer and a dietician. In the best case we could
build the magical experience at scale, but even if that didn’t work, we’d have
such engaged users, that we could extract out products that solve subset
problems 10X better.

### The launch

So, we followed the last approach. We popped up a landing page, and launched a
free cohort on [Hacker news](https://news.ycombinator.com/item?id=27594133).
From there we got about 200 emails, and selected 20 people to join the group.

Initially, we did this all over Slack and Google Sheets. The structure looked
like this:

The user would send us their weight every day on Slack. This was an easy task
that could serve as a touchpoint. They would log their food on MyFitnessPal
every day. They would add us as friends, which would allow us to see their
diaries. Next, at the end of every week they would send a progress photo, as
well as a reflection of how the week went. Each week, would layer on new goals
that would help them get to a six-pack. From logging to setting macro goals,
to tuning their movement, we’d layer changes to help them reach a six-pack.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzEzMTAwNTY4NS0zNjhlY2FlNS1hOGY3LTQwMjMtYmEzNy1hNTc0NTg0MWQ5MDgucG5n)

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzEzMTAwNTcyMS0wZGUyZGE3Ni1jNTBhLTQ4YWUtOGJjNC1jZjdjMmE5MjljNzIucG5n)

### The Initial Pain

For the first week and half or so, the pain in the business was acute. We
would manually ping each person a reminder about their weight, had to look
over their MyFitnessPal diaries, and make sure nothing was amiss. I personally
find it very hard to do “manual tasks” for myself (laundry, taking out the
trash, etc has been a perennial problem for me), so this felt especially
painful. On a particularly dreary day, I would find myself daydreaming and
comparing this to working on a database, writing, or programming in
Clojure…oof.

Thankfully, Joe’s spirit was high, and he took some slack off of me, which
gave me the space to find resolve. At the end of the day, we knew that we had
to do these schleps to really feel the pain and understand what our users
wanted. It’s so easy to read all these essays about “doing schleps” and think
to yourself “yeah, I can do that” — turns out it’s much harder in practice.

### Rafael

Very soon after, we started to move off the Google Sheet and began to build
tools that helped us do these manual tasks. A slack bot would automatically
log weight, progress pictures, and reviews. We also built a quick cron job
that woulds scape everyone’s MyFitnessPal and plop it into our database. This
allowed us to automatically detect problems (missing days, too high / too low
calories), and create analytics tools to more quickly figure out how each user
was doing. This decreased our maintenance load from at least a few hours of
work each day, to 1 day a week. For that one day, the majority of the time was
spent going through each user to build up a weekly review for them. The
reminders about weight, diary logging, and the rest were no longer necessary!

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzEzMTAwNTc1Ni0xODdhMmJmZi00NmY1LTQyZjUtYTcyOS01ZTRlYmY3NzU4MDIucG5n)

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzEzMTAwNTc3NS1jYzBhODMyNy1kNWY2LTQwNWQtOTMyNC03ZTliNDM0MjExNTUucG5n)

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzEzMTAwNTc5Mi1mODAwYWQ0YS0xNGNhLTRiMmYtYjY1MC1jMGUyZTE0YjUzMjAucG5n)

### The Content

As our manual tasks decreased into one day, Joe and I were able to dedicate
time to ramping up coaching literature. Joe went through all of Noom’s course,
as a sort of competitive analysis. I finished the “[certification
textbook](https://twitter.com/stopachka)” Equinox trainers use to become
nutritional coaches. From there and from what we had learned with issues users
had, we built up content to help make progress and overcome plateaus.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzEzMTAwNTgyMC04ZWU4Mzg4ZC0wYTEyLTQxMWUtOWUxOC0zZjc2ODMzNDI5ZDMucG5n)

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzEzMTAwNTgzMC02YzAwZmY1Mi0zMGI5LTRhMDMtYmYwMy0xNDA5ZmNjODE5M2YucG5n)

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzEzMTAwNTg1My0zMmQyZDIxYS00OGZkLTQzODktOWViMC0yY2M0MmFkYjY5ZTgucG5n)

### The App

As users made progress, we began to look at the next big win we could offer
them. We noticed that the most difficult bit was putting all the data
together, to offer insight for change. We thought, what if we made a _really_
nice UX to help you see how you’re doing?

So, we started hacking together an app. Last week, we launched its first
screen — a page that shows you how your week is progressing. This week, we’re
working on the “Report” tab — a view which will help us write about ~70% of
the content we already write for weekly reviews.

There’s so much more to do. As we go further, we’re realizing the need in
integrating sleep and stress, and are constantly relying on a slew of
different apps to get things done. What if it was all well-integrated?

_Note: (the reports tab, second video, currently has partially stubbed data)_

### Feedback so far

One month in, we ran a survey, and received about 16 responses. Following the
[Superhuman PMF test](https://review.firstround.com/how-superhuman-built-an-
engine-to-find-product-market-fit), we asked them how disappointed they would
be if Consistent was no longer.

![image](https://stopa.io/api/image/aHR0cHM6Ly91c2VyLWltYWdlcy5naXRodWJ1c2VyY29udGVudC5jb20vOTg0NTc0LzEzMTAwNTg5My1jNjZjODA5Ny04OTE5LTRlY2UtOTAwZC0yYmZjNmQ3ZDMwYjcucG5n)

43% (7 people) answered “very disappointed”. The answers noted how happy they
were to discover the structure they needed to be accountable, as well as the
guidance and feedback we provided for them to iterate every week. Some
favorite quotes:

> I feel it's improving both my body and also my outlook on life. Whilst the
> end goal is a six pack, the steps look to be making me a healthier and more
> well rounded individual.
>
> I’ve hit an all time low after I started with consistent. I think having a
> check in has kept me accountable about my food choices, and it helps me
> bounce back when those choices aren’t so hot.
>
> I love the motivation to actually consistently (hah) work out and eat right.
> It’s been a total game changer for my personal fitness to be a part of a
> group with similar goals and I love it.
>
> It's the first time I feel I'm making progress towards consciously losing
> weight. Not a lot of tech, but the community + accountability + guidance
> based on data has been game changer.

For those who were “somewhat” disappointed (5), the main feedback was that
though Consistent helped them go faster, they had learned the important bits
now, and felt that they had enough self-belief that they would not be crushed
if we were no longer around, and could continue on their journey:

> I love that consistent has helped me get consistent. But from here, I’m
> getting more value from MFP and the habits I’ve built than the group. I no
> longer need the accountability to keep me on track.
>
> What can I say? Before Consistent, I was 7 lbs heavier.
>
> Could I have done it without y'all? Maybe. But I don't think I'd have
> progressed as aggressively without the motivation and accountability.

For the “not disappointed” group (4), 2 of them misunderstood the question.
They knew that since this was a 3 month program, it would end, and were
thinking that we asked how they would feel once it ended. The message was
similar to the “somewhat” group, in that they would be happy because they
learned a lot:

> I think I’ve learned so much in a way that I have a lot knowledge of how to
> track my health, nutrition intake… etc. therefore, I would not be
> disappointed (in a good way) if I no longer user Consistent in a way that I
> think I might be able to handle it myself. Consistent helped my to get to
> this point.
>
> I like the tracking, the feedback and the community, but I feel that the
> mission statement was to reach a milestone, and so I’ll be happy to
> celebrate with the cohort once the time comes, but in a good way - not
> heartbroken because this was what consistent proposed in the first place.

For the remaining two, the main criticism was that they already had a system,
and didn’t believe that the coaching / content was necessary for them. We also
“force” a bit of a schelp on users: they need to submit their weight manually
each day. This schlep was a bit too much for some, since they have smart
scales:

> I feel I also had gotten into a good habit of tracking before this, so it
> felt like added overhead.
>
> This includes having to double track exercises and slack weight / body fat
> when it's something that's been syncing with my health app for example.
>
> Before Consistent I was quite aware of my weight progression (daily weight),
> some nutrition guidelines and I was doing different exercises (but moving
> already). Consistent added the need to do food logging (that I don't
> particularly like) and didn't gave me any other guideline on how to move
> better.

### Integrating Feedback

Users have lost an average of 4LB over the last month. It’s been surprising
and inspiring to see the kind of changes folks have made: from sedentary life
filled with processed foods to daily movement, hitting 30% protein goals.

The 43% “very disappointed”, excites us. It feels like we are onto something.
From here, and observing the 2 “not disappointed”, openness to change is
crucial for the program. Folks who are open to try new things, and are
determined enough to earnestly give difficult changes a shot have shown
exceptional results.

In the “somewhat disappointed” camp, in some way I am happy that the structure
is valuable. I do think that a person can achieve quite a bit with logging
daily, doing a weekly review, and taking weekly progress pictures. I do think
though that after about a month or so of progress, the body gets used to the
deficit and exercise load, and will tend to plateau. To get through it, they
may need more coaching. I think this is where some of Consistent’s secret
sauce will come in especially useful.

For the “not disappointed” camp, though coachability is a factor, I do think
reducing schelps is going to be helpful. We are conflicted about the shlep of
logging weight, as counterintuitively it’s a very easy way to be “present”
about your progress, and have a touchpoint. We are considering other ways to
achieve this, perhaps with a daily report.

### Next Steps

Priority 1 is to lead the cohort to a successful outcome. In that process,
we’d like to continue to improve our weekly review efficiency, improve the
app, and produce more content.

Priority 2, is to set up a second cohort of 50 people, and begin to charge. 50
is a sufficiently challenging scale for us at this point, and could continue
help us refine the program. If we charge 200 dollars a month, I think it’ll be
sufficient to prove out the value, and select for the kind of customers we’d
like to have. I think we could charge more, but at 100 dollars a month, it’s
more of a no-brainer. To do this, we’ll start by writing content, (Joe is
working on “365 days of logging”, and “Experiments in Nicecream” as we speak),
and reaching out to our extended networks.

We’re also deciding if we should be making the program a “4 month” cohort, or
a community. One thing we realize, is that 4 months is indeed aggressive to
achieve “clearly defined six packs”, though it’s long enough to reach real
transformation. If they continued on, they could keep growing. We personally
also experienced how nice it is to continue working with a coach — I worked
with my personal trainer for 4 years.

### Even further ahead

As the 50-person cohort moves through, we intend to start creating an iPhone
app.

Currently, much of our engagement happens over MyFitnessPal and Slack. Though
this is great for moving fast, we want to start to gain much finer control
over these surfaces. We’d be able to iterate on that UX create a more and more
magical experience.

Towards the end of that, there’ll be an inflection point, where we’ll need to
decide if we want to start scaling as a “Noom-like” app, or a “Lambda-school”
like app. This still requires more thinking — if you have any thoughts we
definitely would to hear it!

### Painful Problems

From a startup perspective, by far the most important lesson we learned, is
the value of solving a _very painful_ problem for people.

On Zeneca it was hard to see daily usage. On this one, you can’t help but see
it. The critical nature of the problem is also motivating: there were times
when it was tough to do the schelp work, but we reminded ourselves, “hey, our
users are counting on us.” It’s not a formula for every startup, but indexing
on a tough problem that users will engage with daily can be great for bottom-
up building.

 _Thanks to Joe Averbukh, Daniel Woelfel, Kam Leung, Thomas Schranz for
reviewing drafts of this essay_

