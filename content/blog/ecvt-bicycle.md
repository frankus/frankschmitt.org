+++
title = "Half-Baked Idea: ECVT Bicycle"
date = 2007-04-11T16:53:18Z
aliases = ["/2007/04/ecvt-bicycle/"]

[taxonomies]
tags = ["halfbakery"]

[extra]
archived_from = "frankschmitt.org, 2007"
+++

I’ve been riding the ChargerBike that I appropriated from my dad to work for the last few weeks (at least on sunny days). For the vast majority of you who have never heard of a ChargerBike, it’s an electric-assist bicycle. There’s a 24-pound removable battery pack/controller that sits between the top tube and the down tube, which powers a little motor that has its own chain and freewheel driving the 7-speed hub shifter in parallel to the pedal chain. It’s an electric-assist bike in the truest sense: The motor controller turns on the juice in proportion to how hard you are pedaling. You can set the ratio in a range from half of your pedal effort all the way up to twice your pedal effort.

I’ve also been thinking about how it could be improved. That led me down the following little rathole which I’ll proceed to share with you.

I’ve been thinking of how you could have a bike with a variable road speed but a relatively constant pedal speed, and it could be done rather simply (if inefficiently) by connecting the pedals to an electronically-controlled generator, and the wheels to an electronically-controlled motor. Leaving aside the obvious efficiency and weight issues, how would one go about providing an intuitive user interface to such a beast?

My best guess at a good interface would be to have a dial that sets the pedal resistance (you could even vary it in concert with the angle of the crank arms). As you pedal faster, more power is generated, and the speed is increased (all else equal).

To make it into an electric-assist bike, you just add another dial labeled “boost” that sets the multiplier for how much power to inject in addition to your pedal power. Interestingly, you could also set the boost to a negative value and recharge the battery pack by using less energy to drive the bike than you are providing through the pedals. And you could use one of the brake levers to engage varying levels of regenerative braking to help recharge the batteries when going downhill.

That problem solved, the next question is how the efficiency can be improved. Well a few years ago Toyota introduced the Prius, a gasoline-electric hybrid vehicle with a fiendishly clever power-splitting gearbox design. It allows a constant engine speed over a wide range of road speeds, all the way from reverse to highway cruising. And it does all of this without an clutches or changing gear ratios.

We can borrow this principle (substituting the rider for the engine) to improve the efficiency of our ECVT bike. Rather than driving the generator directly, the pedals would drive the ring gear of a planetary gearset. The generator is driven by the sun gear, and the planet carrier is connected to the rear wheel. The exact mechanical arrangement is left as an exercise to the reader, but in any case we still have a hub motor driving the front wheel.

At low speeds, the wheel is more or less stopped, and as the rider pedals the generator is turned backwards. The generator is controlled so that the pedal torque stays constant, which causes a forward torque on the wheel, accelerating the bike. As before, the extra generated power is sent to the front wheel (so immediately we have the advantage of two-wheel drive). As the road speed increases, gradually the generator turns (still backwards) more and more slowly, and eventually stops. As the road speed increases further, the generator has to start turning forwards (now acting as a motor) to maintain the pedal torque at the preset value. To do this, the front hub motor has to start regenning slightly. Alternatively the boost dial could be set to a value where the batteries are simply being depleted slowly by providing the needed torque.

So we’ve reduced the amount of power that travels through the “electrical path,” but there’s still enough to make for a pretty lousy overall efficiency: even with expensive components, you’re talking about losing 20% of the energy at each end. But relatively little time is spent riding at very low or very high speeds, so you might be OK.

In the end I think this idea, while insufficiently baked to turn into a product, could make a pretty cool stunt/demo for someone to pull off.
