# Intelligent Text Summarization:  a strategy to reduce information misrepresentation

Dissertation work submitted for MSc. Data Science at Trinity College Dublin by Shreya Jacob, 2021, Supervisor: Prof. Khurshid Ahmad

# Abstract
The year 2019 would remain in history forever due to the outbreak of Covid-19.  Eventhough it has been two years after the discovery of coronavirus,  the situation in many nations remains uncontrollable.  According to a few experts, one of the causes is public obliviousness due to distortion of the truth.  In an unfamiliar environment, the requirement for precise information is paramount.  The information gets diffused on a text clinefrom scientific papers to science magazine articles, then to newspapers, and then to thegeneral  public  via  social  media,  where  half  of  it  gets  lost  or  corrupted.   The  accurate findings of the researchers get suppressed.  This project work designs an automatic text summarization system based on the theory of lexical cohesion that can efficiently extractthe  pertinent  information  from  the  research  papers  to  reduce  the  misrepresentation  oftext in the first level of text cline.  The notion of lexical cohesion is that the repetition of words in the sentences creates a bond between them and brings the text closer.  Identifying the highly bonded sentences would thus aid in creating a summary that is conciseand meaningful.  The concept of using an external keyword list that consists of top terms present  in  the  domain  for  keyword  identification  was  a  significant  contribution  of  thiswork.  The system efficiency was statistically evaluated using various metrics like average sentence length, readability, sentiment similarity, and syntactic similarity.  The evaluation results of the summaries generated for ten research papers confirmed the efficiency of the algorithm when compared to their abstracts (human-generated summaries).  Although the summaries were less readable than the abstracts, they were highly similar to the original text on sentiment and syntactic similarity.

To run,

python3 summarization.py to summarize any text document

python3 evaluation.py to evaluate any two text documents
