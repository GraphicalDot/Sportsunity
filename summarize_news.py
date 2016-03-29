#!/usr/bin/env python

import os
import sys
from news_summary import FrequencySummarizer


class ShortNews:
    
        def __init__(self):
                self.object1 = FrequencySummarizer()

        def summarization(self,full_news):
                try:
                        short_news=''.join(self.object1.summarize(full_news,4)).replace('\n','')
                        return short_news+' ...Read More'
                except:
                        short_news=''.join(self.object1.summarize(full_news,1)).replace('\n','')
                        return short_news+' ...Read More'



def main():
        text = """India were set a target of 176 and had to survive 9 overs. Dhawan who had not taken the field the entire day due to an injury on his right hand, strode out with Rahul. Mathews started with pace and spin, but switched quickly to an all spin attack. Herath took his first wicket of the match and sent back Rahul cheaply. Ishant came as the nightwatchman and survived a few nervous moments.
        At lunch they were 108/5, but what followed soon after surprised everyone. Chandimal and Thirimanne played aggressively to add 125 for the 6th wicket. The wicket-keeper kept going even after losing his partner and added crucial partnerships with Mubarak and Kaushal. He registered his 4th Test ton - first against a Test playing nation apart from Bangladesh and remained unbeaten. The Indians were completely lost for ideas. Kohli was worried when Chandimal was going great guns. Ashwin once again was the pick of the bowlers as he registered his third 10-wicket haul. Mishra gave him good support collecting 3 wickets of his own.
        A very good day for Sri Lanka. In fact, good second and third sessions. They didn't start well as Dhammika, the nightwatchman was sent back off the first ball of the day. The score was reading 5/3 when Mathews joined Sangakkara at the crease. The experienced duo started to milk the bowling around and didn't concede a single maiden over until the veteran was picked by Ashwin. The skipper soon followed and once more the hosts found themselves in trouble."""

        obj = ShortNews()
        obj.summarization(text)

                
                
if __name__=="__main__":
        main()











