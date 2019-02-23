
import marioai
import agents

def main():
    agent = agents.RLAgent()
    task = marioai.Task()
    exp = marioai.Experiment(task, agent)
    
    exp.max_fps = 25
    task.env.level_type = 0
    exp.doEpisodes()

if __name__ == '__main__':
    main()