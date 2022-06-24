# How to get those 9s: on improving service uptime


What do you do when you inherit, or just as commonly, create, a service with
low reliability?

 _Improving reliability can be daunting_. You have low visibility into the
system, and sometimes, if you inherited it, low expertise. The system is ever-
changing, so if you just metric on success rate, you’ll consistently come
across new errors, as soon as you fix old ones.

 _But…with the right strategy, improving reliability can be fun… maybe even
thrilling!_ You’ll get to dive deep and solve some hairy problems. You’ll
create solutions that not only improve your service…but improve all services
in your company.

Now, to do this, I’ve come down to a strategy of three steps:

  1.  **Stop the bleeding** : _Represent the service as it is and hold the fort_
  2. **Bring Observability:** _Identify the root causes weekly_
  3.  **Incrementally Improve:** _Retro and improve based on the most important root causes_

## 1\. Stop the bleeding: Represent the service as it is and hold the fort

This service is often already goal on uptime: maybe with that 99.99.

Most likely though, the service is failing that so consistently, that the goal
no longer has any signal.

Our goal here: _bring back the signal_. To do this,

 **Action Item 1: Update the uptime goal to represent the current state of the
system**

Update the uptime, so that this metric to represent the current P99 uptime and
latency values. If you do this, the goal should start to go green. This will
help you become intentional about uptime slips moving forward.

This brings you back that signal. Now, just because it’s green, doesn’t mean .
that you stop here and go on with our day. The next step is to improve it. To
do that we need to

## 2\. Bring Observability: Identify the root causes weekly

To have a meaningful approach to improving uptime, we’ll need visibility into
your system.

Visibility in this case means the answer this question:

 **Question 1: What were the root causes of incidents last week?**

The key here is _root cause._ You want to know: each week, what where the
actual errors that brought down the system.

 **Action Item 2: Answer “what were the root cause incidents last week?”**

You’ll need to invest in your tooling, to create a list of the big bugs that
brought the system down.

Sometimes, especially in distributed systems, it can be very hard to get a
sense of the _root cause — a_ root cause could be a leaf node service error,
and your infrastructure may not be aggregating by leaf nodes.

Nevertheless, it’s possible. You can look into observability tooling — the
most promising one I know right now is
[www.honeycomb.io](http://www.honeycomb.io) (no affiliation) — but more likely
then not, you can use your existing tooling and an hour of manual work /
scripting, to get a good sense.

Once you know that answer, you can

## 3\. Improve Incrementally: Retro and improve based on the most important
root causes

As you get this information, you can begin to run a “mini incident management”
series:

 **Action Item 3: Create a “retro” series for fixing root causes**

For the biggest error, take the steps needed to _fix and remediate the root
cause._ This includes fixing the bug, as well as adding a test or an alert, or
turning a hard dependency into a soft dependency.

If you do this consistently enough, you should begin to see our uptime
improve. You can goal yourself on the top-line metric (uptime reduction), but
also the number of root cause errors removed, remediations added (tests,
process changes, etc), etc.

I read once in Nasism Taleb’s books: one plane crash, makes all planes safer.
This is because the aviation agency investigates the plane crash, and makes
sure that kind of error doesn’t happen again. This applies to your service
too. When you do these retoes, you all of a sudden make your service better
and better and better. It becomes… _antifragile!_

 ** _Summary of Action Items_**

  1. Update your uptime to represent the current state of the system
  2. Answer _“what were the root cause incidents last week?”_

  3. Create a “retro” series for fixing root causes

