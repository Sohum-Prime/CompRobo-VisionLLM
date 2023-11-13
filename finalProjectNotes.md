> I tested out two apps designed for the BVI: Clew made by Olin and SeeingAI made by Microsoft. My intention was to discover where current apps are limited and how llms can help.

### SeeingAI

When I watched the [videos]() for this app I was impressed with the number of modes it had: currency mode, short text mode, document mode, and more. But, when using the app I realized **having modes switch automatically based on the context might be more helpful for a BVI impaired person (validate this to know if true!)** and if so, a generalized llm + cv app that can detect where a person's phone is pointing, validate if this is what they want it to be pointing at, and execute the necessary function might be better. There's also an opportunity for speech to text where the person tells the device what it wants to do, moves the device around, and the model figures out how to do this. The example in my head is:

> "I want to find the nearest exit, help me find it." The app doesn't have the ability to successfully take in navigation queries and figure out how to help a user. And, what about the methods someone wants to use to exit? Are they elevator only? Or stairs? Are they on the fifteenth floor and need to return to the third. I think more of these detailed scenarios are where we can get curiously testful and design something that solves one of these well. 

One partial counter to the point about validating what a user wants to look at is the document mode on the app which tells the user how to reorient their screen so a picture of the menu can be taken. In addition, I think this mode is helpful for executing a specialized function like reading a menu but not for general purpose. We want to make this general purpose. 

In this [google drive folder](https://drive.google.com/drive/folders/1eqZr2BpUtPq1p-QUVP0E2yLJgRxPMD9O?usp=sharing) folder I've shared 8 images from my tests and categorized examples into 4 categories: great, mode problem, poor context, and nosignrec.

It did **great** with document mode and speech to text. It also did well stating an exit sign but only when I got close to it and didn't have glare from other lights near rm 426. Hence the problem **nosignrec** too.

SeeingAI had **mode problems** as I mentioned earlier. When I stood next to a [male bathroom sign on the wall](https://drive.google.com/file/d/1yEwfxfWLJ2NqftEw-XsUFf7fThhJp77e/view?usp=sharing) it wasn't able to recognize this and responded with "A sign on a purple wall." Interestingly, [ChatGPT did well with this one](https://drive.google.com/file/d/1DeMIcjfIGs5zlQ4s77DMNFQirIM9Jzf9/view?usp=drive_link). **Poor context** is very similar to mode problem. When standing next to the elevator button on the first floor, for example it told me "A close up of a button". 

### Clew app
Clew app is very useful when we set up a route so we can navigate places but I think the limit is, we know how to get one way or have someone to help us in the initial navigation before we can do it ourselves. 

It'd be interesting to look more into Clew's integration of the Google Maps API and how this is helpful for directions. 

### Both app's limitations
I wonder how both apps do real-time motion detection. For example, if a BVI person is at a crosswalk and a car wants to turn right and begins doing so, how will they know about this vehicle and their intention? If we want this app to work in the general environments this is a valid consideration to make.

### Initial problems to solve
- Not able to generate instructions for new routes when user hasn't been there before. (Validated what we already knew)
- Limited input from BVI user outside of mode swiping or anchor point setting. (New idea and application for user)
- Not able to interpret objects, only able to say what's generally there (New idea and application for user)