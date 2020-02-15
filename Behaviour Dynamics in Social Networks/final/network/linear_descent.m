function x = linear_descent(p,v)
    global k;
    global dt;
    global endtimeofsimulation;
    
    current = (k*dt);
    
    x = 1 - (1-p(1)) / (endtimeofsimulation / current);
end

