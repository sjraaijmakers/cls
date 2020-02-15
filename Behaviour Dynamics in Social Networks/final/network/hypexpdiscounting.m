function x=hypexpdiscounting(p,v)
% p(1) = alpha
% p(2) = P
%     if p(1)==0
        x=1/(1+p(2)*v(1));
%     else
%         x =1/(1+p(2)*v(1)*(exp(p(1)*v(1))-1)/(p(1)*v(1)));
end