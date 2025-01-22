# Challenge Description

### Welcome,

First of all, congratulations on being here: it’s no coincidence that you passed the selection process and earned a spot among the best. In fact, only the **top 10% of candidates** have gained access to this exclusive challenge. This means one thing: you are the best of the best, the **crème de la crème**. 

But beware: with great talent comes great responsibility.

Today’s challenge will not be simple at all. At first glance, it may seem complex, even daunting. It will require time, focus, and creativity just to fully understand.

But we know that you are not people who give up when faced with difficulties. On the contrary, it is precisely in these challenges that true talent emerges. And we are confident that you will prove to be up to the task.

# Challenge Description 💫

Welcome to Cosmic Cycle 789, where humanity has not only transcended the boundaries of its solar system but also those of known dimensions. In this vast tapestry of realities and cultures, gastronomy has evolved into an art that transcends space and time.

Restaurants of all kinds enrich the very fabric of the multiverse: from Pandora’s sushi bars serving delicate Magikarp sashimi and Vaporeon dumplings to Tatooine’s taverns where Pipe Weed flavors exquisite dishes, and modern venues where Slurm creates sauces with contrasting flavors—the culinary universe is vast and full of surprises.

Galactic expansion has brought new responsibilities. The Galactic Federation carefully monitors every ingredient, preparation technique, and certification required to ensure that food served is safe for all sentient species. Chefs must navigate complex regulations, manage exotic ingredients that exist simultaneously in multiple quantum states, and respect the dietary restrictions of hundreds of species from every corner of the multiverse.

At the heart of this cosmic archipelago of flavors stands a titan of culinary proportions, an entity that transcends mere culinary materiality: the Cosmic Pizza. Legend has it that its mozzarella was sourced from the Milky Way itself and that its baking required the heat of three suns. No one knows its origins, and religious cults have founded their faith around its mystery.

# Technical Specifications ⚙️

Your mission is to develop an AI assistant to help intergalactic travelers navigate this rich culinary landscape.

The system must be capable of suggesting appropriate dishes to users based on their requests by:

- Interpreting questions in natural language
- Handling complex queries involving preferences and dietary restrictions
- Processing information from various sources (menus, blog posts, galactic laws, and cookbooks)
- Verifying (when required by the question) the compliance of dishes with applicable regulations

Additionally, your system must:

- Use Generative AI techniques (RAG, AI Agents) to process and understand the provided documents
- Implement a software module capable of:
  - Receiving a user request related to possible dishes matching criteria expressed in natural language
  - Providing an output list of dishes that meet these criteria based on the provided documentation

# Documentation 📁

You will have access to a rich set of documents belonging to this galactic gastronomic ecosystem:

- `planets_distance_matrix.csv`
  - A CSV containing the matrix of distances in light years between planets hosting different restaurants.
    
- `Galactic Code.pdf`
  - A legislative document containing:
    - Quantitative limits on the use of certain ingredients in dish preparation
    - Restrictions on the certifications chefs need to acquire to use specific preparation techniques
    
- `Cooking Manual.md`
  - A cooking manual including:
    - The list and description of certifications a chef can acquire
    - The list of professional culinary organizations a chef can join
    - The list and description of existing culinary preparation techniques
    
- `Menus (30 restaurants)`
  - Markdown documents containing the menus of 30 different restaurants.
    
- `Blog posts`
  - Markdown documents containing additional information about certain restaurants.
    
- `dish_mapping.json`
  - A mapping of dishes to progressive numeric IDs, required for generating the final output.
    
- `questions.csv`
  - A file containing the list of questions used to evaluate the implemented solution.

# Evaluation Criteria 💯​

Teams will be evaluated based on the correctness of the responses provided by the implemented software module and the originality of the proposed approach. 

Correctness will be assessed using a standardized set of queries provided to all teams. For each query, the correctness score will be calculated using the Jaccard Similarity, measuring the overlap between the list of dishes returned by the implemented system and the expected list of dishes in the reference solution.

Example CSV output file to upload on Kaggle:
row_id,result
1,"23,122"
2,"12"
3,"11,87"
4,"34,43"
5,"112"
6,"56"
7,"99"
8,"102,103"
9,"11"
10,"11,34"

Where:
- `row_id`: Indicates the ID of the query associated with the response in the `result` field.
- `result`: A string containing the IDs (comma-separated) of dishes that meet the criteria specified in the associated query. The `result` field cannot be left empty. There is always at least one dish that satisfies a query.

To match the name of a dish with its corresponding ID, use the file `dish_mapping.json`.  
Example question: "I would like to try Pipe Weed. In which dishes can I find it?"  
Example response: `"1,5"`, assuming the following mapping exists in `dish_mapping.json`:  
```json
{
  "dish_with_pipe_weed_1": 1,
  "dish_with_pipe_weed_2": 5
}
```

# General Rules 🚫

During the challenge, you may use any existing LLM model and any framework/library.

**N.B.:** Remember that creativity in the implemented solution is part of the evaluation criteria!