**[Developing an AI tutor for boardgames]{.ul}**

**Participants**

Anthony Owen

James Van Der Pol

Gabriel Bosque

Ruizhe Yu Xia

Jeffory Rollason

**Overview and Motivation**

It is commonly known that AI agents can demonstrate super-human
performance in board games, with examples such as AlphaGO and Deep Blue
defeating world champions in Go and Chess. However typically the
rationale for the chosen moves from an AI agent is opaque and not
necessarily interpretable by a human player. In this work we aim to
explore possibilities for developing an AI tutor for Chess, that
combines both strong play with a human readable commentary on the why of
a move. The purpose is ultimately to use AI agents to help human players
improve their game playing abilities.

**Approach**

There are a number of possible approaches. Firstly, building an AI from
scratch that is capable of both playing and reasoning about a game and
also providing commentary and analysis, all within a single modelling
framework. The main advantage of this approach is the explicitly built
link between the reasoning about game moves and the associated
commentary and analysis. The disadvantage is that combining techniques
for language modelling and techniques for game analysis into a single
framework may result in the deterioration in quality of both language
and game playing capabilities. Additionally, this approach may not scale
well to use on a variety of board games.

An alternative approach is to leverage an existing non-interpretable AI
algorithm for playing a board game, and wrap this with the language
capabilities of an LLM. The main advantage of this approach is allowing
a factorisation of the problems of playing a game well and explaining
the rationale for individual moves. The disadvantage is breaking the
link between the move generation and commentary generation.

In this second approach there are again a few possibilities. Firstly, it
may be possible to train an LLM to provide commentary using a bespoke
data set. This data set would consist of pairs of expertly annotated
board positions and the latent embedding from an AI agent (based on a
neural network). The latent embedding would encapsulate the agent's
representation of a board state and move valuations. This training set
could be used to train an LLM to provide commentary on the moves
generated from a non-interpretable AI, helping to bridge the gap between
super-human AI play and human understanding.

Our initial approach is a more simplified version of the above. Here we
directly take the final output (i.e. the top move recommendations) of a
non-interpretable AI and use prompt engineering of an LLM model to
generate commentary. In order to maximise the probability for this
simplified approach to generate meaningful results, the chosen LLM
should have a broad corpus of knowledge in it's training set related to
the game in question. So for our example, we chose Chess. This gives us
a choice of strong chess playing AI agents (in particular we choose
Stockfish), and we can use chatGPT 4 as our LLM which has the broad
amount of Chess related content on the internet available in it's
training set. An additional advantage of choosing Chess, is that a Chess
game can be encoded in a sequence of text tokens in the form of a PGN
description of the game. This formulates a game in a way that can
naturally be processed by an LLM.

More concretely, our process flow is highlighted in the figure below. We
use a PGN file to define a board state (and history of moves) and pass
this information into Stockfish to receive a recommendation on the top 3
moves. These are passed along with the PGN into chatGPT which is tasked
with providing an analysis of material balance, king safety, pawn
structure, immediate threats and a short analysis of the Stockfish
moves.

**Results**

In order to assess the results we examined a number of examples with
specific types of issues in each board state, and analyse the commentary
provided by chatGPT.

**Example 1**

In our first example, Stockfish recommends the move f1d3, and the
chatGPT analysis provides a number of correct insights, including the
threatening of the pawn on h7, and providing the opportunity for
castling in a future move. However, the commentary on taking the pawn
after the move ![](media/image1.png){width="6.6929757217847765in"
height="3.7997889326334207in"}![](media/image2.png){width="2.5208759842519686in"
height="2.346208442694663in"}e4 is incorrect, since this would block the
capture by the bishop.

**Example 2**

In our second example, the commentary from chatGPT is somewhat more
mixed. It is correct in saying that the recommended moves weaken the
squares around the King, however it also suggests that white has already
lost it's black square bishop which is clearly incorrect. This
demonstrates that chatGPT does not necessarily understand the current
state of the board given a history of moves. We will come back to
approaches for fixing this in our conclusion.

**Example 3**

Our final example shows that chatGPT is not able to reliably comment on
moves that have a rationale based on a sequence of future moves. In this
example, the sacrifice of the
knigh![](media/image3.png){width="2.878267716535433in"
height="2.5348950131233594in"}![](media/image4.png){width="2.7116010498687664in"
height="2.3920188101487314in"}t on f3 sets white up for the moves Qa3
placing the king in check and ultimately leading to a checkmate in the
following move. This sequence is entirely missed by chatGPT.

**Conclusion and Future Work**

In conclusion, this approach shows promise as chatGPT is able to provide
commentary that in some instances is correct and insightful. However,
there are a number of issues to be addressed including mis-understanding
of the board state and lack of understanding on the potential for future
moves and how they may impact the board state. A number of immediate
improvements can be made which the authors expect would improve the
quality of the commentary.

Firstly, inputting the FEN string (which encapsulates the board state)
in addition to the PGN into chatGPT should reduce instances of chatGPT
hallucinating pieces. Additionally, using Stockfish to provide not just
the best next move, but the expected best next moves to say 3 or 4 ply,
would provide chatGPT with additional information on which to base a
commentary on more advanced situations such as that seen in our third
example.

Ultimately, the authors expect that fine tuning an LLM with annotated
game play throughs would help unlock the power of LLMs to support humans
in interpreting the play of super-human AI agents.
