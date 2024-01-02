# pyactionmap
Created for MWLL to edit action maps as part of the crysis user profiles. Replaces earlier java based code with something which is hopefully easier to maintain and validate. 

Tries to improve on previous action mapper code by using default action maps to configure how the keys are displayed and their ordering without baking those details deep into the code.

An XML dtd has been created to cover some of the basics of validation, some of the validation is baked into the code where the dtd couldn't.
(dtd docs should be checked to see if more can be added.)

Order of the default map matters, this sets the display order.

A "visible" and "map" tag are added in the default map to set which action sets are visible, and their order.
Also added a "display_name" attribute to actions to override the ugly internal var names for display. 
