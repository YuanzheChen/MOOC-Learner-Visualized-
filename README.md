# MOOC-Learner-Visualized
---------------------------
Visualize the MOOC learner features with MOOC-Learner-Visualized (MLV)


Paper Type:
Please refer to the discussion of paper types for more information. Select the most appropriate type for this paper in your opinion, even if it does not match the choice of the authors.
* Algorithm / Technique
* Application / Design Study
* Evaluation
* Theory / Model
* System

Algorithm / Technique

Scope (relevance to the event):
Does the paper fit into the scope of the event, or is it (somehow) off-topic?
3 - Core topic, fits well
2 - Peripheral, but of interest, somehow
1 - Off topic, does not fit

3

Contribution (novelty, originality):
hen judging non-classical research papers (that do not attempt to contribute a new methodology, for example, to the field, like application papers, for example), then special care is required here (every acceptable paper needs to have a valuable contribution, but what a valuable contribution is depends significantly on the type of paper).
5 - Breakthrough: excellent contribution, opens up exciting new frontiers
4 - Strong: a strong contribution, clearly fill a gap in the literature
3 - Reasonable: some valuable contribution
2 - Minor: only incremental improvements over previous work
1 - None: no valuable contribution, or the claimed contributions are already published

3

References:
3 - At large, all important references are included
2 - Some important references are missing
1 - Major areas of previous work ignored

3

Utility, Importance (relevance in general):
Does the paper provide a relevant, needed contribution? Is there a potential that this paper could become an important reference for future work? Is the paper relevant for important applications?
3 - Addresses clear need
2 - Possibly useful
1 - Case for utility not compelling

3

Soundness (technical soundness, soundness of approach):
Is paper technically sound (when this question is applicable)? Is the chosen approach sound/correct? Is the presented research methodology sound?
3 - Approach is (technically) correct and well justified
2 - Some concerns on correctness, some choices questionable
1 - Fundamentally unsound (technical) approach

2

Reproducability:
3 - Everything critical is discussed
2 - Many issues discussed, but some important details left out
1 - Work cannot be replicated because too many critical aspects remain murky

3

Presentation Quality:
5 - Excellent: exposition is clear and writing flows well
4 - Good: only minor typos and grammar problems
3 - Fair: some structural changes or some wordsmithing needed
2 - Poor: major structural changes or extensive wordsmithing needed
1 - Unpublishable: too difficult to understand

4

Overall Rating:
Provide your overall rating of the paper. If possible, avoid the Borderline category and reserve it for truly indeterminate cases. Also, use the entire scale for your evaluation, clear statements are appreciated.
5 - Definite accept: I would argue strongly for accepting this paper.
4 - Probably accept: I would argue for accepting this paper.
3 - Borderline: the strengths and weaknesses balance for this paper.
2 - Probably reject: I would argue for rejecting this paper.
1 - Definite reject: I would argue strongly for rejecting this paper.

3

Expertise:
Provide your expertise in the topic area of this paper.
4 - Expert
3 - Knowledgeable
2 - Passing Knowledge
1 - No Knowledge

3

Best Paper:
Should this submission be considered for the best paper award?
No
Yes

No

The Review:
Explain your reasons for the numeric ratings above, addressing the following questions.
* What are the major contributions of the paper to the visualization literature?
* What are its strengths and weaknesses?
* Is this work relevant for the EuroVis symposium, and if not what other venues would be appropriate?
* Is this work novel, incremental, or previously published?
* Is the previous work adequately referenced, and if not what citations should be added?
* Is the work important and useful?
* Are the technical results sound?
* Are the techniques described in enough detail that a skilled graduate student could reproduce them?
* Are any important details or analyses missing?
* Is the exposition clear? How could the structure or style of the presentation be improved?
* Should anything be deleted or condensed from the writeup?
* Are the figures as informative as possible?
* Is the (optional) supplementary material helpful (if provided)?
[your full text review here]

This paper presents a framework, along with a visualization system, to help generate visualizations for model parameter space analysis. The paper is well motivated since helping users without VIS background to generate visualizations is a meaningful and timely topic. The draft is also well structured. The formation of the framework is carefully discussed step by step. My main concern of this draft is about the method to generate visualization candidates and recommend them to users. Below is the detail:

First, it is better to discuss in general what are the differences between the design space of VPSA and general visual analytics, which can provide a clearer definition of the problem. After that, the candidates are selected based on literature survey. It is difficult to prove that the resulted tasks and visual design is a reasonable design space for VPSA. For example, if one previous work modifies a common visual design, how to count it in the candidates. Whether an analytical tasks appear in literatures are general tasks or specified to VPSA? There are many detailed questions remain unsolved. 

Related to the first issue, I think recommend visual design with tasks is a reasonable idea, however, the ranked recommendation is questionable. It is only valid when assume the importance of a design is close related to its occurrence in literatures. However, such assumption is probably incorrect. For example, mostly users analyze models in a specific domain where the importance of a design can be different from it in general VPSA, therefore, the ranking can be misleading. Besides, I think the score is difficult to understand. For example, what is the difference between 2 over 1.5?

Mainly because of the above issues, my review is on the border-line.

Below are a few minor issues.

1. Section. 3 mentioned 7 requirements. R4 and R5 is kind of different from others, which is about high-level analysis. I would suggest to revise them. Besides, R6 never appears in following sections.

2. The draft is 12 pages long, and exceeds the usual length of euroVis paper. Some parts of the draft is not necessary. For example, section 6.2 can be combined into case studies.

3. some grammar errors and typos. For example,
P3: doesn’t take advantage nor does it adhere to the mental model of input-output model analysis.
P5: as outlined in Section ??. After filtering, nine papers
P6: If a task is supported in a row (i.e., paper), the algorithm increases S occordingly.
