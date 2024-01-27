# Potential Talents

### <b>Background</b>

As a talent sourcing and management company, we are interested in finding talented individuals for sourcing these candidates to technology companies. Finding talented candidates is not easy, for several reasons. The first reason is one needs to understand what the role is very well to fill in that spot, this requires understanding the client’s needs and what they are looking for in a potential candidate. The second reason is one needs to understand what makes a candidate shine for the role we are in search for. Third, where to find talented individuals is another challenge.

The nature of our job requires a lot of human labor and is full of manual operations. Towards automating this process we want to build a better approach that could save us time and finally help us spot potential candidates that could fit the roles we are in search for. Moreover, going beyond that for a specific role we want to fill in we are interested in developing a machine learning powered pipeline that could spot talented individuals, and rank them based on their fitness.

We are right now semi-automatically sourcing a few candidates, therefore the sourcing part is not a concern at this time but we expect to first determine best matching candidates based on how fit these candidates are for a given role. We generally make these searches based on some keywords such as “full-stack software engineer”, “engineering manager” or “aspiring human resources” based on the role we are trying to fill in. These keywords might change, and you can expect that specific keywords will be provided to you.

Assuming that we were able to list and rank fitting candidates, we then employ a review procedure, as each candidate needs to be reviewed and then determined how good a fit they are through manual inspection. This procedure is done manually and at the end of this manual review, we might choose not the first fitting candidate in the list but maybe the 7th candidate in the list. If that happens, we are interested in being able to re-rank the previous list based on this information. This supervisory signal is going to be supplied by starring the 7th candidate in the list. Starring one candidate actually sets this candidate as an ideal candidate for the given role. Then, we expect the list to be re-ranked each time a candidate is starred.

### <b>Data Description</b>

The data comes from our sourcing efforts. We removed any field that could directly reveal personal details and gave a unique identifier for each candidate.

#### Attributes:
- id : unique identifier for candidate (numeric)
- job_title : job title for candidate (text)
- location : geographical location for candidate (text)
- connections: number of connections candidate has, 500+ means over 500 (text)

#### Output (desired target):
- fit - how fit the candidate is for the role? (numeric, probability between 0-1)

#### Keywords: “Aspiring human resources” or “seeking human resources”

### <b>Goal</b>
- Predict how fit the candidate is based on their available information (variable fit).

### <b> Success Metrics</b>
- Rank candidates based on a fitness score.
- Re-rank candidates when a candidate is starred.

### <b>Other Objectives</b>
- We are interested in a robust algorithm, tell us how your solution works and show us how your ranking gets better with each starring action.
- How can we filter out candidates which in the first place should not be in this list?
- Can we determine a cut-off point that would work for other roles without losing high potential candidates?
- Do you have any ideas that we should explore so that we can even automate this procedure to prevent human bias?

### <b> Results</b>

<u>Fitness Scores</u>

The fitness scores for each candidate, with respect to specific job roles, were determined by computing similarity scores between their job title and keywords (i.e., 'aspiring human resources', 'seeking human resources'). To ensure a robust evaluation, we employed five distinct word embedding techniques: TF-IDF, TensorFlow's Tokenizer, GloVe, Word2Vec, and FastText.

These techniques generated multiple fitness scores for each candidate, ranging from 0 to 1. These scores enabled us to identify candidates who were significantly misaligned with the desired roles, as indicated by a fitness score of 0. To improve the quality of our candidate list and remove those initially unfit for the roles, a thorough examination was conducted. Based on this assessment, we filtered out candidates with a fitness score of 0 by any of the five techniques, deeming them irrelevant to the job roles.

<u>Ranking Algorithms</u>

We utilized two Learning To Rank (LTR) algorithms: XGBoost and LGBM Rankers. In the evaluation on the test dataset, both ranking models showcased a mean absolute difference of less than 2 between the actual and predicted ranks, affirming their high accuracy in rank prediction.

Furthermore, these ranking models effectively accommodated manual input of feedback, facilitating a re-ranking of the candidate list based on the provided feedback. Here's how it functioned: if a candidate received a 'star' through manual review of the ranked list, they were promoted to the top rank. Subsequently, the ranking models were re-trained with this updated ranking information, ensuring continuous refinement and alignment with the manual assessments.

<u>Applications</u>

Our robust scoring and ranking system allows easy integration by simply substituting candidate data and keywords (i.e., specific job roles to fill) with new ones in the pipeline.  Moreover, the system and insights obtained from this project can be applied to a wide array of information retrieval challenges.

### <b>Notebook and Installation</b>

For more details, you may refer to <a href='https://github.com/henryhyunwookim/Potential-Talents/blob/main/Potential%20Talents.ipynb'>this notebook</a> directly.

To run Potential Talents.ipynb locally, please clone or fork this repo and install the required packages by running the following command:

pip install -r requirements.txt

##### <i>* Associated with Apziva</i>
