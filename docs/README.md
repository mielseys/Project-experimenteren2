# Circuits

## Faraday-effect met lock-in versterker

Ik heb een site van PhysicsOpenLab gevonden waar ze vrij DIY-achtig het Faraday-effect willen meten met een lock-in versterker.

- Referentie: **[Faraday Rotation – PhysicsOpenLab](https://physicsopenlab.org/2019/08/20/faraday-rotation/)**


In [deze](https://web.pa.msu.edu/people/edmunds/Lock_In_Amplifiers/lock_in_lab_experiments_univ_tennessee.pdf) paper is er een sectie ``Getting to know the Lock-in``waar Dr. G. Bradley Armen wat dieper in gaan oop hoe een lock in amplifier werkt en hoe je er mee werkt.

Hij praat daar ook over de frequentie:

Finally, the Mode button selects whether to lock onto the input reference frequency f, or at twice this frequency 2f. This is useful when your response of interest doesn’t care about the polarity of the modulation, and so occurs twice as fast. An example of such a case is the AC flicker of light bulbs: they’re supplied with 60 Hz current, but since the filaments are indifferent to current direction, light is radiated with a 120 Hz flicker.

The output stage consists of the actual signal output and some other controls. The actual output can be viewed on the analog meter which displays ± the full-scale sensitivity. Despite the prejudice of the young against anything non-digital, the meter is very useful as a quick guide to what’s happening. Along with the meter output there is an analog output (BNC) which can be connected to a DMM or oscilloscope. This output is
calibrated to give ±1.00 V at full scale. So, for example, if this voltage is 0.580 V on the 250 mV range, the signal reading is 0.580 × 250 = 145 μV. An over-range light informs you when the sensitivity is set too high.

A thoughtful person might wonder just why we want this adjustable – don’t we
want it as sharp as possible to get the best reading? The answer is a matter of
practicality. A Low-Pass filter actually corresponds to a time averaging of the signal (see
App. A). If there is a change in the signal, you must wait for a period of about 5 time-
constants for the averaging to settle to a good result. An infinitely sharp filter would
imply an infinite wait. Thus, there is a trade off between how quickly you want to make
a measurement, and how much low-frequency noise you’re able to tolerate.

circuit-setup-lockin

![Circuit](Docs/Circuits/.png)

Waarbij de DMM onze oscilloscoop zal zijn en de simulator box onze functie generator.
