#!/usr/bin/env python


#-*- coding: utf-8 -*-
from __future__ import division
from __future__ import unicode_literals
import re

# This is a naive text summarization algorithm
# Created by Shlomi Babluki
# April, 2013


class SummaryTool(object):

    # Naive method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")

    # Naive method for splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):

        # split the sentence into words/tokens
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_senteces_ranks(self, content):

        # Split the content into sentences
        sentences = self.split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s

        return best_sentence

    # Build the summary
    def get_summary(self, title, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")

        # Add the best sentence from each paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        return ("\n").join(summary)


# Main method, just run "python summary_tool.py"
def main():

    # Demo
    # Content from: "http://thenextweb.com/apps/2013/03/21/swayy-discover-curate-content/"

    title = """
    Swayy is a beautiful new dashboard for discovering and curating online content [Invites]
    """

    content = """
    Australia captain Michael Clarke angrily denied Monday claims that the disastrous England tour has been plagued by off-field dramas, saying it was "absolute garbage".

    Clarke, 34, announced he was retiring after England completed a crushing innings and 78-run victory in the fourth Test at Trent Bridge on Saturday to take an unbeatable 3-1 lead in the five-match Ashes series.

    He will play the final Test at The Oval on August 20 before the curtain comes down on a distinguished career.

    But his departure has been met by rumblings of off-field unrest in the Australian media, with the Sydney Daily Telegraph claiming there was a long-running feud between the wives of two senior players which caused distractions.

    It also claimed Clarke refused to travel on the team bus or socialise with teammates, while the sacking of popular vice-captain Brad Haddin after time off for family reasons did not go down well.

    "There is no disharmony is this group whatsoever. The players are as tight as any team I've been a part of," Clarke told Sydney radio station Triple M. (How Will You Remember Clarke?)

    "Travelling in different cars. What a load of shit.

    "Wives and girlfriends being on tour is a distraction? What a load of shit. That's absolute garbage," he added.

    "I'll give back 10 of my Test 100s if it wasn't for my beautiful wife."

    - 'Stunned' -

    The newspaper had claimed it was "the year-long disintegration in the off-field relationship between Clarke and the rest of the team" that hindered any chance of Ashes success.

    "He often chooses to travel by private car instead of the team bus and rarely attends team get-togethers," it said.

    "On the night that he made his decision to step down, team members were stunned when he joined them for a rare drink in the hotel bar, although he ended the night drowning his sorrows with former teammate Shane Warne rather than any of the current side."

    Cricket Australia chief executive James Sutherland has vowed a full review of the tour, and Clarke said the players had to accept blame.

    "At the end of the day the players are the ones who walk onto the field, we have to perform and we haven't performed well enough," he said.

    In a column for the Sydney Daily Telegraph on Monday, Clarke revealed it was a tough decision to walk away from Test cricket.

    "My entire life has been about cricket. I've thought about the great game every day for as long as I can remember," he said.
    """

    # Create a SummaryTool object
    st = SummaryTool()

    # Build the sentences dictionary
    sentences_dic = st.get_senteces_ranks(content)

    # Build the summary with the sentences dictionary
    summary = st.get_summary(title, content, sentences_dic)

    # Print the summary
    print summary

    # Print the ratio between the summary length and the original length
    print ""
    print "Original Length %s" % (len(title) + len(content))
    print "Summary Length %s" % len(summary)
    print "Summary Ratio: %s" % (100 - (100 * (len(summary) / (len(title) + len(content)))))


if __name__ == '__main__':
    main()
