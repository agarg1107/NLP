w1 = -0.1
w2 = 0.4

x1 = 0
x2 = 1
bias = 0.4
learn = 0.25
ans =0;
i =1;
w1 = 0.3
w2 = -0.2
def sig(a):
    if(a>= 0):
        return 1
    else:
        return 0
while(i < 500):
    cal = (w1*x1 + w2*x1) - bias
    if(sig(cal) == 1):
        w1 = w1 + x1*learn*(0-sig(cal))
        w2 = w2 + x1*learn*(0-sig(cal))
        print(w1)
        print(w2)
        print("____________");
        ans =0
    ans = ans +1
    cal = (w1 * x1 + w2 * x2) - bias
    if (sig(cal) == 0):
        w1 = w1 + x1 * learn * (0 - sig(cal))
        w2 = w2 + x2 * learn * (0 - sig(cal))
        print(w1);
        print(w2);
        print("____________");
        ans =0;
    ans = ans + 1
    cal = (w1 * x2 + w2 * x1) - bias
    if (sig(cal) == 0):
        w1 = w1 + x2 * learn * (0 - sig(cal))
        w2 = w2 + x1 * learn * (0 - sig(cal))
        print(w1);
        print(w2);
        print("____________");
        ans =0;

    ans = ans +1
    cal = (w1 * x2 + w2 * x2) - bias
    if (sig(cal) == 0):
        w1 = w1 + x2 * learn * (1 - sig(cal))
        w2 = w2 + x2 * learn * (1 - sig(cal))
        print(w1);
        print(w2);
        print("____________");
        ans =0;
    ans = ans+1

    i = i+1

print("Final")
print(w1);
print(w2);