import pandas as pd
def conditional_probability(total, passed_math, passed_both):
    # we are asked prob of passing in science given passed in maths
    # P(S|M) = P(both)/P(maths)
    if (passed_math <= 0 or total <=0 or passed_both < 0
          or passed_both > passed_math):
        return "invalid input"
    
    result = round(passed_both/ passed_math, 2)
