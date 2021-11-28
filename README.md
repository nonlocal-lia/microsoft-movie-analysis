![Header Image](/images/director_shot.jpeg)

# Microsoft Movie Market Analysis
***
Author: [Lia Elwonger](mailto:lelwonger@gmail.com)

## Overview
***
This project analyzes data from [IMDb](imdb.com) and [The Numbers](the-numbers.com) to produce recommendations
for a hypothetical attempt by Microsoft to start a movie studio. Descriptive analysis of the relationship between
director, genre and release date are used to produce three recommendations for their first film release.

## Business Problem
***
Microsoft has decided to create a new movie studio, but they lack experience in this market. There are many difficult problems facing new studios entering the market.

To aid in this endeavor we will give recommendations to help address three core problems that any studio will have to answer in the course of making a project:

* Determining what type of project to pursue.
* Determining what talent should be hired.
* Determining the timeline of the project.

To help answer elements of these problems we will investigate the answers to three related questions:

* What genre has had the high average profit in the past 20 years?
* What directors have had the highest average return in that genre?
* What month of the year is good to release a major film?

## Data
***
Data from IMDb provided information on the genre of films as well as their directors. Budget and ticket revenue was 
taken from The Numbers. The data was filtered to include only movies with budgets over $10 million produced in the last 20 years
to avoid including data of little revelance to the Microsoft project.

## Methods
***
Data was grouped by genre and the mean and std of the worldwide profit for each genre was calculated.
The data was also grouped by release month and the mean and std of the profit was calculated.
Once a recommended genre was selected, the director data was filtered by genre and the mean and total profit
that each director earned within that genre was calculated.

## Results
***
The genre with the highest average profit of big budget movies with more than 20 films in the past 20 years is
the Sci-Fi genre, followed closely by the Animation genre. Sci-Fi is a more risky pick than animation, but synergizes
well with microsofts other properties and has the chance of the highest rewards.

![Genre Chart](/images/genre_chart.png)

The month with the highest mean profit for Sci-Fi movies in the past 20 years is May, it is also has fairly low variance.

![Date Chart](/images/release_chart.png)

The director with the highest mean profit per Sci-Fi movie release was Colin Trevorrow, but they only released 1 Sci-FI film (Jurrasic World)
Joss Whedon is the second highest, with more than one film in his track record.

![Director Chart](/images/director_chart.png)

## Conclusions
***
Stated recommendations:

* Release a Sci-Fi film.
* Hire Joss Whedon to direct it.
* Aim to release the movie in May with June as a backup in case of delays.

### Limitations and Future Work
The calculation of the profit of each film only included ticket revenue and production budget. It did not include marketing budget
nor did it include any revenues from associate film mechandise.

Further analysis and research could help

* Reanalyze profit data with data on marketing budgets and merchandise profits.
* Investigate whether Microsoft has existing media brands that would fit well with a Sci-Fi film.
* Investigate sales in the Sci-Fi novel genre and see if any highly selling books would make for a good adaptation.

***

## For More Information

Please review my full analysis in [our Jupyter Notebook](./microsoft-movie-analysis.ipynb) or our [presentation](./Microsoft Movie Presentation.pdf).

For any additional questions, please contact **Lia Elwonger lelwonger@gmail.com**

## Repository Structure

```
├── README.md                           <- The top-level README for reviewers of this project
├── microsoft-movie-analysis.ipynb      <- Narrative documentation of analysis in Jupyter notebook
├── Microsoft Movie Presentation.pdf    <- PDF version of project presentation
├── data                                <- Both sourced externally and generated from code
├── code                                <- Functions for cleaning the data and constructing visualizations
└── images                              <- Both sourced externally and generated from code
```
