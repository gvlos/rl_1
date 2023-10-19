# RL for industrial production plants

Job Shop Scheduling problem with Reinforcement Learning

- ##### [INPUT PARAMETERS]

Edit the file `learning_config.json`

`episodes` specifies the number of training episodes (an episode end when production is completed) --> [int]

`training` is a flag specifying whether or evaluated only --> [int]
- `1` if the model has to be trained before evaluation
- `0` evaluation only (requires checkpoint files)

`checkpoint` specifies checkpoint logic --> [int] (DEFAULT -1)
- `-1` save checkpoint every x episodes (with x being a fixed variable specified inside code)
- `0` no checkpoint
- `freq` is an integer specifying the checkpoint frequency
Note: every time a new checkpoint overrides the last one. Before evaluation, the final checkpoint is marked with a label `_trained`

`client_server' is  a flag specifying if rllib client-server interface has to be created (required `1` for rllib algorithms) --> [int]

`algorithm_class` specifies the name of the RL algorithm used --> [str]
- `Dist_Q` for distributed Q-learning (custom)
- `PPO` for Proximal Policy Optimization (rllib)
- ...

`exploration` defines the type of exploration (logic of random action selection)
- `eps-greedy`
- `softmax`

`lr` is the learning rate --> [float]

`update_lr` is a flag specifying whether the learning rate has to be updated across training episodes --> [0,1]

`lr_decreasing_factor` specifies the decreasing factor of the learning rate (if `update_lr`=1) (e.g., if `lr_decreasing_factor`=0.1 it means the overall decrease of the learning factor is `lr`*0.1

`gamma` is the discount factor,

`epsilon` is the parameter of the epsilon-greedy exploration

`tau` is the parameter of the softmax exploration

`exploration_var_rate` is the decreasing rate of the exploration factor (epsilon or tau), with the same logic of `lr_decreasing_factor`

`observation_space_dict` is a dictionary specifying the content of the observation:
- "next_skill": next skill to be executed,
- "product_name": name of the product,
- "cppu_state": flag specifying if the cppu is busy or free,
- "product_skills_state": one-hot vector specifying all the remaining skills to be executed,
- "counter": counter of seen observations (retrieved from Q-table when Dist_Q algorithm is used),
- "previous_cppu": name of cppu that has passed the product

Specific parameters for `Dist_Q` algorithm:

- `q_init` is the number used for uniform initialization of the Q table

Specific parameters for all rllib algorithms:

- `inference_mode` specifies if the model has to be copied from server to client for local/remote inference
- `off_policy` specifies if the training procedure should follow an off-policy approach

plus check specific algorithms parameters



- ##### [OUTPUT]

  ├── src
  
    ├── controller
  
    │   ├── **/*.css
  
    ├── views
  
    ├── model
  
    ├── index.js
  
├── public

    ├── css
    
    │   ├── **/*.css
    
    ├── images
    
    ├── js
    
    ├── index.html
    
├── dist (or build

├── node_modules

├── package.json

├── package-lock.json 

└── .gitignore

- ##### [HYPERPARAMETER TUNING]

  Edit the file `hyperparam_tuning.py`
  
