prompt = """Input: List files Output: Is —I 
Input: Count files in a directory Output: is —1 1 we —1 
Input: Disk space used by home directory 
Output: du ~
Input: Replace foo with bar in all .py files 
Output: sed -I .bak -- .s/foo/bar/W •.py 
Input: Delete the models subdirectory 
Output: rm -rf ./models"""
template = """
Input: {}
Output = """
import os, click, openai
while True: request = input(click.style("nlsh>", "red", bold=True))
prompt += template.format(request)
result = openai.Completion()
