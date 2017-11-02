# pyzmqarp

Send Linux kernel network neighbors (ARP) changes to ZMQ Publisher socket where n subscribers can listen to changes and for example keep database or offer realtime log.

Equivalent to:

    % ip monitor neigh
    
or `arpwatch` tool found in many distributions.
