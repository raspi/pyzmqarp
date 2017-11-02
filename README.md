# pyzmqarp

Send Linux kernel network neighbors (ARP) changes to ZMQ Publisher socket where n subscribers can listen to changes.

For example:

  * Keep database of reachable IPs 
  * Offer realtime log for example via websocket

Equivalent to CLI tools:

    % ip monitor neigh
    
or `arpwatch` tool found in many distributions. 

[ZMQ](http://zeromq.org/) is language agnostic so zmq socket subscribers can be written in all languages that zmq supports (C, PHP, Python, Lua, Haxe, C++, C#, CL, Delphi, Erlang, F#, Felix, Haskell, Java, Objective-C, Ruby, Ada, Basic, Clojure, Go, Haxe, Node.js, ooc, Perl, Scala, ..).

# requirements

 * [pyroute2](https://pypi.python.org/pypi/pyroute2)
 * [zmq](https://pypi.python.org/pypi/pyzmq)
 
