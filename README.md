# EnergyTransitionModelling-Public

Exploring robust climate policies for the energy transition in the Dutch built environment sector. Created for my MSc thesis 
_'Robust Policies: An Exploratory Study on the Energy Transition of the Dutch Built Environment Sector'_ at TU Delft.
An electronic version of the thesis is available at http://repository.tudelft.nl/.

## Abstract
This study set out to analyze the robustness of Dutch energy transition policies under deep uncertainty for the scope of the
built environment sector. Open data is gathered which is used in a System Dynamics model to allow exploration under deep uncertainty. 
The Adaptive Robust Design methodology has been adopted to understand how energy transition policies can be designed to be more 
robust under deep uncertainty for the period of 2019-2050. Subsidy-based policy variants have been created, inspired by promising 
policy instruments from current policy documents. Static, dynamic and mission-oriented policy variants have been simulated to show 
effects on annual CO2-eq emissions, renovated houses and awarded subsidies. Adaptive policies have shown to be promising to curb 
undesired influence of uncertainties. However, this study showed that subsidy percentage, alone, does not ensure that policy targets 
for 2050 are reached. Policies should also ensure ample increase in renovation capacity to keep up with rising demand. The limitation 
of merely subsidy-based policies resulted in less significant differences between the policy variants. To benefit of the adaptive 
nature of the climate plan, policies should include ample adjustment mechanisms within policies to realize their goals by adapting 
to changing circumstances.

## Main dependencies
- EMA Workbench

## 1. Data Preparation
Real world open data has been gathered and prepared to create an extensive data set on a neighbourhood scale. Data hase been gather from:
- [House and energy label data (BAG data)](https://www.rvo.nl/onderwerpen/duurzaam-ondernemen/gebouwen/hulpmiddelen-tools-en-inspiratie-gebouwen/ep-online)
- [Energy consumption, renewable energy sources (Klimaatmonitor)](https://klimaatmonitor.databank.nl/Jive?workspace_guid=bd2cdc7f-43f4-40fd-b306-2854ca8b6ecc.)
- [Renewable heat and green gas (Klimaatmonitor)](https://klimaatmonitor.databank.nl/Jive?workspace_guid=c0c76cd7-02c5-46c5-9cb6-8ba3b2a2de71.)

1. BAG data is scaled to neighbourhood, district and municipality level using `1.Data Preparation/BAG_Data_Prep.py`
2. BAG data is merged with klimaatmonitordata using `1.Data Preparation/Data_merge_modelsetup.ipynb`
3. Finally, `1.Data Preparation/Multi-scale-allignment.ipynb` is run to make sure all neighbourhoods are represented on district and municipality level.

## Exploratory Modelling and Analysis
This section relies on the models provided in `0.Models`. The models have been made using _Vensim DSS_ and are packaged into _stand-alone models_ 
which can be used by anyone (without a license). Experiments on the models are performed using the _experiments_ scripts provided in `2.Base Case Analysis` and `3.Policy Analysis`.

Subsequently, the _scenario discovery_ scripts provided in the same folders offer tools for analysis of the results.
