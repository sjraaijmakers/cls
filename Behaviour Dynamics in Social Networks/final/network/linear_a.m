function x = linear_a(p,v)
    global k;
    global dt;
    global endtimeofsimulation;
    
    current = (k*dt);
        
    x = (current / endtimeofsimulation)
end

