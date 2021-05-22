import hedgehog as hh
import pandas as pd
import numpy as np
np.random.seed(1000)

bn = hh.BayesNet(
        ('Burglary', 'Alarm'),
        ('Earthquake', 'Alarm'),
        ('Alarm', 'John'),
        ('Alarm', 'Mary')
)

bn.P['Burglary'] = pd.Series({False: .99, True: .01})
bn.P['Earthquake'] = pd.Series({False: .98, True: .02})

bn.P['Alarm'] = pd.Series({
     (True, True, True): .95,
     (True, True, False): .05,

     (True, False, True): .94,
     (True, False, False): .06,

     (False, True, True): .29,
     (False, True, False): .711,

     (False, False, True): .001,
     (False, False, False): .999
 })

# P(John calls | Alarm)
bn.P['John'] = pd.Series({
     (True, True): .9,
     (True, False): .1,
     (False, True): .05,
     (False, False): .95
 })

# P(Mary calls | Alarm)
bn.P['Mary'] = pd.Series({
     (True, True): .7,
     (True, False): .3,
     (False, True): .01,
     (False, False): .99
})

bn.prepare()

#r1 = bn.query('Burglary', n_iterations=10000, algorithm='exact', event={'Alarm': True})
#r2 = bn.query('Alarm', n_iterations=10000, algorithm='exact', event={'Earthquake': True, 'Burglary': True})
#r3 = bn.query('Burglary', n_iterations=10000, algorithm='exact', event={'John': True, 'Mary': False})
r4 = bn.query('Burglary', n_iterations=100000, algorithm='exact', event={'John': True, 'Mary': True})
#r5 = bn.query('Burglary', n_iterations=10000, algorithm='exact', event={'Alarm': True, 'Earthquake': True})

#print(r1)
#print(r2)
#print(r3)
print(r4)
#print(r5)

print('######################################')

cn = hh.BayesNet(
        ('Tempering', 'Alarm'),
        ('Fire', 'Alarm'),
        ('Fire', 'Smoke'),
        ('Alarm', 'Leaving'),
        ('Leaving', 'Report')
)

cn.P['Tempering'] = pd.Series({False: .98, True: .02})
cn.P['Fire'] = pd.Series({False: .99, True: .01})

cn.P['Alarm'] = pd.Series({
     (True, True, True): .5,
     (True, True, False): .5,

     (True, False, True): .85,
     (True, False, False): .15,

     (False, True, True): .99,
     (False, True, False): .01,

     (False, False, True): .0001,
     (False, False, False): .9999
 })

# P(John calls | Alarm)
cn.P['Smoke'] = pd.Series({
     (True, True): .9, (True, False): .1,
     (False, True): .01, (False, False): .99
 })

# P(Mary calls | Alarm)
cn.P['Leaving'] = pd.Series({
     (True, True): .88, (True, False): .12,
     (False, True): .001, (False, False): .999
})

# P(Mary calls | Alarm)
cn.P['Report'] = pd.Series({
     (True, True): .75, (True, False): .25,
     (False, True): .01, (False, False): .99
})


cn.prepare()

#r1 = cn.query('Alarm', n_iterations=1000, algorithm='likelihood', event={'Tempering': True, 'Smoke': False})
#r2 = cn.query('Alarm', n_iterations=1000, algorithm='likelihood', event={'Tempering': False, 'Smoke': True})
#r3 = cn.query('Fire', n_iterations=1000, algorithm='likelihood', event={'Alarm': True, 'Smoke': False})
#r4 = cn.query('Fire', n_iterations=1000, algorithm='likelihood', event={'Alarm': True, 'Leaving': True})
#r5 = cn.query('Tempering', n_iterations=10000, algorithm='likelihood', event={'Alarm': True, 'Smoke': True, 'Leaving': True})

#print(r1)
#print(r2)
#print(r3)
#print(r4)
#print(r5)