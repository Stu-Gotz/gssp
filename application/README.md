# Post-Graduate Major Project

This is my post-graduate major project for the Information and Communication Technology (ICT) Master's Course at Anglia Ruskin University. All names and images of Pokémon are owned by Nintendo. Usage stats information is owned by Smogon.com.

# Motivation
I have had an interest in full-stack development since I started programming in earnest some four years ago. Understanding how to create a software ecosystem that works together to perform a higher task is something that appeals to me. Most of my current professional experience has been using Python to do data science work and I was always yearning for more proper software development opportunities. As well I often encountered, in my professional experience, that teams were often rigidly inflexible to the idea of using two database management systems to better store data in a logical manner.

# About this project
This project uses a Vue front-end to serve an application to the user to compare their team against current metagame trends as indicated by usage stats. While usage stats do not describe the whole picture of a metagame, it provides a good reference on what encounters one might expect as they battle their way up the ladder.

Data is collected and parsed with Python scripts (found in the `python` folder) from [Smogon](https://smogon.com/stats), the main repository of available battle data information from PokemonShowdown, an online battle simulator created by the Smogon.com community. More information on stats and rankings can be found [here](https://www.smogon.com/forums/threads/gen-9-smogon-university-usage-statistics-discussion-thread.3711767/). Usage stats for this application are stored in a PostgreSQL (v15) database. In the application, users are able to login and register, and that user information is stored in a MongoDB collection, as users may want to have more or less information about themselves on their profile. Separating the user login credentials and profile information also provides an extra layer of security. Only the three most recent months of usage stats data is displayed. Some tiers may not have three months available, especially if they are not frequently played tiers. Any errors in usage stats data, such as missing data is likely a fault from the original source. 

An Express server operates as the connector for the front end application and the back end, making the stored usage stats data readily available for consumption in the front-end. At the moment there are only three basic GET routes to retrieve the usage stats from the PostgreSQL database and two POST routes to handle login and registration. Pinia stores, a state management system designed for use in Vite and Vue applications, manages the state of a user's session and performs all the calls to the API, creating a separation of responsibilities from the front end and back end.

As far as resources that were helpful in this project vis-á-vis data presentation, the PokeAPI and [koffing](https://github.com/itsjavi/koffing) javascript library are essential. [PokeApi](https://pokeapi.com) aims to become the "one stop shop" for Pokémon data online, and has a wealth of information available, some of which was relied on for this project with its JavaScript plugin. The koffing library is built by a member of the Smogon.com community and parses team text data from PokemonShowdown exports.

# Contributing

I hope to expand on this project, as there are several areas for improvement.
1. Increase the speed - Due to the number of iterating asynchronous calls, it takes a noticeable amount of time to process the user input.
2. More analysis - I would like to have a better analysis system for user submissions, including the teams average rank, type matchups and so forth. This will require additional backend work to process the moveset stats data from the Smogon stats source.
3. Better presentation - I consider the current presentation rather basic and I would like to make it look nicer, but I tend to prioritise appearance behind functionality.
4. Viewable stats data - Presenting stats data in a way that users can casually scroll through and view data that is of particular interest to them would be useful, including enabling filtering options and a search function.

To contribute, please create a fork and clone that fork and submit pull requests when changes have been made. I will approve or deny those changes as they come through. For more information on how to fork a repository, please visit the (official GitHub docs)[https://docs.github.com/en/get-started/quickstart/fork-a-repo]
