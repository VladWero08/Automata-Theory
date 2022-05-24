The format of cfg_config_file:

Type of string:
-strings
--end

Type of string can be: "Variables:", "Terminals:", "Rules:"

The last one MUST be the rules, in order to check the validity of the
variables & terminals included in the specific rule. The order of the 
first two doesn't matter.

The starting variable will be followed by ", start"

Each rule should have this format: variable -> combination of variables | combination of terminals,
where | is the or operator.
