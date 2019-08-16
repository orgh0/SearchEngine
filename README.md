# SearchEngine
Contains code to build an inverted index, and a search engine on top of it


# Building the Inverted Index

<-> Indexes are built for 4 types of items
      -> Text
      -> Title
      -> Category
      -> Infobox

<-> We iterate through `<page>` `</page>` tags of the WIKI dump.

<-> For each of these pages, following operation is performed:
      -> Update the index of text
      -> Update the index of Title
      -> Update the index of Category
      -> Update the index of Infobox
      
      
<-> Update of index is the following set of operations:

      -> Add all new tokens to the dict
      -> Update frequency of the other tokens
      

<-> We keep a pagination_val, on it's multiples, we create index files the following operations are performed:

      -> Store all the 4 indexes in different files and update the file number.
