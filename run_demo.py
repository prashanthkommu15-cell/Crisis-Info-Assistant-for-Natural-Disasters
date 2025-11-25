import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from project.main_agent import run_agent
if __name__ == '__main__':
    print(run_agent('Is there a flood warning in Manila?'))
