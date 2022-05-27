The format of the tm_config_input_file:

Type of string:
- strings
--end

Type of strings can be: States, Input alphabet, Tape alphabet, Transitions
Each needs to be follow by ":" in order to be valid.

States:
state_name

at least one state needs to be followed by each of the strings:
state_name, start
state_name, accept
state_name, reject

Input alphabet:
letter

Tape alphabet:
letter

Transitions:
(actual_state,actual_value)->(transition_state,new_value,direction)
-- actual state = the state of the TM
-- actual_value = value where TM is pointing
-- transition_state = the new state of the TM when the 'actual_value' is in the 'actual_state'
-- new_value = the value that will replace the 'actual_value'
-- direction = the direction where the TM will move

The format of the tm_config_input_file:

It is exactly the same with the format of tm_config_file, the only difference being 
an extra type of string: Input:

Input:
string
--end

