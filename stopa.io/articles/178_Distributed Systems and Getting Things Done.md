# Distributed Systems and Getting Things Done


In most programs, it’s best to have a single app state, that trickles down,
and are handled by pure functions.

Erlang takes quite a different approach. There are Supervisors, and Actors,
which encapsulate internal state, and talk to eachother via messages.

This seems more complex, but actually, it is simpler when looked at by the
lens of distributed software. It’s complex to keep a single state in sync when
you’re across datacenters.

What Erlang does is, to essentially embrace the distributed nature of the
problem, and goes by the assumption that if each Supervisor takes care of what
it’s responsible for well, then the system will work.

This was a pretty breakthrough parallel for me, in my task management. Instead
of trying to build a top down system, it’s all about making sure the small
parts work well.

Getting Things Done, by David Allen, is the Erlang of task management x)

