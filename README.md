# RL for industrial production plants

Job Shop Scheduling problem with Reinforcement Learning

- ##### [INPUT PARAMETERS]

Edit the file `learning_config.json`

{
  "episodes" : 16,
  "training" : 1,
  "checkpoint" : -1,
  "client_server" : 0, 
  "inference_mode" : "local",
  "algorithm_class" : "Dist_Q",
  "exploration":"eps-greedy",
  "off_policy" : 0,
  "lr" : 0.7,
  "update_lr": 1,
  "lr_decreasing_factor": 0.1,
  "gamma" : 0.98, 
  "epsilon" : 0.7,
  "exploration_var_rate" : 0.0,
  "q_init" : -10000.0,
  "observation_space_dict" : {"next_skill": true,
                               "product_name": true,
                               "cppu_state": false,
                               "product_skills_state": true,
                               "counter": false,
                               "previous_cppu": true}
}

`features` specifies the features used to create the datasets. The following alternatives are considered in the paper (make sure to use comma-separated values without spaces!)

- `pt1,pt2,eta1,eta2,delta_phi` is the standard choice for most of the experiments

`cut_mll` specifies the optional cut on the mass feature `mll`:

- `None` to apply no cut
- an integer specifying the cut (e.g., `95` to apply a cut `mll > 95`) 

`norm = True/False` is a boolean specifying whether to apply normalization (as described in the paper) to the training set

`ref_size` is an integer specifying the size of the reference sample ($\mathcal{N_R}$ in the paper)

`bkg_exp_size` is an integer specifying the number of expected background events in the data sample ($N(R)$ in the paper)

`sig_type` is a string specifying the type of signal used to create the data sample:

- `no-signal` if the data sample is composed of background events only (sampled from the path `reference`)
- `resonant` if the data sample contains resonant signal components (the data sample is created by mixing background events from the path `reference` and signal events from the path `signal`)
- `non-resonant` if the data sample contains non-resonant signal components (the data sample is created by sampling Poisson(`bkg_exp_size` + `sig_exp_size`) events from the path `signal` only)

`sig_exp_size` is an integer specifying the number of expected signal events in the data sample ($N(S)$ in the paper)

`poisson` is a boolean flag (True/False) specifying whether the background size and the signal size are to extracted from a Poisson distribution with mean `bkg_exp_size`, `sig_exp_size`, respectively

`n_toy` is an integer specifying the number of toy data samples (number of trainings)

`seed_factor` specifies the seed option for the creation of the reference/data samples. Choose:

- an integer (e.g., `3` ) to be used as a multiplier to compute the seed (example: with `n_toy=100` the seeds will be `3 * [1, ..., 100]`)

- `datetime` to generate a random multiplier based on the current time stamp.

  Background events (for both reference and data sample) are extracted at once by means of the multiplier specified here. Signal events are extracted separately with a new seed derived from the other one.

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
  
