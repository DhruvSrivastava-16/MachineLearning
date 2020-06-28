# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 18:41:55 2020

@author: DHRUV
"""

import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

data_csv = pd.read_csv('ml-100k/u.data',sep = '\t')
#\t because the data is not ',' separated but instead tab (\t) separated
#till now we can see that data_csv has no header, so we will do it again

columns = ['user_id','item_id','rating','timestamp']
data_csv = pd.read_csv('ml-100k/u.data',sep = '\t',names=columns)
data_df = pd.DataFrame(data_csv)

item_csv = pd.read_csv('ml-100k/u.item',sep = '\|',header = None)
item_csv = item_csv[[0,1]] #reduce 24 columns (check in .shape) to just 2 columns
item_csv.columns = ['item_id','title']
item_df = pd.DataFrame(item_csv)

X=pd.merge(data_df, item_df, on='item_id') #merging 2 dataframes and linking them using 'item_id'

print(X,'\n')
print(X.head(n=3),'\n')
print(X.tail(n=5),'\n')

print(X.groupby('title').mean()['rating']) #this will group the titles by taking the mean OF RATINGS.
print("\n\n---------------------\n\n")
print(X.groupby('title').mean()['rating'].sort_values()) #this will group the titles by taking the mean OF RATINGS.
#and sort it in Increasing order.

print("\n\n---------------------\n\n")


print(X.groupby('title').mean()['rating'].sort_values(ascending=False)) #this will group the titles by taking the mean OF RATINGS.
#and sort it in Decreasing order.

ratings = pd.DataFrame(X.groupby('title').mean()['rating'])

Views_of_each = pd.DataFrame(X.groupby('title').count()['rating'])

merger = pd.merge(ratings, Views_of_each, on='title')
merger.columns = ['rating','views']

print("\n\n---------------------\n\n")

print(merger)

plt.hist(merger['rating'],bins=70)
plt.show()

sns.jointplot(x='rating',y='views',data=merger,alpha=0.25) #Very Important Depiction 

# MOVIE RECOMMENDER # will work with X dataframe 
print("\n\n----------MOVIE RECOMMENDER-----------\n\n")
print (X.head(3))

print("\n\n---------------------\n\n")

user_movierat = X.pivot_table( index = 'user_id', columns = 'title' , values = 'rating')

#user_movierat.to_csv('usermovierating.csv')

#print(user_movierating.head(n=3))

movie_rat_starwars =  user_movierat['Star Wars (1977)']

print(movie_rat_starwars)

#now we will find correlation of StarWars with other movies

starwar_corr = user_movierat.corrwith(movie_rat_starwars)

print('\n \n Star War Correlation with other movies is:',starwar_corr)

#in console try pd.DataFrame(starwar_corr,columns=['correlation'])

corr_starwars_df = pd.DataFrame(starwar_corr,columns=['correlation'])

#now lets drop the Nan values 

corr_starwars_df.dropna(inplace = True)
corr_starwars_df=corr_starwars_df.sort_values(by='correlation',ascending=False)

#now correlation depends upon number of same users who have seen starwars and that particular movie. So if less number of users have seen both the movies and have given the same rating, correlation becomes 1 easily. thus we put limit on them being at least >100
print("\n--------------------------**-------------------------\n")
final_corr_starwars = corr_starwars_df.join(merger['views'])
print(final_corr_starwars.head)

final_corr_starwars = final_corr_starwars[final_corr_starwars['views']>100].sort_values('correlation',ascending=False)

#lets generalise it through a function: 
    
def movie_recommendation(movie_name):
    movie_rat = user_movierat[movie_name]
    movie_rat_corr=user_movierat.corrwith(movie_rat)
    movie_rat_df = pd.DataFrame(movie_rat_corr,columns=['correlation'])
    movie_rat_df.dropna(inplace = True)
    final_corr_movie = movie_rat_df.join(merger['views'])
    Predictions = final_corr_movie[final_corr_movie['views']>100].sort_values('correlation',ascending=False)

    return Predictions

print('\nEg: Titanic (1997)')
movie_name = input("Enter a Movie which is in the dataset: ")
answer = movie_recommendation(movie_name)
print("\n-----Top 10-Movies Recommended For You--------\n")

print(answer.head(n=10))