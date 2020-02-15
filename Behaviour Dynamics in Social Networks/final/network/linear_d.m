function x = linear_d(p,v)
    global k;
    global dt;
    global endtimeofsimulation
    
    current = (k*dt);
    
    x = endtimeofsimulation - (1 / (p(1) / current)) * endtimeofsimulation;

end

