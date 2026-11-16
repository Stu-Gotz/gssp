# Smogon Stats Browser 

## A brief about

Originally this started as a sister project to my Python [usage stats collection project](https://github.com/Stu-Gotz/smog_usage_stats). I was in a new data science / analyst role and Pokemon is structured data I've intimate knowledge of because of a misspent youth. I loved battling on Smogon's Showdown and earlier ShoddyBattle systems, but the summary data comes in text files, so I sought to fill that gap. Eventually, I got interested in web design and development, and after making a bunch of silly projects for practice, wanted to make one for real. That is this. It's been a long time in development as my interest and time available ebbs and flows.

I am open to help and contributions from other developers. I'm not vibe coding anything, but I do use claude etc as a faster StackOverflow because that place has become a den of sinful pride. I'm by no means an expert at this, but because I feel myself becoming stupider every day as I offload boring tasks at work onto an uncaring, unfeeling GPU halfway across the world in some poor rural town in middle Pennsylvania, I want to actually use what I paid all those thousands of dollars to a university to learn. This is becoming abit of a polemic so I'll just say that I don't really care how you contribute or anything, if you upload a bunch of very clearly AI-generated 80,000 lines of whatever I will reject it without looking at it.

## Bit more technical

This is a Vue3 frontend powered by a Django backend. Why? Because I like them. Vue is like the happy marriage between vanilla JS and something overly cumbersome like React or Angular. It's fast, it's quick, it's easy to use (imo) and I fucking hate React. Django is just a really good backend, and I love Python. I think in the future I'd be kinda keen to try out something like C# or Rust though, but that's miles away. I'm using Postgresql because there is no DB but RDB and it offers an excellent amount of flexibility. Originally it had a hybrid system of MongoDB for users and Postgresql for usage stats data, but that quickly grew tedious. Using MongoDB also reinforced my core belief that all you really need are RDBMS. 

I'm not entirely sure I'm sold on the structure of the database, but that's something to explore later. Data can be populated locally by creating your own `.env` and running the bit under `if __name__ == '__main__'` in `data_collection.py`. It does require Python>=3.10 and my `smog_usage_stats` package from above, which can be pip installed. The code in the bottom *does* come from Claude, but it's just upload scripts that are kinda one-timers and I couldn't be bothered if I'm honest, this is something I work on after my day job.

I have a really shitty powerpoint that I don't update that was meant to contain a bunch of user stories and flowcharts and stuff but, man, one thing this has really taught me is I do not like administrative work. Even this readme is a chore, but I owe anyone whos actually reading this more than some AI summary bullshit.

### Contributing

If you want to contribute, submit a PR and I'll get to it when I get to it. 

### License

GPL 3.0

### Disclaimer

I am not affiliated with Smogon, Nintendo or GameFreak in any way and do not claim ownership of any of the data or official artwork used within this project. I am just a lifelong fan.

I would like to thank very much Smogon for their wonderful data curation efforts (shoutout to DougNotDoug if he's still doing it), the PokeAPI which this project relies on in small parts mostly for sprites or patching small datafields.  